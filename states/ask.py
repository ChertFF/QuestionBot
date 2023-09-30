from aiogram.dispatcher.filters.state import StatesGroup, State

class Ask(StatesGroup):
    City = State()
    Group = State()
    Question = State()