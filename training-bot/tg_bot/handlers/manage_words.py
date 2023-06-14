import logging
from typing import List

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from .keyboards import words_kb
from .utils import registered, notify_unregistered
from .trainings import process_data, Data
from math import ceil

PAGE_SIZE = 6

async def to_words_type_choice(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.finish()
    await call.message.edit_text(text="Выберите тип слов, чтобы посмотреть их список.", reply_markup=words_kb.words_choice)

async def choose_words_type(call: CallbackQuery):
    await call.answer()
    if not await registered(call.bot, call.from_user.username):
        await notify_unregistered(call)
    else:
        await call.message.edit_text(text="Выберите тип слов, чтобы посмотреть их список.", reply_markup=words_kb.words_choice)
async def show_words(call: CallbackQuery, state: FSMContext):
    await call.answer()
    words: List[Data] = []
    if call.data == "not_trained":
        words = await process_data(call.bot, tg_tag=call.from_user.username, trained=False)
    elif call.data == "trained":
        words = await process_data(call.bot, tg_tag=call.from_user.username, trained=True)
    if len(words) == 0 and call.data == "not_trained":
        await call.message.edit_text(text="У Вас нет неизученных слов!", reply_markup=words_kb.to_words_choice)
    elif len(words) == 0 and call.data == "trained":
        await call.message.edit_text(text="У Вас нет изученных слов!", reply_markup=words_kb.to_words_choice)
    else:
        await state.set_state("show_words")
        await state.update_data(cur=0)
        await state.update_data(words=words)
        await state.update_data(max_page=ceil(len(words) / PAGE_SIZE))
        await show_words_page(call, state)

async def show_words_page(call: CallbackQuery, state: FSMContext):
    await call.answer()
    async with state.proxy() as data:
        if call.data == "prev_page":
            data["cur"] -= 1
        if call.data == "next_page":
            data["cur"] += 1
        start = data["cur"] * PAGE_SIZE
        reply: List[str] = []
        for i in range(start, min(start + PAGE_SIZE, len(data["words"]))):
            cur: Data = data["words"][i]
            reply.append(f"◽ {cur.word} ➝ {cur.trans} ➝ <a href='{cur.website}'>Источник</a>")
        await call.message.edit_text(text="\n\n".join(reply),
                                     reply_markup=words_kb.get_page_keyboard(page=data["cur"] + 1, max_page=data["max_page"]),
                                     disable_web_page_preview=True)

async def delete_word(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state("delete_word")
    await call.message.answer(text="Введите слово на английском, которое Вы хотите удалить.")

async def delete_word_execute(message: Message, state: FSMContext):
    try:
        await message.bot.get("database").delete_word(tg_tag=message.from_user.username, word=message.text)
        await message.answer(text="Слово успешно удалено", reply_markup=words_kb.to_words_choice)
    except Exception as ex:
        logging.info(ex)
        await message.answer(text="Не удалось найти слово, убедитесь в том, что вы в точности ввели добавленное слово.",
                             reply_markup=words_kb.to_words_choice)
    await state.finish()

def register_added_words(dp: Dispatcher):
    dp.register_callback_query_handler(choose_words_type, lambda call: call.data == "show_words")
    dp.register_callback_query_handler(to_words_type_choice, lambda call: call.data == "to_words_choice", state="*")
    dp.register_callback_query_handler(show_words, lambda call: call.data in ["trained", "not_trained"])
    dp.register_callback_query_handler(show_words_page, lambda call: call.data in ["prev_page", "next_page"], state="show_words")
    dp.register_callback_query_handler(delete_word, lambda call: call.data == "delete_word", state="*")
    dp.register_message_handler(delete_word_execute, state="delete_word")