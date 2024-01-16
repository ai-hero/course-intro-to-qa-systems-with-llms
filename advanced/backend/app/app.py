""" Backend """
import json
import logging
import os
import sys
import traceback
from typing import Any
from uuid import uuid4

import chromadb
import redis  # type: ignore
from chromadb.config import Settings
from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
from minio import Minio
from minio.error import S3Error
from openai import OpenAI
from werkzeug.exceptions import HTTPException, UnprocessableEntity

# The flask api for serving predictions
app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
CORS(app)


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

bucket_name = os.environ["S3_BUCKET_NAME"]


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


@app.errorhandler(HTTPException)  # type: ignore
def handle_exception(e: Any) -> Any:
    """
    To keep all responses consistently JSON.
    Return JSON instead of HTML for HTTP errors.
    """
    return (
        jsonify(
            {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        ),
        e.code,
    )


@app.route("/", methods=["GET"])  # type: ignore
@app.route("/ping", methods=["GET"])  # type: ignore
@app.route("/health_check", methods=["GET"])  # type: ignore
def health_check() -> Any:
    """
    The health check makes sure container is ok.
    Checks the status of MinIO and Redis connections.
    """
    try:
        # Check MinIO connection
        minio_client.list_buckets()
        minio_status = "healthy"
    except Exception as e:
        traceback.print_exc()
        minio_status = "unhealthy"
        minio_error = str(e)

    try:
        # Check Redis connection
        redis_client = redis.StrictRedis(connection_pool=redis_pool, decode_responses=True)
        redis_client.ping()
        redis_status = "healthy"
    except Exception as e:
        traceback.print_exc()
        redis_status = "unhealthy"
        redis_error = str(e)

    if minio_status == "healthy" and redis_status == "healthy":
        return jsonify({"success": True, "minio_status": minio_status, "redis_status": redis_status}), 200
    else:
        return (
            jsonify(
                {
                    "success": False,
                    "minio_status": minio_status,
                    "redis_status": redis_status,
                    "minio_error": minio_error if minio_status == "unhealthy" else None,
                    "redis_error": redis_error if redis_status == "unhealthy" else None,
                }
            ),
            500,
        )


@app.route("/uploads/<folder>/<filename>", methods=["PUT"])  # type: ignore
def uploads(folder: str, filename: str) -> Any:
    """Return presigned url to upload file"""
    if not (filename.endswith(".txt") or filename.endswith(".md")):
        raise UnprocessableEntity("Only .txt files are accepted")

    # Generate presigned URL for upload
    try:
        presigned_url = minio_client.presigned_put_object(bucket_name, f"/uploads/{folder}/{filename}")
    except S3Error as err:
        return str(err), 500

    # Redirect to presigned URL
    return redirect(presigned_url, code=307)


@app.route("/ingest/<folder>/<filename>", methods=["POST"])  # type: ignore
def ingest(folder: str, filename: str) -> Any:
    """Send ingest message for uploaded file to queue"""
    upload_id = str(uuid4())
    ingest_obj = {
        "upload_id": upload_id,
        "folder": folder,
        "filename": filename,
        "bucket_name": bucket_name,
        "path": f"/uploads/{folder}/{filename}",
    }

    try:
        redis_client = redis.StrictRedis(connection_pool=redis_pool, decode_responses=True)
        redis_client.lpush("ingest", json.dumps(ingest_obj))
    except redis.exceptions.RedisError as e:
        raise HTTPException(f"Unable to add to ingest queue: {e}")

    return jsonify(ingest_obj), 200


@app.route("/chat", methods=["POST"])  # type: ignore
def chat():
    """Answer a question given a context."""
    request_obj = request.get_json()
    question = request_obj["question"]
    embedding = get_embedding(question)
    results = chroma_collection.query(query_embeddings=[embedding], n_results=3)
    context = "\n".join([m["text"] for m in results["metadatas"][0]])

    if not question.endswith("?"):
        question = question + "?"

    # Combine the summaries into a prompt and use SotA GPT-4 to answer.
    prompt = (
        # Identity
        "Your name is Milo. You are a chatbot representing the MLOps Community. "
        # Purpose
        "Your purpose is to answer questions about the MLOps Community. "
        # Introduce yourself
        "If the user says hi, introduce yourself to the user."
        # Scoping
        "Please answer the user's questions based on the provided context. "
        "If the answer is not in the context, reply 'I don't know'. "
        "If the answer contains some personal information, remove it before answering. "
        "But if it cannot be removed, please politely decline to answer."
        "\nContext:```\n"
        f"{context}"
        "```"
        f"\nQuestion: {question}"
    )
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    answer = completion.choices[0].message.content
    return jsonify({"answer": answer}), 200


if __name__ == "__main__":
    app.run(debug=True)
