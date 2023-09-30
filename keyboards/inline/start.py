from aiogram import types

startVal = ['Спросить']

start_keyboard = types.InlineKeyboardMarkup()
for start in startVal:
    start_keyboard.add(types.InlineKeyboardButton(text=start, callback_data=f"startVal_{start}"))