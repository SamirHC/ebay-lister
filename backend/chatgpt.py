from openai import OpenAI
from dotenv import dotenv_values
from model import Model, SystemMessage
import os
import datetime

config = dotenv_values(".env")
client = OpenAI(api_key=config["OPENAI_API_KEY"])

MAX_TOKENS = 300


def log_response(response):
    with open(os.path.join(os.getcwd(), "log.txt"), 'a') as file:
        file.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        file.write("\n")
        file.write(str(response))
        file.write("\n")


def get_chatgpt_4o_response(
        prompt, image_urls, system_msg=SystemMessage.DEFAULT
):
    image_url_data = map(
        lambda url: {
            "type": "image_url",
            "image_url": {"url": url,},
        },
        image_urls
    )
    content_data = [{"type": "text", "text": prompt}]
    content_data.extend(image_url_data)

    response = client.chat.completions.create(
        model=Model.GPT_4_O,
        messages=[
            {"role": "system", "content": system_msg},
            {
                "role": "user",
                "content": content_data,
            },
        ],
        max_tokens=MAX_TOKENS,
    )

    log_response(response)
    return response
