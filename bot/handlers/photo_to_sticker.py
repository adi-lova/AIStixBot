from aiogram import Router, types
from bot.services.colab_integration import photo_to_sticker

router = Router()

@router.message(lambda message: message.photo)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_path = file.file_path
    await message.answer("Обрабатываю фото...")

    sticker = photo_to_sticker(file_path)

    await message.answer_photo(photo=sticker)
