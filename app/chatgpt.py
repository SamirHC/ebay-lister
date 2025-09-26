from dotenv import dotenv_values
from openai import OpenAI, BadRequestError

from app.utils import logger
from app.model import Model


config = dotenv_values(".env")
client = OpenAI(api_key=config["OPENAI_API_KEY"])

MAX_TOKENS = 300
MAX_ATTEMPTS = 10  # No cost associated with BadRequestErrors


def get_chatgpt_4o_response(prompt, image_urls):
    image_url_data = map(
        lambda url: {
            "type": "image_url",
            "image_url": {"url": url},
        },
        image_urls
    )
    content_data = [{"type": "text", "text": prompt}]
    content_data.extend(image_url_data)

    response = None
    count = 0
    while response is None and count < MAX_ATTEMPTS:
        count += 1
        try:
            response = client.chat.completions.create(
                model=Model.GPT_4_O,
                messages=[
                    {"role": "system", "content":  "You are ChatGPT, a large language model."},
                    {"role": "user", "content": content_data},
                ],
                max_tokens=MAX_TOKENS,
            )
        except BadRequestError as e:
            logger.log_response(f"ChatGPT failed to get a response: {e}" )
            if count < MAX_ATTEMPTS:
                logger.log_response(f" Trying again (attempt {count})")
            else:
                logger.log_response(f"Maximum attempts made ({count}). Aborting ChatGPT.")
                raise Exception

    return response.choices[0].message.content
