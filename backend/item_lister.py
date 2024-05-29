import os
import image_encoder
from chatgpt import chatgpt


PROMPT = """
    WRITE AN EBAY UK TITLE FOR THIS ITEM. Take into account what ebay uk 
    category the item is and therefore INCLUDE ANY REQUIRED ITEM SPECIFICS for 
    that category IN THE TITLE. You must make sure that the title does not 
    exceed 80 characters. Refrain from saying what country the item is made in. 
    Just give the answer without speech marks at the beginning and end."
"""

def list_item(path: str):
    if not path.endswith(".png"):
        return
    print(path)
    base64_image = image_encoder.encode_image(path)
    response = chatgpt.get_chatgpt_4o_response(PROMPT, base64_image)
    print(response)


def list_items(dir: str):
    """Takes a directory and lists all items given by the images to eBay."""
    path = os.path.join(os.getcwd(), dir)
    for filepath in os.listdir(path):
        list_item(os.path.join(path, filepath))

IMAGE_DIR = os.path.join(os.getcwd(), "images")


list_items(IMAGE_DIR)
