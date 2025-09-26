from itertools import chain
import os

import pandas as pd


EBAY_CATEGORIES_PATH = os.path.join("data", "Ebay Categories & Specifics.csv")


def get_ebay_categories_df() -> pd.DataFrame:
    df = pd.read_csv(EBAY_CATEGORIES_PATH)
    df["Required Item Specifics"] = df["Required Item Specifics"].apply(
        lambda s: [category.strip() for category in s.split(",")]
    )
    return df

ebay_categories_df = get_ebay_categories_df()
id_to_specifics = dict(zip(ebay_categories_df["ID"], ebay_categories_df["Required Item Specifics"]))
all_specifics = list(set(chain.from_iterable(ebay_categories_df["Required Item Specifics"])))

def get_specifics_from_id(id: int) -> list[str]:
    return id_to_specifics[id]


def get_all_specifics() -> list[str]:
    return all_specifics


if __name__ == "__main__":
    print(ebay_categories_df)
    print()
    print(id_to_specifics)
    print()
    print(all_specifics)
