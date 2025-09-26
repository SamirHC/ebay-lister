import os
import urllib.parse

import base64
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


def upload_image(dir, file):
    image_path = os.path.join(IMAGE_DIR, dir, file)
    aws_path = f"{dir}/{file}"
    s3.upload_file(image_path, BUCKET_NAME, aws_path)
    logger.log_response(f"Uploaded {image_path} to {BUCKET_NAME}/{aws_path}.")


def get_public_url(dir, file):
    encoded_object_key = urllib.parse.quote_plus(f"{dir}/{file}")
    return f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{encoded_object_key}"


def is_image_path(path: str):
    image_file_extensions = [".png", ".jpeg", ".jpg", ".PNG", ".JPEG", ".JPG"]
    return any(path.endswith(ext) for ext in image_file_extensions)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
