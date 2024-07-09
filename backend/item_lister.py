import os
import image_handler, chatgpt, model, ebay_item


CSV_HEADER = f"""
#INFO,Version=0.0.2,Template= eBay-draft-listings-template_GB,,,,,,,,
#INFO Action and Category ID are required fields. 1) Set Action to Draft 2) Please find the category ID for your listings here: https://pages.ebay.com/sellerinformation/news/categorychanges.html,,,,,,,,,,
"#INFO After you've successfully uploaded your draft from the Seller Hub Reports tab, complete your drafts to active listings here: https://www.ebay.co.uk/sh/lst/drafts",,,,,,,,,,
#INFO,,,,,,,,,,
Action(SiteID=UK|Country=GB|Currency=GBP|Version=1193|CC=UTF-8),Custom label (SKU),Category ID,Title,UPC,Price,Quantity,Item photo URL,Condition ID,Description,Format,Duration,Start price,{",".join(ebay_item.all_specifics)}
"""


def query_image_info(image_urls):
    response = chatgpt.get_chatgpt_4o_response(
        model.Prompts.PROMPT, image_urls)
    text = response.choices[0].message.content
    print(text)
    return text


def write_items_to_csv():
    lines = get_csv_lines()

    with open("out.csv", "w") as f:
        
        f.write(f"{CSV_HEADER}\n")
        f.writelines(lines)

def get_csv_lines():
    subdirs = [
        entry 
        for entry in os.listdir(image_handler.IMAGE_DIR)
        if os.path.isdir(os.path.join(image_handler.IMAGE_DIR, entry))
    ]

    MAX_COUNT = 3
    res = []

    for subdir in subdirs:
        line = None
        count = 0
        while line is None and count < MAX_COUNT:
            count += 1
            try:
                line = get_csv_line(subdir)
            except Exception:
                print(f"Something went wrong when getting the csv line for item {subdir}.")
                if count < MAX_COUNT:
                    print(f"Trying again (attempt {count})")
                else:
                    print(f"Maximum attempts made ({count}). Terminating early.")
                    # End getting csv lines and write what was able to be retrieved.
                    return res
        
        res.append(line)

    return res


def get_csv_line(subdir):
    abs_path = os.path.join(image_handler.IMAGE_DIR, subdir)

    image_urls = []
    for file in sorted(filter(image_handler.is_image_path, os.listdir(abs_path))):

        rel_path = os.path.join(subdir, file)
        
        image_handler.upload_image(rel_path)
        image_urls.append(image_handler.get_public_url(rel_path))
        
    image_info = query_image_info(image_urls).split(",")
    image_info = [item.strip() for item in image_info]

    title = image_info[0]
    category_id = image_info[1]
    item_specifics = image_info[2:]

    item = (ebay_item.EbayItemBuilder(image_urls)
        .set_title(title)
        .set_description(title)
        .set_category_id(category_id)
        .set_item_specifics(item_specifics)
        .build()
    )

    row = f"{item.to_csv_row()}\n"
    return row

if __name__ == "__main__":
    write_items_to_csv()
