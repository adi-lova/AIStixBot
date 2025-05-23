from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()

# Клавиатура с фильтрами
def get_filters_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text="🎨 Аниме", callback_data="style_anime"),
            InlineKeyboardButton(text="🖼️ Реализм", callback_data="style_realism"),
        ],
        [
            InlineKeyboardButton(text="1️⃣", callback_data="count_1"),
            InlineKeyboardButton(text="3️⃣", callback_data="count_3"),
            InlineKeyboardButton(text="5️⃣", callback_data="count_5"),
        ],
        [
            InlineKeyboardButton(text="📸 Из фото", callback_data="from_photo"),
            InlineKeyboardButton(text="😊 Эмоции", callback_data="emotions_pack"),
        ],
        [
            InlineKeyboardButton(text="🟩 С фоном", callback_data="with_bg"),
            InlineKeyboardButton(text="⬜ Без фона", callback_data="no_bg"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Обработчик /start
@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Привет! Я помогу тебе создать стикеры.\nВыбери стиль и отправь описание.",
        reply_markup=get_filters_keyboard()
    )
