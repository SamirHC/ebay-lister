import base64
import boto3
from botocore.client import Config
import os
import urllib.parse
import logger
from dotenv import dotenv_values

config = dotenv_values(".env")

BUCKET_NAME = config["AWS_BUCKET_NAME"]
REGION_NAME = config["AWS_REGION_NAME"]

IMAGE_DIR = os.path.join(os.getcwd(), "images")

s3 = boto3.client(
    "s3", region_name=REGION_NAME, config=Config(signature_version="s3v4")
)


def upload_image(rel_path):
    image_path = os.path.join(IMAGE_DIR, rel_path)
    s3.upload_file(image_path, BUCKET_NAME, rel_path)
    logger.log_response(f"Uploaded {image_path} to {BUCKET_NAME}/{rel_path}.")


def get_public_url(rel_path):
    encoded_object_key = urllib.parse.quote_plus(rel_path)
    return f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{encoded_object_key}"


def is_image_path(path: str):
    image_file_extensions = [".png", ".jpeg", ".jpg", ".PNG", ".JPEG", ".JPG"]
    return any(path.endswith(ext) for ext in image_file_extensions)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
