from aiogram import types

cityVal = ['Иркутск', 'Ростов', 'Саранск', 'Челябинск']

city_keyboard = types.InlineKeyboardMarkup()
for city in cityVal:
    city_keyboard.add(types.InlineKeyboardButton(text=city, callback_data=f"cityVal_{city}"))