from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

router = Router()

# Пример стилей, можешь расширить список
STYLE_OPTIONS = [
    ("Аниме", "style_anime"),
    ("Реализм", "style_realism"),
    ("Мультфильм", "style_cartoon"),
    ("3D", "style_3d"),
]

@router.message(commands=["start"])
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=label, callback_data=value)]
            for label, value in STYLE_OPTIONS
        ]
    )
    await message.answer(
        "Привет! Я помогу тебе создать стикеры.\n\nВыбери стиль и отправь описание:",
        reply_markup=keyboard
    )
