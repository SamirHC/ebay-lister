import os
import image_encoder
from chatgpt import chatgpt


def list_item(path: str):
    if not path.endswith(".png"):
        return
    print(path)
    base64_image = image_encoder.encode_image(path)
    response = chatgpt.get_chatgpt_4o_response(
        "Create an eBay listing from the provided image.", base64_image
    )
    print(response)


def list_items(dir: str):
    """Takes a directory and lists all items given by the images to eBay."""
    path = os.path.join(os.getcwd(), dir)
    for filepath in os.listdir(path):
        list_item(filepath)

IMAGE_DIR = os.path.join(os.getcwd(), "images")
list_items(IMAGE_DIR)
