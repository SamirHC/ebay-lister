import base64
import boto3
from botocore.client import Config
import os

s3 = boto3.client("s3", region_name="eu-west-2", config=Config(signature_version="s3v4"))
BUCKET_NAME = "ebay-lister-images"
IMAGE_DIR = os.path.join(os.getcwd(), "images")
EXPIRATION = 7200  # 2 hours

def upload_image(rel_path):
    image_path = os.path.join(IMAGE_DIR, rel_path)
    s3.upload_file(image_path, BUCKET_NAME, rel_path)
    print(f"Uploaded {image_path} to {BUCKET_NAME}/{rel_path}.")
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": rel_path},
        ExpiresIn=EXPIRATION
    )
    print(f"Pre-Signed URL: {url}")
    return url

def is_image_path(path: str):
    return path.endswith(".png") or path.endswith(".jpeg")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
