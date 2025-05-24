from aiogram.fsm.state import State, StatesGroup

class StickerGeneration(StatesGroup):
    select_style = State()
    enter_prompt = State()
    select_background = State()
    select_quantity = State()