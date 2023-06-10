import random
from typing import List

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from .utils import registered, notify_unregistered
from .keyboards import trainings_kb
from dataclasses import dataclass

@dataclass
class Data:
    word_id: int
    word: str
    trans: str
    website: str
    sentence: str
    learning_step: int

async def process_data(bot: Bot, tg_tag: str) -> List[Data]:
    data = await bot.get("database").get_user_not_trained_words(tg_tag=tg_tag)
    random.shuffle(data)
    return [Data(
        word_id=row.get("word_id"),
        word=row.get("word"),
        trans=row.get("trans"),
        website=row.get("website"),
        sentence=row.get("sentence"),
        learning_step=row.get("learning_step")) for row in data]

async def to_mode_choice(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(text="Выберите режим", reply_markup=trainings_kb.choose_mode_keyboard)

async def choose_training_mode(call: CallbackQuery):
    if not await registered(call.bot, call.from_user.username):
        await notify_unregistered(call)
    else:
        await call.message.edit_text(text="Выберите режим", reply_markup=trainings_kb.choose_mode_keyboard)


def register_training(dp: Dispatcher):
    dp.register_callback_query_handler(choose_training_mode, lambda call: call.data == "train")
    dp.register_callback_query_handler(to_mode_choice, lambda call: call.data == "to_mode_choice", state="*")