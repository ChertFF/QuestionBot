from aiogram import types

groupVal = ['ГАО', 'Эксперты', 'ШПД', 'Ключевые клиенты', 'Бэк-Офис', 'Мониторинг', 'Поддержка и Эффективность', 'Другое']

group_keyboard = types.InlineKeyboardMarkup()
for group in groupVal:
    group_keyboard.add(types.InlineKeyboardButton(text=group, callback_data=f"groupVal_{group}"))