import uuid
from functools import lru_cache

import boto3
from botocore.config import Config

from api.settings import get_settings


settings = get_settings()


@lru_cache
def get_s3_client():
    return boto3.client(
        "s3",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version="s3v4"),
    )


def generate_s3_key(session_component_id: int) -> str:
    return f"videos/{session_component_id}/{uuid.uuid4().hex}"


def generate_upload_url(s3_key: str) -> str:
    client = get_s3_client()
    return client.generate_presigned_url(
        "put_object",
        Params={"Bucket": settings.S3_BUCKET_NAME, "Key": s3_key},
        ExpiresIn=settings.S3_UPLOAD_URL_TTL,
    )


def generate_read_url(s3_key: str) -> str:
    client = get_s3_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.S3_BUCKET_NAME, "Key": s3_key},
        ExpiresIn=settings.S3_READ_URL_TTL,
    )


def delete_object(s3_key: str) -> None:
    client = get_s3_client()
    client.delete_object(Bucket=settings.S3_BUCKET_NAME, Key=s3_key)
