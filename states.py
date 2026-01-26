from aiogram.fsm.state import StatesGroup, State


class ChatState(StatesGroup):
    user_id = State()
    message = State()
    confirmation = State()
