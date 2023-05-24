import logging

from aiogram import Dispatcher
from aiogram.types import Message


async def notify(dp: Dispatcher):
    config = dp.bot.get("config")
    for admin in config.tg_bot.admins:
        try:
            await dp.bot.send_message(admin, "Bot is running")
        except Exception as error:
            logging.exception(error)
async def admin_reply(message: Message):
    await message.reply("Admin indeed.")

def register_admins(dp: Dispatcher):
    dp.register_message_handler(admin_reply, commands=['admin'], is_admin=True)