import requests
from io import BytesIO
from PIL import Image
from typing import List


def generate_sticker(prompt: str, style: str, background: str, quantity: int) -> List[BytesIO]:
    stickers = []

    full_prompt = f"{style} {prompt}, centered".strip()
    encoded_prompt = requests.utils.quote(full_prompt)
    url = f"https://image.pollinations.ai/prompt/ {encoded_prompt}?width=512&height=512"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Ошибка при генерации изображения: {e}")

    image = Image.open(BytesIO(response.content))

    if background == "без фона":
        try:
            bg_remove_response = requests.post(
                "https://colab.pollinations.ai/remove_bg ",
                files={"image": BytesIO(response.content)}
            )
            bg_remove_response.raise_for_status()
            image = Image.open(BytesIO(bg_remove_response.content))
        except requests.RequestException as e:
            raise RuntimeError(f"Ошибка удаления фона: {e}")

    for _ in range(quantity):
        bio = BytesIO()
        image.thumbnail((512, 512))  # уменьшаем размер для Telegram
        image.save(bio, format="PNG")
        bio.seek(0)
        stickers.append(bio)

    return stickers