python
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from bot.keyboards.filters import style_keyboard, background_keyboard, quantity_keyboard
from bot.services.colab_integration import generate_sticker
from bot.config import load_config

router = Router()

config = load_config(".env")
colab_url = config.colab_url

@router.message(lambda message: message.text.lower() in ["аниме", "реализм", "чиби"])
async def select_style(message: types.Message, state: FSMContext):
    await state.update_data(style=message.text.lower())
    await message.answer("Выбери фон:", reply_markup=background_keyboard())

@router.message(lambda message: message.text.lower() in ["с фоном", "без фона"])
async def select_background(message: types.Message, state: FSMContext):
    await state.update_data(background=message.text.lower())
    await message.answer("Сколько стикеров сгенерировать?", reply_markup=quantity_keyboard())

@router.message(lambda message: message.text.isdigit())
async def select_quantity(message: types.Message, state: FSMContext):
    await state.update_data(quantity=int(message.text))
    await message.answer("Опиши, что должно быть на стикере:")

@router.message()
async def generate(message: types.Message, state: FSMContext):
    data = await state.get_data()
    style = data.get("style")
    background = data.get("background")
    quantity = data.get("quantity", 1)
    prompt = message.text

    await message.answer("Генерирую стикеры, подождите...")
    
    try:
        stickers = generate_sticker(prompt, style, background, quantity, colab_url)
        for sticker in stickers:
            await message.answer_photo(photo=sticker)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")