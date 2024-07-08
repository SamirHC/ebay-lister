from __future__ import annotations
import os
import csv

id_to_specifics = {}

with open(os.path.join("Ebay Categories & Specifics.csv"), mode='r') as f:
    csv_reader = csv.reader(f)
    next(csv_reader)  # Skip header
    for row in csv_reader:
        id, specifics = str(row[1]), [f"C:{x.strip()}" for x in row[2].split(",")]
        id_to_specifics[id] = specifics

all_specifics = list(set(item for sublist in id_to_specifics.values() for item in sublist))

# Action(SiteID=UK|Country=GB|Currency=GBP|Version=1193|CC=UTF-8),Custom label (SKU),Category ID,Title,UPC,Price,Quantity,Item photo URL,Condition ID,Description,Format

class EbayItem:
    def __init__(
        self,
        action="Draft",  # Default
        SKU="",  # Manual
        category_id="",
        title="",
        UPC="",  # Leave Blank
        price="11.95",  # Default
        quantity=1,  # Default
        image_URL="",
        condition_id="USED",  # Manual
        description="",
        format="",  # Leave Blank
        item_specifics=None
    ):
        self.action = action
        self.SKU = SKU
        self.category_id = category_id
        self.title = title
        self.UPC = UPC
        self.price = price
        self.quantity = quantity
        self.image_URL = image_URL
        self.condition_id = condition_id
        self.description = description
        self.format = format
        self.item_specifics=item_specifics

    def map_item_specifics(self):
        mapped = {s:"" for s in all_specifics}

        cat_specifics = id_to_specifics[self.category_id]

        for cs, it in zip(cat_specifics, self.item_specifics):
            mapped[cs] = it
        
        res = ",".join(mapped[s] for s in all_specifics)
        return res


    def to_csv_row(self):
        return ",".join(map(str, [
            self.action,
            self.SKU,
            self.category_id,
            self.title,
            self.UPC,
            self.price,
            self.quantity,
            self.image_URL,
            self.condition_id,
            self.description,
            self.format,
            self.map_item_specifics()
        ]))


class EbayItemBuilder:
    def __init__(self, image_urls: list[str]):
        self.image_urls = image_urls

        self.title = ""
        self.description = ""
        self.category_id = ""
        self.item_specifics = None

    def set_title(self, title: str) -> EbayItemBuilder: 
        self.title = title
        return self
    
    def set_description(self, description: str) -> EbayItemBuilder:
        self.description = description
        return self
    
    def set_category_id(self, category_id: str) -> EbayItemBuilder:
        self.category_id = category_id
        return self
    
    def set_item_specifics(self, item_specifics: list[str]) -> EbayItemBuilder:
        self.item_specifics = item_specifics
        return self
    
    def format_image_urls(self):
        return "|".join(self.image_urls)

    def build(self) -> EbayItem:
        return EbayItem(
            title=self.title,
            description=self.description,
            category_id=self.category_id,
            image_URL=self.format_image_urls(),
            item_specifics=self.item_specifics
        )
