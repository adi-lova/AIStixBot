from aiogram import Router, types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from bot.keyboards.filters import style_keyboard, background_keyboard, quantity_keyboard
from bot.services.colab_integration import generate_sticker
from bot.handlers.states import StickerGeneration
from aiogram.types import BufferedInputFile
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",  # Убедитесь, что формат корректен
    datefmt="%Y-%m-%d %H:%M:%S",
)

router = Router()

@router.message(Command("generate"))
async def start_generation(message: types.Message, state: FSMContext):
    await message.answer("Выберите стиль изображения:", reply_markup=style_keyboard())
    await state.set_state(StickerGeneration.select_style)


@router.message(StateFilter(StickerGeneration.select_style))
async def select_style(message: types.Message, state: FSMContext):
    style = message.text.lower()
    if style not in ["аниме", "реализм", "чиби", "фэнтези"]:
        await message.answer("Пожалуйста, выберите стиль из предложенных вариантов.")
        return

    await state.update_data(style=style)
    await message.answer(f"Вы выбрали стиль: {style}. Теперь опишите, что должно быть на изображении.")
    await state.set_state(StickerGeneration.enter_prompt)


@router.message(StateFilter(StickerGeneration.enter_prompt))
async def enter_prompt(message: types.Message, state: FSMContext):
    prompt = message.text
    await state.update_data(prompt=prompt)

    await message.answer("Выберите фон для изображения:", reply_markup=background_keyboard())
    await state.set_state(StickerGeneration.select_background)


@router.message(StateFilter(StickerGeneration.select_background))
async def select_background(message: types.Message, state: FSMContext):
    background = message.text.lower()
    if background not in ["с фоном", "без фона"]:
        await message.answer("Пожалуйста, выберите вариант: 'С фоном' или 'Без фона'.")
        return

    await state.update_data(background=background)
    await message.answer("Сколько стикеров сгенерировать?", reply_markup=quantity_keyboard())
    await state.set_state(StickerGeneration.select_quantity)


@router.message(StateFilter(StickerGeneration.select_quantity))
async def select_quantity(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) not in [1, 3, 5]:
        await message.answer("Пожалуйста, выберите количество: 1, 3 или 5.")
        return

    quantity = int(message.text)
    await state.update_data(quantity=quantity)

    await message.answer("Опишите, что должно быть на стикере:")
    await state.set_state(StickerGeneration.enter_prompt)


@router.message(StateFilter(StickerGeneration.enter_prompt))
async def generate(message: types.Message, state: FSMContext):
    data = await state.get_data()

    style = data.get("style", "аниме")
    background = data.get("background", "с фоном")
    quantity = data.get("quantity", 1)
    prompt = data.get("prompt", "описание отсутствует")

    await message.answer("🧠 Генерирую стикеры...")

    try:
        stickers = generate_sticker(prompt, style, background, quantity)

        for i, sticker in enumerate(stickers):
            file = BufferedInputFile(sticker.getvalue(), filename=f"sticker_{i + 1}.webp")
            await message.answer_photo(photo=file, caption=f"Стиль: {style}\nОписание: {prompt}")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

    await state.clear()