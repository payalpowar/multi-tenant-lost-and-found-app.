import uuid
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile, status

from core.config import settings, UPLOAD_DIR

ALLOWED_CONTENT_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


async def validate_image(image: UploadFile) -> None:
    if image.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Allowed: JPEG, PNG, WEBP",
        )

    image.file.seek(0, 2)
    size = image.file.tell()
    image.file.seek(0)

    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if size > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Max size is {settings.MAX_UPLOAD_SIZE_MB}MB",
        )


def _build_filename(content_type: str) -> str:
    extension = ALLOWED_CONTENT_TYPES[content_type]
    return f"{uuid.uuid4()}{extension}"


async def _upload_to_s3(
    file_bytes: bytes,
    content_type: str,
    key_prefix: str,
) -> str:
    filename = _build_filename(content_type)
    object_key = f"{key_prefix}/{filename}"

    client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )

    try:
        client.put_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=object_key,
            Body=file_bytes,
            ContentType=content_type,
        )
    except ClientError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload image to S3",
        ) from exc

    return f"https://{settings.S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{object_key}"


async def _upload_to_local(
    file_bytes: bytes,
    content_type: str,
    key_prefix: str,
) -> str:
    filename = _build_filename(content_type)
    folder = UPLOAD_DIR / key_prefix
    folder.mkdir(parents=True, exist_ok=True)

    file_path = folder / filename
    file_path.write_bytes(file_bytes)

    return f"{settings.BASE_URL}/uploads/{key_prefix}/{filename}"


async def upload_image(
    image: UploadFile,
    key_prefix: str,
) -> str:
    await validate_image(image)

    file_bytes = await image.read()

    if settings.USE_S3:
        if not settings.S3_BUCKET_NAME:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="S3 bucket is not configured",
            )
        return await _upload_to_s3(file_bytes, image.content_type, key_prefix)

    return await _upload_to_local(file_bytes, image.content_type, key_prefix)
