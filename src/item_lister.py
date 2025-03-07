import os
import image_handler
import chatgpt
import model
import ebay_item
import logger
import concurrent.futures


MAX_ATTEMPTS = 5
PARALLEL = True
MAX_WORKERS = 20


def main():
    subdirs = get_subdirs()

    logger.log_response("Started uploading images.")

    image_urls = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_subdir = {executor.submit(get_image_urls, s): s for s in subdirs}
        for future in concurrent.futures.as_completed(future_to_subdir):
            s = future_to_subdir[future]
            image_urls[s] = future.result()

    logger.log_response("Finished uploading images.")
    logger.log_response("")

    csv_line_getter = get_csv_lines_parallel if PARALLEL else get_csv_lines
    lines = csv_line_getter(image_urls)

    write_items_to_csv(lines)


def get_subdirs():
    return [
        entry
        for entry in os.listdir(image_handler.IMAGE_DIR)
        if os.path.isdir(os.path.join(image_handler.IMAGE_DIR, entry))
    ]


def get_image_urls(subdir):
    abs_path = os.path.join(image_handler.IMAGE_DIR, subdir)

    image_urls = []
    for file in sorted(filter(image_handler.is_image_path, os.listdir(abs_path))):
        image_handler.upload_image(subdir, file)
        image_urls.append(image_handler.get_public_url(subdir, file))

    return image_urls


def get_csv_lines(image_urls: dict[str, list[str]]):
    NUM_SUBDIRS = len(image_urls)
    res = []

    for i, s in enumerate(image_urls):
        logger.log_response(
            f"Progress:  {i}/{NUM_SUBDIRS} ({round(100 * i/NUM_SUBDIRS)}%)"
        )
        res.append((s, try_get_csv_line(s, image_urls.get(s))))
    res.sort()

    logger.log_response("")
    logger.log_response(f"Progress: {NUM_SUBDIRS}/{NUM_SUBDIRS} (100%)")
    logger.log_response(f"Failed jobs: {[s for s,r in res if r is None]}")
    logger.log_response("")

    return [r for _, r in res if r is not None]


def get_csv_lines_parallel(image_urls: dict[str, list[str]]):
    NUM_SUBDIRS = len(image_urls)
    res = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_subdir = {executor.submit(try_get_csv_line, s, urls): s for s, urls in image_urls.items()}
        for future in concurrent.futures.as_completed(future_to_subdir):
            s = future_to_subdir[future]
            res.append((s, future.result()))
    
    res.sort()

    logger.log_response("")
    logger.log_response(f"Progress: {NUM_SUBDIRS}/{NUM_SUBDIRS} (100%)")
    logger.log_response(f"Failed jobs: {[s for s,r in res if r is None]}")
    logger.log_response("")

    return [r for _, r in res if r is not None]


def try_get_csv_line(s: str, subdir_image_urls: list[str]):
    line = None
    count = 0
    while line is None and count < MAX_ATTEMPTS:
        count += 1
        try:
            line = get_csv_line(subdir_image_urls)
        except Exception as e:
            logger.log_response(
                f"Something went wrong when getting the csv line for item {s}: {e}"
            )
            if count < MAX_ATTEMPTS:
                logger.log_response(f"Trying again (attempt {count}) for item {s}")
            else:
                logger.log_response(f"Maximum attempts made ({count}) for item {s}")
    return line


def get_csv_line(image_urls):
    image_info = query_image_info(image_urls)
    if "\n" in image_info:
        raise Exception("Aborting: Detected newline.")
    elif image_info[0] == '"':
        raise Exception("Aborting: Detected starting speech marks.")
    image_info = [item.strip() for item in image_info.split(",")]

    title = image_info[0]

    try:
        category_id = str(int(image_info[1]))
    except:
        raise Exception(
            "Aborting: Non-integer category ID (Possibly due to comma in title)"
        )

    item_specifics = image_info[2:]

    item = (
        ebay_item.EbayItemBuilder(image_urls)
        .set_title(title)
        .set_description(title)
        .set_category_id(category_id)
        .set_item_specifics(item_specifics)
        .build()
    )  # May raise exception if item_specifics aren't fulfilled

    row = f"{item.to_csv_row()}\n"
    return row


def query_image_info(image_urls):
    response = chatgpt.get_chatgpt_4o_response(model.Prompts.PROMPT, image_urls)
    text = response.choices[0].message.content
    logger.log_response(f"ChatGPT output: {text}")
    return text


CSV_HEADER = f"""
#INFO,Version=0.0.2,Template= eBay-draft-listings-template_GB,,,,,,,,
#INFO Action and Category ID are required fields. 1) Set Action to Draft 2) Please find the category ID for your listings here: https://pages.ebay.com/sellerinformation/news/categorychanges.html,,,,,,,,,,
#INFO After you've successfully uploaded your draft from the Seller Hub Reports tab, complete your drafts to active listings here: https://www.ebay.co.uk/sh/lst/drafts",,,,,,,,,,
#INFO,,,,,,,,,,
Action(SiteID=UK|Country=GB|Currency=GBP|Version=1193|CC=UTF-8),Custom label (SKU),Category ID,Title,UPC,Price,Quantity,Item photo URL,Condition ID,Description,Format,Duration,Start price,{",".join([f"C:{s}" for s in ebay_item.all_specifics])}
"""


def write_items_to_csv(lines):
    with open("out.csv", "w") as f:
        f.write(f"{CSV_HEADER}\n")
        f.writelines(lines)
