from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👀 Show all products"),
            KeyboardButton(text="📝Add new product"),
        ],
        [
            KeyboardButton(text="🗑️ Delete product"),
            KeyboardButton(text="📅 Show today's menu"),
        ],
        [
            KeyboardButton(text="➕ Add product to today's menu"),
            KeyboardButton(text="🗑️ Remove product from today's menu"),
        ],
    ], resize_keyboard=True
)
