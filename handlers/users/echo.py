from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from loader import dp


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.callback_query_handler(state="*")
async def bot_echo_all(callback: types.CallbackQuery, state: FSMContext):
    state_str = await state.get_state()
    await callback.message.answer(f'Упс! Произошла ошибка, я передал её разработчикам\n'
                             f'Попробуй задать вопрос снова.', reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(content_types=types.ContentTypes.ANY, state="*")
async def bot_echo_all(message: types.Message, state: FSMContext):
    state_str = await state.get_state()
    await message.answer(f'Упс! Произошла ошибка, я передал её разработчикам\n'
                             f'Попробуй задать вопрос снова.', reply_markup=ReplyKeyboardRemove())
    await state.finish()


