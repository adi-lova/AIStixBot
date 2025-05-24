from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def style_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Аниме"), KeyboardButton(text="Реализм")],
            [KeyboardButton(text="Чиби"), KeyboardButton(text="Фэнтези")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def background_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="С фоном"), KeyboardButton(text="Без фона")]
        ],
        resize_keyboard=True
    )

def quantity_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1"), KeyboardButton(text="3"), KeyboardButton(text="5")]
        ],
        resize_keyboard=True
    )
