import os
import image_encoder, chatgpt, model, ebay_item


IMAGE_DIR = os.path.join(os.getcwd(), "images")
CSV_HEADER = """
#INFO,Version=0.0.2,Template= eBay-draft-listings-template_GB,,,,,,,,
#INFO Action and Category ID are required fields. 1) Set Action to Draft 2) Please find the category ID for your listings here: https://pages.ebay.com/sellerinformation/news/categorychanges.html,,,,,,,,,,
"#INFO After you've successfully uploaded your draft from the Seller Hub Reports tab, complete your drafts to active listings here: https://www.ebay.co.uk/sh/lst/drafts",,,,,,,,,,
#INFO,,,,,,,,,,
Action(SiteID=UK|Country=GB|Currency=GBP|Version=1193|CC=UTF-8),Custom label (SKU),Category ID,Title,UPC,Price,Quantity,Item photo URL,Condition ID,Description,Format
"""
TEST_IMAGE_URL = "https://ir.ebaystatic.com/cr/v/c1/rsc/ebay_logo_512.png"

def is_image_path(path):
    return path.endswith(".png") or path.endswith(".jpeg")

def query_title_from_image(path: str):
    if not is_image_path(path):
        return
    print(path)
    base64_image = image_encoder.encode_image(path)
    response = chatgpt.get_chatgpt_4o_response(model.Prompts.TITLE_PROMPT, base64_image)
    text = response.choices[0].message.content
    print(text)
    return text


def write_items_to_csv(path):
    with open("out.csv", "w") as f:
        
        f.write(f"{CSV_HEADER}\n")
        
        for filepath in os.listdir(path):
            image_path = os.path.join(path, filepath)
            if not is_image_path(image_path):
                continue

            title = query_title_from_image(image_path)
            
            item = (ebay_item.EbayItemBuilder(image_path)
                .set_title(title)
                .set_description(title)
                .set_category_id("11450")
                .set_image_url(TEST_IMAGE_URL)
                .build()
            )

            row = f"{item.to_csv_row()}\n"
            f.write(row)
            print(row)


if __name__ == "__main__":
    write_items_to_csv(IMAGE_DIR)
