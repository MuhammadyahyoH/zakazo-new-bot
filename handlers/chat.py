from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext

from states import ChatState
from utils import add_to_messages, check_user_id, read_file

router = Router()


@router.message(F.text == '✍️ Send message')
async def send_message_handler(message: types.Message, state: FSMContext):
    text = "🆔 Please, enter user id"
    await message.answer(text=text)
    await state.set_state(ChatState.user_id)


@router.message(ChatState.user_id)
async def get_user_id_handler(message: types.Message, state: FSMContext):
    user_id = message.text
    if await check_user_id(user_id):
        await state.update_data(user_id=user_id)
        text = "📝 Please enter your message"
        await state.set_state(ChatState.message)
    else:
        text = "😔 User does not found in my database"
    await message.answer(text=text)


@router.message(ChatState.message)
async def get_message_handler(message: types.Message, state: FSMContext, bot: Bot):
    await state.update_data(message=message.text)

    data = await state.get_data()
    data['from_user'] = message.from_user.id
    await add_to_messages(data)

    await bot.send_message(chat_id=data['user_id'], text=data['message'])
    text = "✅ Successfully sent"
    await message.answer(text=text)
    await state.clear()


@router.message(F.text == '📝 My messages')
async def my_messages_handler(message: types.Message, state: FSMContext):
    messages: dict = await read_file(file_path='data/messages.json')

    user_id = str(message.from_user.id)

    if user_id not in messages.keys():
        text = "😁 You do not have any messages yet"
        await message.answer(text=text)
    else:
        user_messages = messages.get(user_id)
        for user_message in user_messages:
            text = f"User: {user_message['user_id']} | {user_message['message']}"
            await message.answer(text=text)
