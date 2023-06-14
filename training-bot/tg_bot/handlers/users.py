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
        f"Данный бот поможет Вам учить английский эффективней! Вы можете:",
        "• просматривать добавленные расширением слова\n"
        "• отслеживать статистику выученных слов\n"
        "• тренировать запоминание слов в различных режимах",
        f"Перед использованием <u>необходимо зарегистрировать свой телеграм аккаунт</u> в настройках расширения."
    ]
    await message.answer("\n\n".join(reply), reply_markup=users_kb.check_registry)

async def check_registry(call: CallbackQuery, state: FSMContext):
    if not await registered(call.bot, call.from_user.username):
        await notify_unregistered(call)
    else:
        await open_menu(call.message, state)

async def open_menu(message: Message, state: FSMContext):
    await state.finish()
    reply = [
        "Выберите, что вы хотите?",
        "• <b>Тренироваться:</b> выбирайте режимы для тренировки новых добавленных слов, проверяйте свои знания в "
        "быстрых тренировках и не забывайте о главной интервальной тренировке.",
        "• <b>Добавленные слова:</b> просматривайте добавленные изученные и неизученные слова, вспоминайте страницы, "
        "с которых были добавлены эти слова, удаляйте ненужные и лишние слова.",
        "• <b>Просмотреть статистику:</b> следите за количеством уже изученных слов, общим количеством добавленных слов.",
        "• <b>Помощь:</b> контакты для вопросов и оповещения о багах, предложениях."
    ]
    try:
        await message.edit_text(text="\n\n".join(reply), reply_markup=users_kb.menu_choice)
    except MessageCantBeEdited:
        await message.answer(text="\n\n".join(reply), reply_markup=users_kb.menu_choice)
    except Exception as ex:
        logging.info(ex)

async def open_stats(call: CallbackQuery):
    if not await registered(call.bot, call.from_user.username):
        await notify_unregistered(call)
    else:
        database = call.bot.get("database")
        trained = await database.get_count_words(tg_tag=call.from_user.username, trained=True)
        not_trained = await database.get_count_words(tg_tag=call.from_user.username, trained=False)
        reply = [
            f"〩 ➝ Общее количество добавленных слов: {trained + not_trained}",
            f"✓  ➝ Количество успешно выученных слов: {trained}",
            f"✕  ➝ Количество еще не изученных слов: {not_trained}"
        ]
        await call.message.edit_text("\n\n".join(reply), reply_markup=users_kb.to_menu)

async def open_help(call: CallbackQuery):
    reply = [
        "Любые вопросы, предложения и замечания, в том числе и баги, приветствуются в личные сообщения:",
        "⇉   @I8usy_I8eaver\n⇉   @vagizdaudov\n⇉   @perkyfever"
    ]
    await call.message.edit_text(text="\n\n".join(reply), reply_markup=users_kb.to_menu)
async def add_word(message: Message, state: FSMContext):
    await message.answer("Введите слово и перевод через пробел. Ex: apple яблоко")
    await state.set_state("get_word")

async def add_word_execute(message: Message, state: FSMContext):
    db = message.bot.get("database")
    user = await db.get_user(tg_tag=message.from_user.username)
    if user is None:
        await message.answer("Вы не зарегистрированы")
    else:
        items = message.text.split(' ')
        await db.add_word(message.from_user.username, items[0], items[1])
        await message.answer("Слово добавлено")
    await state.finish()

def register_users(dp: Dispatcher):
    dp.register_callback_query_handler(to_menu, lambda call: call.data == "to_menu", state="*")
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_message_handler(open_menu, commands=["menu"], state="*")
    dp.register_callback_query_handler(open_stats, lambda call: call.data == "show_stats")
    dp.register_callback_query_handler(check_registry, lambda call: call.data == "check_registry")
    dp.register_callback_query_handler(open_help, lambda call: call.data == "get_help")
    dp.register_message_handler(add_word, commands=['add_word'], state='*')
    dp.register_message_handler(add_word_execute, state='get_word')