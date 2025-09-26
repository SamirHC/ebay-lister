import os
from pathlib import Path
import urllib.parse

import boto3
from botocore.client import Config
from dotenv import load_dotenv

from app.utils import logger


load_dotenv()


BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
REGION_NAME = os.getenv("AWS_REGION_NAME")

IMAGE_DIR = os.path.join(os.getcwd(), "images")

s3 = boto3.client(
    "s3", region_name=REGION_NAME, config=Config(signature_version="s3v4")
)


def upload_image(path: Path) -> str:
    abs_path = path.resolve()
    aws_path_str = abs_path.relative_to(IMAGE_DIR).as_posix()
    s3.upload_file(str(path), BUCKET_NAME, aws_path_str)
    logger.log_response(f"Uploaded {path} to {BUCKET_NAME}/{aws_path_str}.")
    return get_public_url(aws_path_str)


def get_public_url(aws_path: str) -> str:
    encoded_object_key = urllib.parse.quote_plus(aws_path)
    return f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{encoded_object_key}"
