from datetime import datetime, timedelta
import time
import random
from typing import List

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from .trainings import Data, process_data
from .keyboards import trainings_kb

MAX_STEP = 8

def get_timedelta(step: int) -> timedelta:
    if step == 0:
        return timedelta(seconds=0)
    if step == 1:
        return timedelta(minutes=30)
    if step == 2:
        return timedelta(hours=2)
    if step == 3:
        return timedelta(hours=6)
    if step == 4:
        return timedelta(hours=12)
    if step == 5:
        return timedelta(days=1)
    if step == 6:
        return timedelta(days=4)
    if step == 7:
        return timedelta(days=8)
    if step == 8:
        return timedelta(days=14)

async def process_available_data(bot: Bot, tg_tag: str) -> List[Data]:
    data: List[Data] = await process_data(bot, tg_tag=tg_tag, trained=False)
    result: List[Data] = []
    for word in data:
        next_time = word.learned_at + get_timedelta(word.learning_step)
        if datetime.now().replace(microsecond=0) > next_time:
            result.append(word)
    return result

async def intro_info(call: CallbackQuery, state: FSMContext):
    await call.answer()
    words = await process_available_data(call.bot, call.from_user.username)
    if len(words) > 0:
        await state.set_state("main_mode")
        await state.update_data(words=words)
        reply = [
            "<b><u>Главная тренировка</u></b>",
            "<b><u>Описание:</u></b> в данном режиме происходит основное изучение слов. Вам будут предложено перевести "
            "еще не изученные слова, доступные для тренировки. Если вы правильно перевели слово, оно будет встречаться "
            "реже. При неправильном ответе встречаться чаще. Слово будет считаться изученным при успешном прохождении "
            "всех циклов изучения.",
            "<b><u>Выберите один из предложенных режимов:</u></b> перевод с русского на английский, перевод с английского "
            "на русский или оба варианта в случайном порядке."
        ]
        await call.message.edit_text(text="\n\n".join(reply), reply_markup=trainings_kb.choose_language)
    else:
        await state.finish()
        reply = [
            "У вас нет доступных неизученных слов!",
            "Возвращайтесь позже или добавьте новые слова."
        ]
        await call.message.edit_text(text="\n\n".join(reply), reply_markup=trainings_kb.to_mode_choice)

async def start_round(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    words = data["words"]
    await state.set_state(f"main_{call.data}")
    await state.update_data(cur=1)
    await state.update_data(words=words)
    if call.data == "ru_to_en":
        await state.update_data(ru=True)
        await call.message.answer(text=f"Переведите данное слово: {words[0].trans}", reply_markup=trainings_kb.to_mode_choice)
    elif call.data == "en_to_ru":
        await state.update_data(ru=False)
        await call.message.answer(text=f"Переведите данное слово: {words[0].word}", reply_markup=trainings_kb.to_mode_choice)
    elif call.data == "rand_mode":
        if random.randint(0, 1):
            await state.update_data(ru=False)
            await call.message.answer(text=f"Переведите данное слово: {words[0].word}", reply_markup=trainings_kb.to_mode_choice)
        else:
            await state.update_data(ru=True)
            await call.message.answer(text=f"Переведите данное слово: {words[0].trans}", reply_markup=trainings_kb.to_mode_choice)

async def next_word(message: Message, state: FSMContext):
    async with state.proxy() as data:
        prev: Data = data["words"][data["cur"] - 1]
        if data["ru"]:
            if message.text.lower() == prev.word.lower():
                await message.answer("Верно ✓")
                await message.bot.get("database").increment_step(word_id=prev.word_id, learning_step=prev.learning_step)
                if prev.learning_step == MAX_STEP:
                    await message.bot.get("database").mark_as_trained(word_id=prev.word_id)
            else:
                await message.answer(f"Неверно ⊗\n\n Правильный перевод: {prev.word.lower()}")
                await message.bot.get("database").decrement_step(word_id=prev.word_id, learning_step=prev.learning_step)
        else:
            if message.text.lower() == prev.trans.lower():
                await message.answer("Верно ✓")
                await message.bot.get("database").increment_step(word_id=prev.word_id, learning_step=prev.learning_step)
                if prev.learning_step == MAX_STEP:
                    await message.bot.get("database").mark_as_trained(word_id=prev.word_id)
            else:
                await message.answer(f"Неверно ⊗\n\n Правильный перевод: {prev.trans.lower()}")
                await message.bot.get("database").decrement_step(word_id=prev.word_id, learning_step=prev.learning_step)
        time.sleep(1)
        if data["cur"] == len(data["words"]):
            await state.finish()
            await message.answer("Тренировка завершена!", reply_markup=trainings_kb.to_mode_choice)
        else:
            current: Data = data["words"][data["cur"]]
            data["cur"] += 1
            if await state.get_state() == "main_random_mode":
                if random.randint(0, 1):
                    data["ru"] = True
                    await message.answer(text=f"Переведите данное слово: {current.trans}", reply_markup=trainings_kb.to_mode_choice)
                else:
                    data["ru"] = False
                    await message.answer(text=f"Переведите данное слово: {current.word}", reply_markup=trainings_kb.to_mode_choice)
            elif data["ru"]:
                data["ru"] = True
                await message.answer(text=f"Переведите данное слово: {current.trans}", reply_markup=trainings_kb.to_mode_choice)
            else:
                data["ru"] = False
                await message.answer(text=f"Переведите данное слово: {current.word}", reply_markup=trainings_kb.to_mode_choice)



def register_main_mode(dp: Dispatcher):
    dp.register_callback_query_handler(intro_info, lambda call: call.data == "main_mode")
    dp.register_message_handler(next_word, state=["main_ru_to_en", "main_en_to_ru", "main_rand_mode"])
    dp.register_callback_query_handler(start_round, lambda call: call.data in ["ru_to_en", "en_to_ru", "rand_mode"],
                                       state="main_mode")