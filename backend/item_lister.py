import os


def list_item(path: str):
    # if not path.endswith(".png"):
    #     return
    print(path)


def list_items(dir: str):
    """Takes a directory and lists all items given by the images to eBay."""
    path = os.path.join(os.getcwd(), dir)
    for filepath in os.listdir(path):
        list_item(filepath)
