from aiogram import Router, types
from PIL import Image
from io import BytesIO
import requests
from bot.config import load_config

router = Router()

config = load_config(".env")
colab_url = config.colab_url

@router.message(lambda message: message.photo)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_path = file.file_path
    await message.answer("Обрабатываю фото...")

    # Загрузка изображения
    image_data = await message.bot.download_file(file_path)
    input_image = Image.open(BytesIO(image_data))

    # Удаление фона через Colab
    response = requests.post(f"{colab_url}/remove_bg", files={"image": image_data})
    if response.status_code != 200:
        raise RuntimeError(f"Ошибка удаления фона: {response.status_code}\n    Тело ответа: {response.text}")
    
    output_image_data = response.content
    output_image = Image.open(BytesIO(output_image_data))

    # Сохранение результата
    bio = BytesIO()
    output_image.save(bio, format="PNG")
    bio.seek(0)

    await message.answer_photo(photo=bio, caption="Вот ваш стикер без фона!")