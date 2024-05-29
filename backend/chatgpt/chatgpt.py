from openai import OpenAI
from dotenv import dotenv_values
from model import Model, SystemMessage

config = dotenv_values(".env")
client = OpenAI(api_key=config["OPENAI_API_KEY"])

MAX_TOKENS = 300


def get_chatgpt_4o_response(prompt, base64_image, system_msg=SystemMessage.DEFAULT):
    response = client.chat.completions.create(
        model=Model.GPT_4_O,
        messages=[
            {"role": "system", "content": system_msg},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}",
                        },
                    },
                ],
            },
        ],
        max_tokens=MAX_TOKENS,
    )
    return response["choices"][0]["message"]["content"]
