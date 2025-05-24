import requests
from PIL import Image
from io import BytesIO

def generate_sticker(prompt: str, style: str, background: str, quantity: int, colab_url: str) -> list[BytesIO]:
    """
    Генерация стикеров с использованием Colab API.

    Аргументы:
    prompt (str): Текстовый запрос для генерации изображения.
    style (str): Стиль изображения.
    background (str): Тип фона ("с фоном" или "без фона").
    quantity (int): Количество стикеров для генерации.
    colab_url (str): URL для Colab API.

    Возвращает:
    list[BytesIO]: Список сгенерированных изображений в формате BytesIO.
    """
    stickers = []
    for i in range(quantity):
        full_prompt = f"{style} {prompt}, centered"
        if background == "с фоном":
            full_prompt += ", white background"
        
        try:
            response = requests.post(f"{colab_url}/generate", json={"prompt": full_prompt})
            response.raise_for_status()  # Проверка на успешный статус-код
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к Colab API: {e}")
            print(f"Статус код: {e.response.status_code if e.response else 'Нет ответа'}")
            print(f"Текст ответа: {e.response.text if e.response else 'Нет ответа'}")
            raise RuntimeError(f"Ошибка Colab API (стикер #{i+1}): {e}")
        
        image_data = response.content
        image = Image.open(BytesIO(image_data))
        
        if background == "без фона":
            try:
                response = requests.post(f"{colab_url}/remove_bg", files={"image": image_data})
                response.raise_for_status()  # Проверка на успешный статус-код
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при запросе к Colab API: {e}")
                print(f"Статус код: {e.response.status_code if e.response else 'Нет ответа'}")
                print(f"Текст ответа: {e.response.text if e.response else 'Нет ответа'}")
                raise RuntimeError(f"Ошибка удаления фона (стикер #{i+1}): {e}")
            image_data = response.content
            image = Image.open(BytesIO(image_data))
        
        bio = BytesIO()
        image.save(bio, format="PNG")
        bio.seek(0)
        stickers.append(bio)
    
    return stickers