import json
import logging

from aiogram import types

logger = logging.getLogger(__name__)


async def read_file(file_path):
    with open(file=file_path, mode="r", encoding="UTF-8") as file:
        try:
            return json.load(file)
        except:
            return dict()


async def add_to_file(message: types.Message):
    user_id = message.from_user.id
    data = {
        "chat_id": user_id,
        "full_name": message.from_user.full_name,
        "username": message.from_user.username,
        "created_at": str(message.date)
    }
    users: dict = await read_file(file_path="data/users.json")
    users[user_id] = data
    try:
        with open(file='data/users.json', mode='w', encoding='UTF-8') as file:
            json.dump(users, file, indent=4)
    except Exception as e:
        logger.error(msg=str(e))


async def add_to_messages(data: dict):
    messages: dict = await read_file(file_path="data/messages.json")
    user_messages = messages.get(str(data['from_user']), [])
    user_messages.append(data)
    messages[data['from_user']] = user_messages
    try:
        with open(file='data/messages.json', mode='w', encoding='UTF-8') as file:
            json.dump(messages, file, indent=4)
    except Exception as e:
        logger.error(msg=str(e))


async def check_user_id(user_id):
    users: dict = await read_file(file_path='data/users.json')
    return user_id in users.keys()
