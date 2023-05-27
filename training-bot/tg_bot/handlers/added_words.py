from . import utils
from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from .keyboards import added_words_keyboards


async def back_to_choice(call: CallbackQuery):
    await call.answer()
    print("OK")
    await utils.remove_prev_button(call.message)
    await call.message.answer("Выберите нужный тип слов", reply_markup=added_words_keyboards.words_type_choice_keyboard)


async def open_words(call: CallbackQuery): # Выбор тип показываемых слов
    await call.answer()
    await utils.remove_prev_button(call.message)
    await call.message.answer("Выберите нужный тип слов", reply_markup=added_words_keyboards.words_type_choice_keyboard)


async def show_trained_words(call: CallbackQuery):
    await call.answer()
    await utils.remove_prev_button(call.message)
    db = call.bot.get("database")
    user = await db.get_user(tg_id=call.from_user.id)
    data = await db.get_user_trained_words(owner_id=user.get("user_id"))
    reply = ["Список выученных слов:\n"]
    for row in data:
        reply.append(f"{row.get('word')} -- {row.get('trans')}")
    await call.message.answer("\n".join(reply), reply_markup=added_words_keyboards.back_to_choice_keyboard)


async def show_not_trained_words(call: CallbackQuery):
    await call.answer()
    await utils.remove_prev_button(call.message)
    db = call.bot.get("database")
    user = await db.get_user(tg_id=call.from_user.id)
    data = await db.get_user_not_trained_words(owner_id=user.get("user_id"))
    reply = ["Список выученных слов:\n"]
    for row in data:
        reply.append(f"{row.get('word')} -- {row.get('trans')}")
    await call.message.answer("\n".join(reply), reply_markup=added_words_keyboards.back_to_choice_keyboard)


def register_added_words(dp: Dispatcher):
    dp.register_callback_query_handler(open_words, lambda call: call.data == "words")
    dp.register_callback_query_handler(back_to_choice, lambda call: call.data == "back_to_choice")
    dp.register_callback_query_handler(show_trained_words, lambda call: call.data == "trained_words")
    dp.register_callback_query_handler(show_not_trained_words, lambda call: call.data == "not_trained_words")