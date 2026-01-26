from aiogram import Router, types
from aiogram.filters import Command

from keyboards.default import user_main_menu
from utils import add_to_file

router = Router()


@router.message(Command('start'))
async def start_handler(message: types.Message):
    await add_to_file(message)
    await message.answer(
        text=f"Salom, {message.from_user.full_name}",
        reply_markup=user_main_menu
    )
