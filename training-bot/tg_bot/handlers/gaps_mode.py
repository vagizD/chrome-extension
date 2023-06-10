import time

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from .trainings import process_data
from .keyboards import trainings_kb, gaps_kb

async def intro_info(call: CallbackQuery, state: FSMContext):
    words = await process_data(call.bot, call.from_user.username)
    await state.set_state("gaps_mode")
    await state.update_data(right=0)
    await state.update_data(overall=0)
    await state.update_data(words=words)
    cur = 0
    while cur < len(words) and words[cur].sentence is None:
        cur += 1
    if cur < len(words):
        await state.update_data(cur=cur)
        reply = [
            "<b><u>Режим дополнения</u></b>",
            "<b><u>Описание:</u></b> в данном режиме выбираются все неизученные слова. На каждом шаге необходимо "
            "вставить корректно переведенное слово в предложение. Вы можете завершить тренировку в любой момент, либо "
            "она завершится автоматически по истечении слов."
        ]
        await call.message.edit_text(text="\n\n".join(reply), reply_markup=gaps_kb.gaps_start)
    else:
        await state.finish()
        await call.message.edit_text(text="У вас нет неизученных слов! Возвращайтесь, когда добавите парочку.",
                                     reply_markup=trainings_kb.to_mode_choice)

async def start_round(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        current = data["words"][data["cur"]]
        reply = [
            "Введите корректный перевод подходящего слова:",
            f"{current.sentence.replace(current.word, '___')} ({current.trans})"
        ]
        data["cur"] += 1
        data["overall"] += 1
        await call.message.answer(text="\n\n".join(reply), reply_markup=trainings_kb.to_mode_choice)


async def next_word(message: Message, state: FSMContext):
    async with state.proxy() as data:
        prev = data["words"][data["cur"] - 1]
        if message.text.lower() == prev.word.lower():
            data["right"] += 1
            await message.answer(text="Верно ✓")
        else:
            await message.answer(text=f"Неверно ⊗\n\n{prev.sentence}")
        while data["cur"] < len(data["words"]) and data["words"][data["cur"]].sentence is None:
            data["cur"] += 1
        time.sleep(1)
        if data["cur"] == len(data["words"]):
            reply = [
                "Тренировка завершена!",
                f"Количество правильных ответов: {data['right']}/{data['overall']}"
            ]
            await state.finish()
            await message.answer(text="\n\n".join(reply), reply_markup=trainings_kb.to_mode_choice)
        else:
            current = data["words"][data["cur"]]
            reply = [
                "Введите корректный перевод подходящего слова:",
                f"{current.sentence.replace(current.word, '___')} ({current.trans})"
            ]
            data["cur"] += 1
            data["overall"] += 1
            await message.answer(text="\n\n".join(reply), reply_markup=trainings_kb.to_mode_choice)




def register_gaps_mode(dp: Dispatcher):
    dp.register_message_handler(next_word, state="gaps_mode")
    dp.register_callback_query_handler(intro_info, lambda call: call.data == "gaps_mode")
    dp.register_callback_query_handler(start_round, lambda call: call.data == "gaps_start", state="gaps_mode")