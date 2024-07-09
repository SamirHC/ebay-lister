import base64
import boto3
from botocore.client import Config
import os
import urllib.parse

BUCKET_NAME = "ebay-lister-images"
IMAGE_DIR = os.path.join(os.getcwd(), "images")
EXPIRATION = 7200  # 2 hours
REGION_NAME = "eu-west-2"

s3 = boto3.client("s3", region_name=REGION_NAME, config=Config(signature_version="s3v4"))

def upload_image(rel_path):
    image_path = os.path.join(IMAGE_DIR, rel_path)
    s3.upload_file(image_path, BUCKET_NAME, rel_path)
    print(f"Uploaded {image_path} to {BUCKET_NAME}/{rel_path}.")

def get_public_url(rel_path):
    encoded_object_key = urllib.parse.quote_plus(rel_path)
    return f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{encoded_object_key}"

def is_image_path(path: str):
    image_file_extensions = [".png", ".jpeg", ".jpg", ".PNG", ".JPEG", ".JPG"]
    return any(path.endswith(ext) for ext in image_file_extensions)
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
