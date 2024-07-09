import os
import image_handler
import chatgpt
import model
import ebay_item
import logger


CSV_HEADER = f"""
#INFO,Version=0.0.2,Template= eBay-draft-listings-template_GB,,,,,,,,
#INFO Action and Category ID are required fields. 1) Set Action to Draft 2) Please find the category ID for your listings here: https://pages.ebay.com/sellerinformation/news/categorychanges.html,,,,,,,,,,
"#INFO After you've successfully uploaded your draft from the Seller Hub Reports tab, complete your drafts to active listings here: https://www.ebay.co.uk/sh/lst/drafts",,,,,,,,,,
#INFO,,,,,,,,,,
Action(SiteID=UK|Country=GB|Currency=GBP|Version=1193|CC=UTF-8),Custom label (SKU),Category ID,Title,UPC,Price,Quantity,Item photo URL,Condition ID,Description,Format,Duration,Start price,{",".join(ebay_item.all_specifics)}
"""
MAX_ATTEMPTS = 3


def query_image_info(image_urls):
    response = chatgpt.get_chatgpt_4o_response(model.Prompts.PROMPT, image_urls)
    text = response.choices[0].message.content
    logger.log_response(f"ChatGPT output: {text}")
    return text


def write_items_to_csv():
    lines = get_csv_lines()

    with open("out.csv", "w") as f:
        f.write(f"{CSV_HEADER}\n")
        f.writelines(lines)


def try_get_csv_line(s):
    line = None
    count = 0
    while line is None and count < MAX_ATTEMPTS:
        count += 1
        try:
            line = get_csv_line(s)
        except Exception as e:
            logger.log_response(
                f"Something went wrong when getting the csv line for item {s}: {e}"
            )
            if count < MAX_ATTEMPTS:
                logger.log_response(f"Trying again (attempt {count}) for item {s}")
            else:
                logger.log_response(f"Maximum attempts made ({count}) for item {s}")
    return line


def get_csv_lines():
    subdirs = [
        entry
        for entry in os.listdir(image_handler.IMAGE_DIR)
        if os.path.isdir(os.path.join(image_handler.IMAGE_DIR, entry))
    ]
    subdirs.sort()

    res = []
    for i, s in enumerate(subdirs):
        logger.log_response(
            f"Progress:  {i}/{len(subdirs)} ({round(100 * i/len(subdirs))}%)"
        )
        res.append((s, try_get_csv_line(s)))
    res.sort()

    logger.log_response(f"Progress: {len(subdirs)}/{len(subdirs)} (100%)")
    logger.log_response(f"Failed jobs: {[s for s,r in res if r is None]}")

    return [r for _, r in res if r is not None]


def get_image_urls(subdir):
    abs_path = os.path.join(image_handler.IMAGE_DIR, subdir)

    image_urls = []
    for file in sorted(filter(image_handler.is_image_path, os.listdir(abs_path))):
        rel_path = os.path.join(subdir, file)
        image_handler.upload_image(rel_path)
        image_urls.append(image_handler.get_public_url(rel_path))

    return image_urls


def get_csv_line(subdir):
    image_urls = get_image_urls(subdir)

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
    )

    row = f"{item.to_csv_row()}\n"
    return row
