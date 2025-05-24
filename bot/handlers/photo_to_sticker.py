from aiogram import Router, types
from PIL import Image
from io import BytesIO
import requests

router = Router()


@router.message(lambda message: message.photo)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_path = file.file_path
    await message.answer("Обрабатываю фото...")

    # Скачиваем фото
    image_data = await message.bot.download_file(file_path)
    input_image = Image.open(BytesIO(image_data))

    # Отправляем на удаление фона через Pollinations Colab
    try:
        response = requests.post(
            "https://colab.pollinations.ai/remove_bg ",
            files={"image": image_data}
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Ошибка при удалении фона: {e}")

    # Загружаем результат
    output_image = Image.open(BytesIO(response.content))
    bio = BytesIO()
    output_image.save(bio, format="PNG")
    bio.seek(0)

    await message.answer_photo(photo=bio, caption="Вот ваш стикер без фона!")