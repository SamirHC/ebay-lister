from dotenv import dotenv_values
from openai import OpenAI, BadRequestError

from app.utils import logger
from app.model import Model


config = dotenv_values(".env")
client = OpenAI(api_key=config["OPENAI_API_KEY"])


def get_chatgpt_response(prompt: str, image_urls: list[str]) -> str:
    content = [{"type": "input_text", "text": prompt}]
    content.extend({"type": "input_image", "image_url": image_url} for image_url in image_urls)
    try:
        response = client.responses.create(
            model=Model.GPT_5,
            input=[{"role": "user", "content": content}]
        )
    except BadRequestError as e:
        logger.log_response(f"ChatGPT failed to get a response: {e}")
        raise
    else:
        return response.output_text
