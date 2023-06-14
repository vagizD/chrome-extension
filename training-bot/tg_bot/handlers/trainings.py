import random
from datetime import datetime
from typing import List

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

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
    learned_at: datetime
    learning_step: int

async def process_data(bot: Bot, **kwargs) -> List[Data]:
    data = await bot.get("database").get_words(**kwargs)
    random.shuffle(data)
    return [Data(
        word_id=row.get("word_id"),
        word=row.get("word"),
        trans=row.get("trans"),
        website=row.get("website"),
        sentence=row.get("sentence"),
        learned_at=row.get("learned_at"),
        learning_step=row.get("learning_step")) for row in data]

async def to_mode_choice(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.finish()
    await call.message.edit_text(text="Выберите режим тренировки, чтобы увидеть его описание.",
                                 reply_markup=trainings_kb.choose_training_mode)

async def choose_training_mode(call: CallbackQuery):
    await call.answer()
    if not await registered(call.bot, call.from_user.username):
        await notify_unregistered(call)
    else:
        await call.message.edit_text(text="Выберите режим тренировки, чтобы увидеть его описание.",
                                     reply_markup=trainings_kb.choose_training_mode)


def register_training(dp: Dispatcher):
    dp.register_callback_query_handler(choose_training_mode, lambda call: call.data == "train")
    dp.register_callback_query_handler(to_mode_choice, lambda call: call.data == "to_mode_choice", state="*")