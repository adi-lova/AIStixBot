import os
import requests
from dotenv import load_dotenv

load_dotenv()

# URL публичного Inference API для модели
HF_API_URL = "https://api-inference.huggingface.co/models/stable-diffusion-v1-5/stable-diffusion-v1-5"

# Токен обязателен даже для публичных моделей, чтобы не проваливаться в rate limits
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise EnvironmentError("HF_TOKEN не найден в переменных окружения. "
                           "Добавьте HF_TOKEN в .env или в окружение Colab/сервера.")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def generate_sticker(prompt: str, style: str, background: str, quantity: int) -> list[bytes]:
    """
    Генерирует `quantity` стикеров по описанию через Hugging Face Inference API.
    Возвращает список байт-контента PNG-изображений.
    """
    stickers = []
    for i in range(quantity):
        # Собираем полный промпт
        full_prompt = f"{style} sticker, {prompt}, {background}"
        payload = {
            "inputs": full_prompt,
            "options": {"wait_for_model": True},
            "parameters": {
                "num_inference_steps": 30,
                "guidance_scale": 7.5
            }
        }

        response = requests.post(HF_API_URL, headers=HEADERS, json=payload)

        # Если что-то пошло не так — логируем и пропускаем
        if response.status_code != 200:
            print(f"❌ Ошибка Hugging Face API (стикер #{i+1}): {response.status_code}")
            print(f"    Тело ответа: {response.text}")
            continue

        # При удаче Hugging Face отдаёт бинарный PNG
        stickers.append(response.content)

    return stickers

def photo_to_sticker(file_bytes: bytes, style: str, background: str) -> bytes:
    """
    Преобразует фото пользователя (bytes) в стикер.
    Можно использовать ту же модель, передав фото как input,
    либо отдельно вызывать rembg для удаления фона.
    Здесь пример простого конверта без HF:
    """
    # Если хочешь: вызывай тот же API, либо обрезай/меняй размер
    # В этом примере просто возвращаем исходное фото (placeholder)
    return file_bytes
