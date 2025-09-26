from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path

from app import chatgpt
from app.data import ebay_images
from app.data.ebay_categories import get_ebay_categories_df, get_all_specifics
from app.ebay_item import EbayItemBuilder, EbayItem
from app import s3
from app.utils import logger
from app.utils import time_util


MAX_ATTEMPTS = 5
MAX_WORKERS = 20


def get_json_prompt():
    return f"""
        You are a clothes seller on eBay. Given the images, produce information 
        for an SEO optimised listing, taking into account what eBay UK category 
        the item is by using the table provided. INCLUDE ALL REQUIRED ITEM 
        SPECIFICS for that category IN THE TITLE.
        You must make sure that the title does not exceed 80 characters. 
        Refrain from saying what country the item is made in.

        Respond in raw JSON for parsing with Python json.loads:
        {{
            "title": str,
            "category_id": int,
            "item_specifics": {{
                "<item specific name>": str,
                ...
            }}
        }}

        For example, given images with the title:
        "M&S Collection womens pink floral blouse size 14 long sleeve top"
        An appropriate output could be:
        {{
            "title": "M&S Collection womens pink floral blouse size 14 long sleeve top",
            "category_id: 53159,
            "item_specifics": {{
                "Brand": "M&S Collection",
                "Size": "14",
                "Type": "Blouse",
                "Colour": "Pink",
                "Department": "Women",
                "Sleeve Length": "Long Sleeve"
            }}
        }}

        Here is the item specifics and category id table:
        {get_ebay_categories_df().to_string()}
    """


def get_image_urls_for_item(subdir: Path) -> list[str]:
    return [s3.upload_image(fp)
            for fp in ebay_images.iter_item_dir_image_paths(subdir)]


def get_image_urls() -> dict[str, str]:
    image_urls = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_subdir = {executor.submit(get_image_urls_for_item, s): s
                            for s in ebay_images.iter_item_dirs()}
        for future in as_completed(future_to_subdir):
            s = future_to_subdir[future]
            image_urls[s] = future.result()

    return image_urls


def get_ebay_items(image_urls: dict[str, list[str]]) -> list[EbayItem]:
    NUM_SUBDIRS = len(image_urls)
    res = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_subdir = {executor.submit(try_get_ebay_item, s, urls): s for s, urls in image_urls.items()}
        for future in as_completed(future_to_subdir):
            s = future_to_subdir[future]
            res.append((s, future.result()))
    
    res.sort()

    logger.log_response("")
    logger.log_response(f"Progress: {NUM_SUBDIRS}/{NUM_SUBDIRS} (100%)")
    logger.log_response(f"Failed jobs: {[s for s,r in res if r is None]}")
    logger.log_response("")

    return [r for _, r in res if r is not None]


def try_get_ebay_item(s: str, subdir_image_urls: list[str]) -> EbayItem:
    ebay_item = None
    count = 0
    while ebay_item is None and count < MAX_ATTEMPTS:
        count += 1
        try:
            ebay_item = get_ebay_csv_item_json(subdir_image_urls)
        except Exception as e:
            logger.log_response(
                f"Something went wrong when getting the csv line for item {s}: {e}"
            )
            if count < MAX_ATTEMPTS:
                logger.log_response(f"Trying again (attempt {count}) for item {s}")
            else:
                logger.log_response(f"Maximum attempts made ({count}) for item {s}")
    return ebay_item


def get_ebay_csv_item_json(image_urls: list[str]) -> EbayItem:
    image_info = chatgpt.get_chatgpt_response(get_json_prompt(), image_urls)
    logger.log_response(f"ChatGPT output: {image_info}")

    try:
        data = json.loads(image_info)
    except:
        raise Exception(f"ChatGPT output is not json.loads compatible:\n{image_info}")

    try:
        assert isinstance(data["category_id"], int)
    except:
        raise Exception("Non-int category_id (Comma in title?)")

    return (
        EbayItemBuilder(image_urls)
        .set_title(data["title"])
        .set_description(data["title"])
        .set_category_id(data["category_id"])
        .set_item_specifics([x for item in data["item_specifics"].items() for x in item])
        .build()
    )  # May raise exception if item_specifics aren't fulfilled


def write_items_to_csv(ebay_items: list[EbayItem]):
    CSV_HEADER = f"""
#INFO,Version=0.0.2,Template= eBay-draft-listings-template_GB,,,,,,,,
#INFO Action and Category ID are required fields. 1) Set Action to Draft 2) Please find the category ID for your listings here: https://pages.ebay.com/sellerinformation/news/categorychanges.html,,,,,,,,,,
#INFO After you've successfully uploaded your draft from the Seller Hub Reports tab, complete your drafts to active listings here: https://www.ebay.co.uk/sh/lst/drafts",,,,,,,,,,
#INFO,,,,,,,,,,
Action(SiteID=UK|Country=GB|Currency=GBP|Version=1193|CC=UTF-8),Custom label (SKU),Category ID,Title,UPC,Price,Quantity,Item photo URL,Condition ID,Description,Format,Duration,Start price,{",".join(f"C:{s}" for s in get_all_specifics())}
"""
    file_name =f"out_{time_util.get_timestamp()}.csv"
    out_path = os.path.join("out", file_name)
    with open(out_path, "w") as f:
        f.write(f"{CSV_HEADER}\n")
        f.writelines(f"{item.to_csv_row()}\n" for item in ebay_items)


if __name__ == "__main__":
    print(get_image_urls_for_item(Path("images/1")))
