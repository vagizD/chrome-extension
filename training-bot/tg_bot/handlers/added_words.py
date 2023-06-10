from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from .keyboards import added_words_kb
from .utils import registered, notify_unregistered

async def to_words_choice(call: CallbackQuery):
    await call.message.edit_text("Выберите нужный тип слов", reply_markup=added_words_kb.words_choice)

async def open_words(call: CallbackQuery):
    if not await registered(call.bot, call.from_user.username):
        await notify_unregistered(call)
    else:
        await call.message.edit_text("Выберите нужный тип слов", reply_markup=added_words_kb.words_choice)

async def show_trained_words(call: CallbackQuery):
    data = await call.bot.get("database").get_user_trained_words(tg_tag=call.from_user.username)
    if len(data) == 0:
        reply = ["У вас нет выученных слов"]
    else:
        reply = [f"{row.get('word')} -- {row.get('trans')}" for row in data]
    await call.message.edit_text("\n".join(reply), reply_markup=added_words_kb.to_words_choice)

async def show_not_trained_words(call: CallbackQuery):
    data = await call.bot.get("database").get_user_not_trained_words(tg_tag=call.from_user.username)
    if len(data) == 0:
        reply = ["У вас нет невыученных слов"]
    else:
        reply = [f"{row.get('word')} -- {row.get('trans')}" for row in data]
    await call.message.edit_text("\n".join(reply), reply_markup=added_words_kb.to_words_choice)

def register_added_words(dp: Dispatcher):
    dp.register_callback_query_handler(open_words, lambda call: call.data == "words")
    dp.register_callback_query_handler(to_words_choice, lambda call: call.data == "to_words_choice")
    dp.register_callback_query_handler(show_trained_words, lambda call: call.data == "trained")
    dp.register_callback_query_handler(show_not_trained_words, lambda call: call.data == "not_trained")