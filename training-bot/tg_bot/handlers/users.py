from . import utils
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from .keyboards import main_keyboards

async def back_to_menu(call: CallbackQuery):
    await call.answer()
    await utils.remove_prev_button(call.message)
    await open_menu(call.message)

async def start(message: Message): # Приветственная функция /start
    reply = [
        f"<b>Приветствую, {message.from_user.first_name}!</b> 👋",
        f"Информация о боте.",
        f"Перед использованием нужно зарегистрироваться. Инструкция"
    ]
    await message.answer("\n\n".join(reply), reply_markup=main_keyboards.check_register_keyboard)

async def check_register(call: CallbackQuery): # Регистрация
    await call.answer()
    await utils.remove_prev_button(call.message)
    if not await utils.registered(call.bot.get("database"), call.from_user.id):
        await utils.notify_unregistered(call.message)
    else:
        await open_menu(call.message)

async def open_menu(message: Message): # Панель меню /menu
    await message.answer("Что делаем сегодня?", reply_markup=main_keyboards.menu_keyboard)

async def open_stats(call: CallbackQuery): # Открывает статистику выученных слов
    await call.answer()
    await utils.remove_prev_button(call.message)
    db = call.bot.get("database")
    user = await db.get_user(tg_id=call.from_user.id)
    trained_cnt = await db.count_user_trained_words(owner_id=user.get("user_id"))
    not_trained_cnt = await db.count_user_not_trained_words(owner_id=user.get("user_id"))
    reply = [
        f"За все время Вы добавили <b>{trained_cnt + not_trained_cnt}</b> слов/слова!",
        f"Из них Вы уже успели выучить <b>{trained_cnt}</b> слов/слова.",
        f"Вам предстоит еще выучить {not_trained_cnt} слов/слова."
    ]
    await call.message.answer("\n\n".join(reply), reply_markup=main_keyboards.back_to_menu_keyboard)

async def open_help(call: CallbackQuery): # Открывает раздел помощи/контактов
    await call.answer()
    await utils.remove_prev_button(call.message)
    await call.message.answer("Какая-то информация / Контакты", reply_markup=main_keyboards.back_to_menu_keyboard)

async def add_word(message: Message, state: FSMContext):
    await message.answer("Введите слово и перевод через пробел. Ex: apple яблоко")
    await state.set_state("get_word")

async def add_word_execute(message: Message, state: FSMContext):
    db = message.bot.get("database")
    tg_id = await db.get_user(tg_id=message.from_id)
    if tg_id is None:
        await message.answer("Вы не зареганы")
    else:
        items = message.text.split(' ')
        await db.add_word(tg_id.get("user_id"), items[0], items[1])
        await message.answer("Слово добавлено")
    await state.finish()

def register_users(dp: Dispatcher):
    dp.register_callback_query_handler(back_to_menu, lambda call: call.data == "back_to_menu")
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_message_handler(open_menu, commands=["menu"], state="*")
    dp.register_callback_query_handler(open_stats, lambda call: call.data == "stats")
    dp.register_callback_query_handler(check_register, lambda call: call.data == "check_register")
    dp.register_callback_query_handler(open_help, lambda call: call.data == "help")
    dp.register_message_handler(add_word, commands=['add_word'], state='*')
    dp.register_message_handler(add_word_execute, state='get_word')