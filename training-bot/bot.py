import asyncio
import logging
import sys, os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

from tg_bot.filters.admins import AdminFilter
from tg_bot.handlers.admins import register_admins, notify
from tg_bot.handlers.users import register_users
from tg_bot.handlers.trainings import register_training
from tg_bot.handlers.added_words import register_added_words
from tg_bot.config import load_config
from tg_bot.utils.db_api.postgres import Database


logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

def register_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)

def register_handlers(dp: Dispatcher):
    register_users(dp)
    register_admins(dp)
    register_added_words(dp)
    register_training(dp)

async def main():
    config = load_config(".env")
    bot = Bot(token=config.tg_bot.token, parse_mode=ParseMode.HTML)
    bot['config'] = config
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    await notify(dp)

    db = Database(config)
    bot['database'] = db
    logging.info(f"{db.config.user} connecting to {db.config.host}...")
    await db.create()
    logging.info("Creating Users table...")
    await db.create_users_table()
    logging.info("Creating Words table...")
    await db.create_words_table()

    register_filters(dp)
    register_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Stopped.")
