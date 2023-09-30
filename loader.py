from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiohttp import BasicAuth

from data import config



#bot = Bot(token=config.BOT_TOKEN, proxy=proxy_url, parse_mode=types.ParseMode.HTML)
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
