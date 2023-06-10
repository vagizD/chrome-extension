import logging
from aiogram import Dispatcher
from .utils import registered, notify_unregistered
from aiogram.utils.exceptions import MessageCantBeEdited
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from .keyboards import users_kb

async def to_menu(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await open_menu(call.message, state)
async def start(message: Message):
    reply = [
        f"<b>Приветствую, {message.from_user.first_name}!</b> 👋",
        f"Информация о боте.",
        f"Перед использованием нужно зарегистрироваться. Инструкция"
    ]
    await message.answer("\n\n".join(reply), reply_markup=users_kb.check_registry)

async def check_registry(call: CallbackQuery, state: FSMContext):
    if not await registered(call.bot, call.from_user.username):
        await notify_unregistered(call)
    else:
        await open_menu(call.message, state)

async def open_menu(message: Message, state: FSMContext):
    await state.finish()
    try:
        await message.edit_text("Выберите, что вы хотите?", reply_markup=users_kb.menu_choice)
    except MessageCantBeEdited:
        await message.answer("Выберите, что вы хотите?", reply_markup=users_kb.menu_choice)
    except Exception as ex:
        logging.info(ex)

async def open_stats(call: CallbackQuery):
    if not await registered(call.bot, call.from_user.username):
        await notify_unregistered(call)
    else:
        database = call.bot.get("database")
        trained = await database.count_user_trained_words(tg_tag=call.from_user.username)
        not_trained = await database.count_user_not_trained_words(tg_tag=call.from_user.username)
        reply = [
            f"За все время Вы добавили <b>{trained + not_trained}</b> слов/слова!",
            f"Из них Вы уже успели выучить <b>{trained}</b> слов/слова.",
            f"Вам предстоит еще выучить {not_trained} слов/слова."
        ]
        await call.message.edit_text("\n\n".join(reply), reply_markup=users_kb.to_menu)

async def open_help(call: CallbackQuery):
    await call.message.edit_text("Какая-то информация / Контакты", reply_markup=users_kb.to_menu)
async def add_word(message: Message, state: FSMContext): # TODO: REMOVE
    await message.answer("Введите слово и перевод через пробел. Ex: apple яблоко")
    await state.set_state("get_word")

async def add_word_execute(message: Message, state: FSMContext): # TODO: REMOVE
    db = message.bot.get("database")
    user = await db.get_user(tg_tag=message.from_user.username)
    if user is None:
        await message.answer("Вы не зареганы")
    else:
        items = message.text.split(' ')
        await db.add_word(message.from_user.username, items[0], items[1])
        await message.answer("Слово добавлено")
    await state.finish()

def register_users(dp: Dispatcher):
    dp.register_callback_query_handler(to_menu, lambda call: call.data == "to_menu")
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_message_handler(open_menu, commands=["menu"], state="*")
    dp.register_callback_query_handler(open_stats, lambda call: call.data == "stats")
    dp.register_callback_query_handler(check_registry, lambda call: call.data == "check_registry")
    dp.register_callback_query_handler(open_help, lambda call: call.data == "help")
    dp.register_message_handler(add_word, commands=['add_word'], state='*')
    dp.register_message_handler(add_word_execute, state='get_word')