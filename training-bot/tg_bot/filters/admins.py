from typing import Union

from aiogram.dispatcher.filters import BoundFilter
import config
class AdminFilter(BoundFilter):

    key = 'is_admin'
    def __init__(self, is_admin = None):
        self.is_admin = is_admin

    async def check(self, obj) -> Union[bool, None]:
        if self.is_admin is None:
            return
        if not self.is_admin:
            return False
        conf: config.Config = obj.bot.get('config')
        return obj.chat.id in conf.tg_bot.admins