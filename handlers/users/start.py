from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging

from filters import IsPrivate
from keyboards.inline import start_keyboard
from loader import dp
import emoji

@dp.message_handler(CommandStart(), IsPrivate())
async def bot_start(message: types.Message):
    await message.answer(f"Приветствую, Друг! {emoji.emojize('👋')}\n\n"
                         
                         f"Я создан, чтобы помочь тебе в выполнении одной интересной мисcии {emoji.emojize('💡')}\n"
                         f"С моей помощью ты можешь задать любой вопрос директору своего Контактного центра.\n\n"
                         
                         f"Вопросы будут переданы анонимно {emoji.emojize('🥸')}, но часть информации попросим указать: "
                         f"нам интересно из какого ты города и в каком отделе работаешь.\n\n"
                         
                         f"Свой вопрос ты можешь передать в самый разных и оригинальных форматах:\n"
                         f"{emoji.emojize('💬')} обычным текстовым сообщением;\n"
                         f"{emoji.emojize('📸')} фотографией;\n"
                         f"{emoji.emojize('🎙')} голосовым;\n"
                         f"{emoji.emojize('🎬')} видео-кружочком.\n\n"

                         f"Скорей жми кнопку ниже! {emoji.emojize('📢')}", reply_markup=start_keyboard)
    logging.info(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} {message.from_user.url} @{message.from_user.username} зарегистрировался в боте | {message.text}')
