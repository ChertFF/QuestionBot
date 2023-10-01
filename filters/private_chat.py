from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from loader import dp, bot


class IsPrivate(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return (message.chat.type == types.ChatType.PRIVATE)