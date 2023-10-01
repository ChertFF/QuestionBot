from time import gmtime, strftime

import emoji

from data import config
from aiogram import types
from aiogram.dispatcher.filters import Command
from filters import IsAdmin
from loader import dp, bot
from utils.misc.logging import filename_path


@dp.message_handler(Command("logs_out"), IsAdmin())
async def logs_out(message: types.Message):
    await message.answer("Выгружаю для тебя логи...")
    await bot.send_document(message.from_user.id, types.InputFile(filename_path), caption=f'Актуальные данные для тебя {emoji.emojize(":heart_hands:")}')