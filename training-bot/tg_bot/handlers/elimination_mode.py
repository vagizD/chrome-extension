import random
import time
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from .trainings import process_data
from .keyboards import trainings_kb

MAX_WORDS = 15

async def intro_info(call: CallbackQuery, state: FSMContext):
    await call.answer()
    words = await process_data(bot=call.bot, tg_tag=call.from_user.username, trained=False)
    if len(words) > 0:
        await state.set_state("elimination")
        await state.update_data(words=words[:MAX_WORDS])
        reply = [
            "<b><u>До последнего</u></b>",
            "<b><u>Описание:</u></b> в данном режиме выбираются от 1 до 20 случайных добавленных и неизученных слов. "
            "На каждом шаге необходимо ввести корректный перевод предложенного слова. Если Ваш ответ верный, слово "
            "пропадает из текущей тренировки, иначе остается. Для завершения тренировки нужно верно перевести все "
            "случайно выбранные слова.",
            "<b><u>Выберите один из предложенных режимов:</u></b> перевод с русского на английский, перевод с английского "
            "на русский или оба варианта в случайном порядке."
        ]
        await call.message.edit_text(text="\n\n".join(reply), reply_markup=trainings_kb.choose_language)
    else:
        await state.finish()
        reply = [
            "У вас нет неизученных слов!",
            "Возвращайтесь, когда добавите парочку."
        ]
        await call.message.edit_text(text="\n\n".join(reply), reply_markup=trainings_kb.to_mode_choice)

async def start_round(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    words = data["words"]
    it = random.randint(0, len(words) - 1)
    await state.set_state(f"elimination_{call.data}")
    await state.update_data(prev=it)
    await state.update_data(words=words)
    if call.data == "ru_to_en":
        await state.update_data(ru=True)
        await call.message.edit_text(f"Переведите данное слово: {words[it].trans}", reply_markup=trainings_kb.to_mode_choice)
    elif call.data == "en_to_ru":
        await state.update_data(ru=False)
        await call.message.edit_text(f"Переведите данное слово: {words[it].word}", reply_markup=trainings_kb.to_mode_choice)
    elif call.data == "rand_mode":
        if random.randint(0, 1):
            await state.update_data(ru=False)
            await call.message.edit_text(f"Переведите данное слово: {words[it].word}", reply_markup=trainings_kb.to_mode_choice)
        else:
            await state.update_data(ru=True)
            await call.message.edit_text(f"Переведите данное слово: {words[it].trans}", reply_markup=trainings_kb.to_mode_choice)


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
            if await state.get_state() == "elimination_rand_mode":
                if random.randint(0, 1):
                    data["ru"] = True
                    await message.answer(f"Переведите данное слово: {data['words'][it].trans}",
                                         reply_markup=trainings_kb.to_mode_choice)
                else:
                    data["ru"] = False
                    await message.answer(f"Переведите данное слово: {data['words'][it].word}",
                                         reply_markup=trainings_kb.to_mode_choice)
            elif data["ru"]:
                await message.answer(f"Переведите данное слово: {data['words'][it].trans}",
                                     reply_markup=trainings_kb.to_mode_choice)
            else:
                await message.answer(f"Переведите данное слово: {data['words'][it].word}",
                                     reply_markup=trainings_kb.to_mode_choice)
        else:
            await state.finish()
            await message.answer("Вы успешно завершили тренировку!", reply_markup=trainings_kb.to_mode_choice)



def register_elimination_mode(dp: Dispatcher):
    dp.register_callback_query_handler(intro_info, lambda call: call.data == "elimination_mode")
    dp.register_message_handler(next_word, state=["elimination_ru_to_en", "elimination_en_to_ru", "elimination_rand_mode"])
    dp.register_callback_query_handler(start_round, lambda call: call.data in ["ru_to_en", "en_to_ru", "rand_mode"], state="elimination")