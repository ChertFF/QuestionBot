from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline import start_keyboard
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!\n"
                         f"С моей помощью можешь задать вопросу Директору\n", reply_markup=start_keyboard)
