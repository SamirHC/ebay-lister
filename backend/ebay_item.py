from __future__ import annotations

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

    def to_csv_row(self):
        return ",".join([
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
            self.format
        ])


class EbayItemBuilder:
    def __init__(self, image_urls: list[str]):
        self.image_urls = image_urls

        self.title = ""
        self.description = ""
        self.category_id = ""

    def set_title(self, title: str) -> EbayItemBuilder: 
        self.title = title
        return self
    
    def set_description(self, description: str) -> EbayItemBuilder:
        self.description = description
        return self
    
    def set_category_id(self, category_id: str) -> EbayItemBuilder:
        self.category_id = category_id
        return self
    
    def format_image_urls(self):
        return "|".join(self.image_urls)

    def build(self) -> EbayItem:
        return EbayItem(
            title=self.title,
            description=self.description,
            category_id=self.category_id,
            image_URL=self.format_image_urls()
        )
