from aiogram import types, Dispatcher


async def admin_reply(message: types.Message):
    await message.reply("Admin indeed.")

def register_admins(dp: Dispatcher):
    dp.register_message_handler(admin_reply, commands=['admin'])