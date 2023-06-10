import random
import time
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from .trainings import process_data
from .keyboards import elimination_kb, trainings_kb


async def intro_info(call: CallbackQuery, state: FSMContext):
    words = await process_data(call.bot, call.from_user.username)
    if len(words) > 0:
        await state.set_state("elimination")
        await state.update_data(words=words[:20])
        reply = [
            "<b><u>Режим устранения</u></b>",
            "<b><u>Описание:</u></b> в данном режиме выбираются от 1 до 20 случайных добавленных и неизученных слов. "
            "На каждом шаге необходимо ввести корректный перевод предложенного слова. Если Ваш ответ верный, слово "
            "пропадает из текущей тренировки, иначе остается. Для завершения тренировки нужно верно перевести все "
            "случайно выбранные слова.",
            "<b><u>Выберите один из предложенных режимов:</u></b> перевод с русского на английский, перевод с английского "
            "на русский или оба варианта в случайном порядке."
        ]
        await call.message.edit_text(text="\n\n".join(reply), reply_markup=elimination_kb.choose_mode)
    else:
        await call.message.edit_text(text="У вас нет неизученных слов! Возвращайтесь, когда добавите парочку.",
                                     reply_markup=trainings_kb.to_mode_choice)

async def start_round(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    words = data["words"]
    it = random.randint(0, len(words) - 1)
    await state.set_state(call.data)
    await state.update_data(prev=it)
    await state.update_data(words=words)
    if call.data == "ru_to_en":
        await state.update_data(ru=True)
        await call.message.edit_text(f"Введите перевод данного слова: {words[it].trans}")
    elif call.data == "en_to_ru":
        await state.update_data(ru=False)
        await call.message.edit_text(f"Введите перевод данного слова: {words[it].word}")
    elif call.data == "rand_mode":
        if random.randint(0, 1):
            await state.update_data(ru=False)
            await call.message.edit_text(f"Введите перевод данного слова: {words[it].word}")
        else:
            await state.update_data(ru=True)
            await call.message.edit_text(f"Введите перевод данного слова: {words[it].trans}")


async def next_word(message: Message, state: FSMContext):
    async with state.proxy() as data:
        prev = data["words"][data["prev"]]
        if data["ru"]:
            if message.text.lower() == prev.word.lower():
                await message.answer("Верно ✓")
                data["words"].pop(data["prev"])
            else:
                await message.answer(f"Неверно ⊗\n\n Правильный перевод: {prev.word.lower()}")
        else:
            if message.text.lower() == prev.trans.lower():
                await message.answer("Верно ✓")
                data["words"].pop(data["prev"])
            else:
                await message.answer(f"Неверно ⊗\n\n Правильный перевод: {prev.trans.lower()}")
        time.sleep(1)
        if len(data["words"]) > 0:
            it = random.randint(0, len(data["words"]) - 1)
            data["prev"] = it
            if await state.get_state() == "rand_mode":
                if random.randint(0, 1):
                    data["ru"] = True
                    await message.answer(f"Введите перевод данного слова: {data['words'][it].trans}",
                                         reply_markup=trainings_kb.to_mode_choice)
                else:
                    data["ru"] = False
                    await message.answer(f"Введите перевод данного слова: {data['words'][it].word}",
                                         reply_markup=trainings_kb.to_mode_choice)
            elif data["ru"]:
                await message.answer(f"Введите перевод данного слова: {data['words'][it].trans}",
                                     reply_markup=trainings_kb.to_mode_choice)
            else:
                await message.answer(f"Введите перевод данного слова: {data['words'][it].word}",
                                     reply_markup=trainings_kb.to_mode_choice)
        else:
            await state.finish()
            await message.answer("Вы успешно завершили тренировку!", reply_markup=trainings_kb.to_mode_choice)



def register_elimination_mode(dp: Dispatcher):
    dp.register_message_handler(next_word, state=["ru_to_en", "en_to_ru", "rand_mode"])
    dp.register_callback_query_handler(intro_info, lambda call: call.data == "elimination_mode")
    dp.register_callback_query_handler(start_round, lambda call: call.data in ["ru_to_en", "en_to_ru", "rand_mode"], state="elimination")