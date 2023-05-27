import logging
from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

async def notify(dp: Dispatcher):
    config = dp.bot.get("config")
    for admin in config.tg_bot.admins:
        try:
            await dp.bot.send_message(admin, "Bot is running")
        except Exception as error:
            logging.exception(error)

async def admin_reply(message: Message):
    await message.answer("Admin indeed.")

async def admin_add_user(message: Message, state: FSMContext):
    await message.answer("Введите айди пользователя:")
    await state.set_state("admin_add")

async def admin_add_user_execute(message: Message, state: FSMContext):
    db = message.bot.get("database")
    await db.add_user(gmail="something", tg_id=int(message.text))
    await message.answer("Пользователь добавлен")
    await state.finish()

def register_admins(dp: Dispatcher):
    dp.register_message_handler(admin_reply, state='*', commands=['admin'], is_admin=True)
    dp.register_message_handler(admin_add_user, state='*', commands=['add'], is_admin=True)
    dp.register_message_handler(admin_add_user_execute, state='admin_add')
