from aiogram.dispatcher.filters import BoundFilter
import config

class AdminFilter(BoundFilter):
    async def check(self, obj) -> bool:
        conf: config.Config = obj.bot.get('config')
        return obj.from_user_id in conf.tg_bot.admins