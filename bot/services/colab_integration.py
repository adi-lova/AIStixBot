import requests
from bot.config import load_config

config = load_config(".env")

def generate_sticker(prompt, style, background, quantity):
    payload = {
        "prompt": prompt,
        "style": style,
        "background": background,
        "quantity": quantity
    }
    response = requests.post(f"{config.colab_url}/generate", json=payload)
    return response.json().get("stickers", [])

def photo_to_sticker(file_path):
    payload = {
        "file_path": file_path
    }
    response = requests.post(f"{config.colab_url}/photo_to_sticker", json=payload)
    return response.json().get("sticker")
