from aiogram import Dispatcher
from aiogram.types import Message

async def registered(user_id: int) -> bool:
    users =  [] # find user_id in database
    return user_id in users

async def start(message: Message):
    bot = message.bot
    if await registered(message.from_id):
        message_text = f"Hello, <b>{message.from_user.first_name}!</b>\n\n" \
                       f"What are we going to do today?"
        await bot.send_message(message.chat.id, text=message_text)
    else:
        message_text = f"Hello, <b>{message.from_user.first_name}!</b>\n\n" \
                       f"Your account is <b>not</b> registered yet. Provide your <b><u>username</u></b> in " \
                       f"SubLive config settings please.\n\n" \
                       f"Your current username is @{message.from_user.id}."
        await bot.send_message(message.chat.id, message_text)

def register_users(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])