import logging
from io import BytesIO
from PIL import Image
from urllib.parse import quote
import requests

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelоmlevelname)s - %(message)s")

def generate_sticker(prompt: str, style: str = "", background: str = "с фоном", quantity: int = 1) -> list[BytesIO]:
    # Генерация корректного URL с параметрами для удаления логотипа и приватности
    full_prompt = f"{style} {prompt}".strip()
    encoded_prompt = quote(full_prompt, safe="")
    url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width=512&height=512&nologo=true&private=true"
    )

    logging.info(f"Generated URL: {url}")

    try:
        # Запрос к Pollinations API
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logging.info(f"Pollinations API response status: {response.status_code}")
    except requests.RequestException as e:
        logging.error(f"Pollinations API error: {e}")
        raise RuntimeError(f"Ошибка при запросе к Pollinations API: {e}")

    try:
        # Проверка и обработка изображения
        image = Image.open(BytesIO(response.content)).convert("RGBA")  # WebP поддерживает прозрачность
        logging.info("Image successfully loaded and converted to RGBA.")
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        raise RuntimeError(f"Ошибка обработки изображения: {e}")

    # Удаление фона, если требуется
    if background == "без фона":
        try:
            logging.info("Removing background from image...")
            bg_remove_response = requests.post(
                "https://colab.pollinations.ai/remove_bg",
                files={"image": BytesIO(response.content)}
            )
            bg_remove_response.raise_for_status()
            image = Image.open(BytesIO(bg_remove_response.content)).convert("RGBA")
            logging.info("Background successfully removed.")
        except requests.RequestException as e:
            logging.error(f"Error removing background: {e}")
            raise RuntimeError(f"Ошибка удаления фона: {e}")

    # Генерация нескольких стикеров
    stickers = []
    for i in range(quantity):
        bio = BytesIO()
        image.thumbnail((512, 512), Image.LANCZOS)  # Уменьшаем размер до 512x512
        image.save(bio, format="WEBP", quality=85, optimize=True)  # Сохраняем в WebP с качеством 85
        bio.seek(0)

        # Проверка размера файла
        if bio.getbuffer().nbytes > 5 * 1024 * 1024:  # Лимит 5 МБ
            logging.warning(f"Sticker {i + 1} is too large for Telegram (size: {bio.getbuffer().nbytes} bytes).")
            raise RuntimeError("❌ Изображение слишком большое для Telegram. Попробуйте другой prompt или стиль.")

        stickers.append(bio)
        logging.info(f"Sticker {i + 1} generated successfully.")

    return stickers
