""" Backend """
import json
import logging
import os
import sys
import traceback
from typing import Any
from uuid import uuid4

import redis  # type: ignore
from flask import Flask, jsonify, redirect
from flask_cors import CORS
from minio import Minio
from minio.error import S3Error
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


if __name__ == "__main__":
    app.run(debug=True)
