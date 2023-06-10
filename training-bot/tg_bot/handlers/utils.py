from typing import List
from dataclasses import dataclass
from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified
import random
from .keyboards import users_kb

async def registered(bot: Bot, tg_tag: str) -> bool:
    return await bot.get("database").get_user(tg_tag=tg_tag) is not None

async def notify_unregistered(call: CallbackQuery):
    reply = [
        f"Кажется, Ваш телеграм аккаунт <b>не зарегистрирован</b>. "
        f"Укажите ваш телеграм айди в <b>настройках расширения!</b>",
        f"Ваш текущий айди: <code>{call.from_user.username}</code>"
    ]
    try:
        await call.message.edit_text("\n\n".join(reply), reply_markup=users_kb.check_registry)
    except MessageNotModified:
        await call.message.reply("\n\n".join(reply), reply_markup=users_kb.check_registry)