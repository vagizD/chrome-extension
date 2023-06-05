import random
from typing import List

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from .keyboards import trainings_kb
from dataclasses import dataclass

@dataclass
class Data:
    id: int
    word: str
    translated: str

async def to_mode_choice(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(text="Выберите режим", reply_markup=trainings_kb.choose_mode_keyboard)

async def choose_training_mode(call: CallbackQuery):
    await call.message.edit_text(text="Выберите режим", reply_markup=trainings_kb.choose_mode_keyboard)

async def process_data(bot: Bot, tg_tag: str) -> List[Data]:
    data = await bot.get("database").get_user_not_trained_words(tg_tag=tg_tag)
    random.shuffle(data)
    return [Data(id=row.get("word_id"), word=row.get("word"), translated=row.get("trans")) for row in data]

async def default_intro(call: CallbackQuery, state: FSMContext):
    words = await process_data(call.bot, call.from_user.username)
    if len(words) > 0:
        await state.set_state("default_mode")
        await state.update_data(current=1)
        await state.update_data(words=words)
        await call.message.edit_text(text="Описание режима. Начинаем?", reply_markup=trainings_kb.default_start)
    else:
        await call.message.edit_text(text="У вас нет неизученных слов!", reply_markup=trainings_kb.to_mode_choice)

async def default_start(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        reply = f"Введите перевод данного слова: {data['words'][0].word}"
        await call.message.edit_text(text=reply, reply_markup=trainings_kb.to_mode_choice)

async def default_next_word(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == data["words"][data["current"] - 1].translated.lower():
            await message.answer(text="Верно!")
            await message.bot.get("database").mark_as_trained(data["words"][data["current"] - 1].id)
        else:
            await message.answer(text=f"Неверно! Правильный ответ: {data['words'][data['current'] - 1].translated}")
        if data["current"] < len(data["words"]):
            data["current"] += 1
            reply = f"Введите перевод данного слова: {data['words'][data['current'] - 1].word}"
            await message.answer(text=reply, reply_markup=trainings_kb.to_mode_choice)
        else:
            await message.answer(text="Все слова изучены!", reply_markup=trainings_kb.to_mode_choice)


def register_training(dp: Dispatcher):
    dp.register_callback_query_handler(choose_training_mode, lambda call: call.data == "train")
    dp.register_callback_query_handler(default_intro, lambda call: call.data == "default_mode")
    dp.register_callback_query_handler(to_mode_choice, lambda call: call.data == "to_mode_choice", state="*")
    dp.register_callback_query_handler(default_start, lambda call: call.data == "default_start", state="default_mode")
    dp.register_message_handler(default_next_word, state="default_mode")