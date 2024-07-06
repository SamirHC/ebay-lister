# Models
class Model:
    GPT_4_O = "gpt-4o"
    GPT_3_5_TURBO = "gpt-3.5-turbo"


# Customisation
class SystemMessage:
    DEFAULT = "You are ChatGPT, a large language model."


class Prompts:
    TITLE_PROMPT = """
        WRITE AN EBAY UK TITLE FOR THIS ITEM. Take into account what ebay uk 
        category the item is and therefore INCLUDE ANY REQUIRED ITEM SPECIFICS 
        for that category IN THE TITLE. You must make sure that the title does 
        not exceed 80 characters. Refrain from saying what country the item is 
        made in. Just give the answer without speech marks at the beginning and 
        end."""
