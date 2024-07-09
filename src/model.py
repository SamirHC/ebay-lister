# Models
class Model:
    GPT_4_O = "gpt-4o"
    GPT_3_5_TURBO = "gpt-3.5-turbo"


# Customisation
class SystemMessage:
    DEFAULT = "You are ChatGPT, a large language model."


class Prompts:
    def get_ebay_csv():
        import os

        with open(
            os.path.join(os.getcwd(), "src", "Ebay Categories & Specifics.csv"), "r"
        ) as f:
            lines = f.readlines()
        return "".join(lines)

    PROMPT = f"""
        DO NOT USE NEW LINES ANYWHERE IN YOUR ANSWER.
        WRITE AN EBAY UK TITLE FOR THIS ITEM. Take into account what ebay uk 
        category the item is and therefore INCLUDE ANY REQUIRED ITEM SPECIFICS 
        for that category IN THE TITLE. You must make sure that the title does 
        not exceed 80 characters. Refrain from saying what country the item is 
        made in. DO NOT INCLUDE COMMAS IN THE TITLE. Then on a new line, tell me the ID that best corresponds to the
        images provided by using the csv file, as well as filling in the item 
        specific information. GIVE THE ANSWERS ONLY SEPARATED BY COMMAS AND WITHOUT SPEECH MARKS. Make sure that
        the order of the information is preserved: Title, ID, Item specifics... WRITE THE HEADING OF THE ITEM SPECIFIC IN YOUR ANSWER,
        for example:
        Brand, Adidas, Size, 30, Colour, Brown

        \n{get_ebay_csv()}"""

    FAIL_PROMPT = f"""write a single word describing these images and nothing else"""
