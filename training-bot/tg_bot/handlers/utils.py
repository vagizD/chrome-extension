import logging
from aiogram.types import Message
from aiogram.utils.exceptions import MessageNotModified, MessageCantBeEdited
from .keyboards import main_keyboards


async def registered(db, user_id: int) -> bool: # Проверяет регистрацию
    return await db.get_user(tg_id=user_id) is not None

async def remove_prev_button(message: Message): # Удаляет ненужные кнопки
    try:
        await message.delete_reply_markup()
    except (MessageNotModified, MessageCantBeEdited):
        pass
    except Exception as ex:
        logging.info(ex)


async def notify_unregistered(message: Message): # Оповещает о необходимости зарегистрироваться
    reply = [
        f"Кажется, Ваш телеграм аккаунт <b>не зарегистрирован</b>. "
        f"Укажите ваш телеграм айди в <b>настройках расширения!</b>",
        f"Ваш текущий айди: <code>{message.chat.id}</code>"
    ]
    await message.answer("\n\n".join(reply), reply_markup=main_keyboards.check_register_keyboard)