from __future__ import annotations
import csv
import os


id_to_specifics = {}

with open(os.path.join("data", "Ebay Categories & Specifics.csv"), mode="r") as f:
    csv_reader = csv.reader(f)
    next(csv_reader)  # Skip header
    for row in csv_reader:
        id = str(row[1])
        specifics = [x.strip() for x in row[2].split(",")]
        id_to_specifics[id] = specifics

all_specifics = list(
    set(item for sublist in id_to_specifics.values() for item in sublist)
)


class EbayItem:
    def __init__(
        self,
        action="Draft",  # Default
        SKU="",  # Manual
        category_id="",
        title="",
        UPC="",  # Leave Blank
        price="",  # Leave Blank
        quantity="",  # Default
        image_URL="",
        condition_id="USED",  # Manual
        description="",
        format="Auction",  # Defualt
        duration=7,  # Default
        start_price="11.99",  # Default
        item_specifics=None,
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
        self.duration = duration
        self.start_price = start_price
        self.item_specifics = item_specifics

    def to_csv_row(self):
        return ",".join(
            map(
                str,
                [
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
                    self.duration,
                    self.start_price,
                    self.item_specifics,
                ],
            )
        )


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
        mapped = {s: "" for s in all_specifics}

        while item_specifics:
            v = item_specifics.pop().title()
            k = item_specifics.pop().title()
            if k not in mapped:
                if k == "Number Of Pieces":
                    k = "Number of Pieces"
                elif k == "Uk Shoe Size":
                    k = "UK Shoe Size"
                else:
                    raise Exception(f"UNKNOWN CATEGORY: Could not parse {k}")
            mapped[k] = v

        for s in id_to_specifics[self.category_id]:
            if not mapped[s]:
                raise Exception(f"{s} is not provided.")

        self.check_title_for_category("Brand", item_specifics, mapped)

        self.item_specifics = ",".join(mapped[s] for s in all_specifics)
        return self
    
    def check_title_for_category(self, category: str, item_specifics, mapped):
        if category in item_specifics and mapped[category] not in self.title:
            raise Exception(f"Title does not include {category}.")

    def format_image_urls(self):
        return "|".join(self.image_urls)

    def build(self) -> EbayItem:
        return EbayItem(
            title=self.title,
            description=self.description,
            category_id=self.category_id,
            image_URL=self.format_image_urls(),
            item_specifics=self.item_specifics,
        )
