"""Ingest Message Queue Processor"""
import json
import logging
import os
import sys
import traceback
from io import StringIO
from typing import Any, Dict, Optional
from uuid import uuid4

import chromadb
import redis  # type: ignore
from chromadb.config import Settings
from minio import Minio
from minio.error import S3Error
from openai import OpenAI

# Set up logger
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

# Initialize Redis Client
REDIS_URL = os.environ["REDIS_URL"]
REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]
REDIS_DB = os.environ.get("REDIS_DB", "0")  # Default to DB 0 if not specified
REDIS_PROTOCOL = os.environ.get("REDIS_PROTOCOL", "redis")
REDIS_CONNECTION_STRING = f"{REDIS_PROTOCOL}://:{REDIS_PASSWORD}@{REDIS_URL}/{REDIS_DB}"
redis_pool = redis.ConnectionPool.from_url(REDIS_CONNECTION_STRING)

# Initialize MinIO client
minio_client = Minio(
    os.environ["S3_URL"],
    region=os.environ["S3_REGION"],
    access_key=os.environ["S3_ACCESS_KEY_ID"],
    secret_key=os.environ["S3_SECRET_ACCESS_KEY"],
    secure=(os.environ["S3_SECURE"].lower() == "true"),
)

# Initialize Open AI client
client = OpenAI()


# Initialize Chroma Client
# create client and a new collection
chroma_collection_name = "blogs"

chroma_client = chromadb.HttpClient(
    host=os.environ["CHROMA_URL"],
    port=os.environ["CHROMA_PORT"],
    settings=Settings(
        chroma_client_auth_provider="chromadb.auth.token.TokenAuthClientProvider",
        chroma_client_auth_credentials=os.environ["CHROMA_AUTH_TOKEN"],
    ),
)
chroma_client.heartbeat()

try:
    # Create the collection
    chroma_collection = chroma_client.get_collection(chroma_collection_name)
except (Exception, ValueError):
    # Create the collection if it doesn't exist
    chroma_collection = chroma_client.create_collection(chroma_collection_name)


def get_embedding(text: str) -> Any:
    """Use the same embedding generator as what was used on the data!!!"""
    if len(text) > 8000:  # Hack to be under the 8k limit
        text = text[:8000]
    response = client.embeddings.create(model="text-embedding-ada-002", input=text)
    return response.data[0].embedding


def fetch_content(bucket_name: str, path: str) -> Optional[str]:
    """Fetch content from S3"""
    try:
        # Get the object from the bucket
        response = minio_client.get_object(bucket_name, path)

        # Read the response into StringIO
        file_content = StringIO(response.read().decode("utf-8"))

        # Now, you can use file_content as a file-like object
        # For example, to read its contents you can do:
        content = file_content.read()

        # Remember to close the StringIO object when done
        file_content.close()
        return content
    except S3Error:
        log.error("Cannot get content from S3")
        return None


def ingest(request_obj: Dict[str, str]) -> None:
    """Ingest a document from MQ"""
    upload_id = request_obj["upload_id"]
    bucket_name = request_obj["bucket_name"]
    path = request_obj["path"]
    log.info("Ingesting %s: %s/%s", upload_id, bucket_name, path)

    content = fetch_content(bucket_name, path)
    if content:
        upsert(content, request_obj)


def upsert(content: str, context: Dict[str, str]) -> None:
    """Upsert embeddings for document chunks in db"""
    path = context["path"]
    filename = context["filename"]
    folder = context["folder"]

    # Delete existing for this doc
    chroma_collection.delete(where={"path": path})

    # Dummy chunking
    chunks = [chunk for chunk in content.split("\n\n") if chunk.strip()]
    log.info("Upserting %s chunks for %s/%s", len(chunks), folder, filename)
    embeddings = []
    metadatas = []
    ids = []
    for i, chunk in enumerate(chunks):
        chunk_id = f"{folder}/{filename}/{i}"
        log.info(chunk_id)
        embedding = get_embedding(chunk)
        embeddings.append(embedding)
        metadatas.append(request_obj)
        ids.append(chunk_id)
    chroma_collection.add(embeddings=embeddings, metadatas=metadatas, ids=ids)
    log.info("Done.")


if __name__ == "__main__":
    log.info("Starting queue...")
    while True:
        try:
            # Wait for predict request on request topic
            log.info("Waiting for request message...")
            try:
                redis_client = redis.StrictRedis(connection_pool=redis_pool, decode_responses=True)
                _, msg = redis_client.brpop("ingest")
            except redis.exceptions.RedisError as e:
                raise SystemExit(f"Unable to read from ingest queue: {e}")
            request_obj = json.loads(msg.decode("utf-8"))

            # request_obj example:
            # {
            #     "upload_id": upload_id,
            #     "folder": folder,
            #     "filename": filename,
            # }

            # We need an id so that our response message can include
            # the identifier. We extract it before the validation,
            # in order to send the error message in case the validation fails.
            _id = request_obj.get("id", str(uuid4()))

            # Ingest
            ingest(request_obj)

        except Exception:  # pylint: disable=broad-except
            traceback.print_exc()
