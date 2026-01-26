from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✍️ Send message"),
            KeyboardButton(text="📝 My messages"),
        ]
    ], resize_keyboard=True
)
