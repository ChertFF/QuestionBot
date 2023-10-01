import emoji
import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from magic_filter import F
import aiogram.utils.markdown as fmt
from data.config import ADMIN_CHAT_ID
from filters import IsPrivate
from keyboards.inline import city_keyboard, group_keyboard
from loader import dp
from aiogram.dispatcher.filters import Command, Text

from states.ask import Ask


#После /start пользователь решил задать вопрос
@dp.callback_query_handler(F.data == 'startVal_Спросить', IsPrivate())
async def process_ask_press(callback: types.CallbackQuery):
    await callback.message.answer(f'Расскажи немного о себе {emoji.emojize("🔍")}\n'
                         f'Вопросы будут переданы анонимно, только с указанием города и отдела, в котором ты работаешь {emoji.emojize("🫶")}\n')
    await callback.message.answer(f'Выбери город, в котором ты работаешь:', reply_markup=city_keyboard)
    logging.info(
        f'Пользователь {callback.message.from_user.id} {callback.message.from_user.full_name} {callback.message.from_user.url} @{callback.message.from_user.username} решил задать вопрос | Выбор города')
    await Ask.City.set()


#Дубль функции выше, при вызове с клавиатуры
@dp.message_handler(Command("ask"))
async def start_ask_command(message: types.Message):
    await message.answer(f'Давай познакомимься. {emoji.emojize("🔍")}\n'
                         f'Вопросы будут переданы анонимно, только с указанием города и отдела, в котором ты работаешь {emoji.emojize("🫶")}\n')
    await message.answer(f'Выбери город, в котором ты работаешь:', reply_markup=city_keyboard)
    logging.info(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} {message.from_user.url} @{message.from_user.username} решил задать вопрос | Выбор города')
    await Ask.City.set()


@dp.callback_query_handler(lambda c: c.data.startswith('cityVal_'), state=Ask.City)
async def process_city_press(callback: types.CallbackQuery, state:FSMContext):
    # Удаляем клавитуру после ответа пользователя
    await dp.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    #Отсекаем в начале cityVal_ в callback, оставляя только название города
    city = callback.data.split('_')[1]
    #Записываем данные в State, чтобы передавать их из шага в шаг
    await state.update_data(City=city)
    # Извлекаем записанные данные, чтобы потом передать их в сообщение
    data = await state.get_data()
    await callback.message.answer(f'Супер, твой город {data.get("City")}!\n'
                                  f'Осталось уточнить последнюю деталь.')
    await callback.message.answer(f'Выбери отдел, в котором ты работаешь:', reply_markup=group_keyboard)
    logging.info(
        f'Пользователь {callback.message.from_user.id} {callback.message.from_user.full_name} {callback.message.from_user.url} @{callback.message.from_user.username} выбрал город {city} | Выбор отдела')
    await Ask.Group.set()


@dp.callback_query_handler(lambda c: c.data.startswith('groupVal_'), state=Ask.Group)
async def process_group_press(callback: types.CallbackQuery, state:FSMContext):
    # Удаляем клавитуру после ответа пользователя
    await dp.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    #Отсекаем в начале cityVal_ в callback, оставляя только название группы
    group = callback.data.split('_')[1]
    #Записываем данные в State, чтобы передавать их из шага в шаг
    await state.update_data(Group=group)
    # Извлекаем записанные данные, чтобы потом передать их в сообщение
    data = await state.get_data()
    await callback.message.answer(f'Отлично, твой отдел {data.get("Group")}!\n'
                                  f'Напиши вопрос, который ты бы хотел задать.', reply_markup=ReplyKeyboardRemove())
    logging.info(
        f'Пользователь {callback.message.from_user.id} {callback.message.from_user.full_name} {callback.message.from_user.url} @{callback.message.from_user.username} выбрал город {group} | Думает над вопросом')
    await Ask.Question.set()


@dp.message_handler(content_types=types.ContentType.TEXT,state=Ask.Question)
async def question_text(message: types.Message, state: FSMContext):
    # Извлекаем данные из стейтов
    await state.update_data(Question=message.text)
    data = await state.get_data()
    question = data.get("Question")
    city = data.get("City")
    group = data.get("Group")
    # Основной блок ниже
    await dp.bot.send_message(ADMIN_CHAT_ID, f'Поступил вопрос от сотрудника!\n'
                                             f'Данные о сотруднике:\n'
                                             f'город #{city}, отдел #{group}\n\n'
                                             f'{question}\n')
    await message.reply("Твой вопрос успешно передан!")
    logging.info(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} {message.from_user.url} @{message.from_user.username} задал вопрос {message.text}| Задал вопрос')
    await state.finish()


@dp.message_handler(content_types=types.ContentType.PHOTO,state=Ask.Question)
async def question_photo(message: types.Message, state: FSMContext):
    #Извлекаем данные из стейтов
    await state.update_data(Question=message.text)
    data = await state.get_data()
    question = data.get("Question")
    city = data.get("City")
    group = data.get("Group")
    #Основной блок ниже
    photo = message.photo[-1]
    photo_file = await dp.bot.get_file(photo.file_id)
    await dp.bot.send_message(ADMIN_CHAT_ID, f'Поступил вопрос от сотрудника!\n'
                                             f'Данные о сотруднике:\n'
                                             f'город #{city}, отдел #{group}\n\n'
                                             f'{question}\n')
    await dp.bot.send_photo(ADMIN_CHAT_ID, photo=photo_file.file_id, caption='Сотрудник прикрепил фото')
    await message.reply("Твой вопрос успешно передан!")
    logging.info(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} {message.from_user.url} @{message.from_user.username} задал вопрос c картинкой {message.text}| Задал вопрос')
    await state.finish()


@dp.message_handler(content_types=types.ContentType.VOICE,state=Ask.Question)
async def question_voice(message: types.Message, state: FSMContext):
    #Извлекаем данные из стейтов
    await state.update_data(Question=message.text)
    data = await state.get_data()
    question = data.get("Question")
    city = data.get("City")
    group = data.get("Group")
    #Основной блок ниже
    voice = message.voice
    voice_file = await dp.bot.get_file(voice.file_id)
    await dp.bot.send_voice(ADMIN_CHAT_ID, voice=voice_file.file_id, caption= f'Поступил вопрос от сотрудника!\n'
                                                                         f'Данные о сотруднике:\n'
                                                                         f'город #{city}, отдел #{group}\n\n')
    await message.reply("Твой вопрос успешно передан!")
    logging.info(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} {message.from_user.url} @{message.from_user.username} отправил голосовое | Задал вопрос')
    await state.finish()


@dp.message_handler(content_types=types.ContentType.VIDEO_NOTE,state=Ask.Question)
async def question_video_note(message: types.Message, state: FSMContext):
    #Извлекаем данные из стейтов
    await state.update_data(Question=message.text)
    data = await state.get_data()
    question = data.get("Question")
    city = data.get("City")
    group = data.get("Group")
    #Основной блок ниже
    video_note = message.video_note
    voice_file = await dp.bot.get_file(video_note.file_id)
    await dp.bot.send_voice(ADMIN_CHAT_ID, voice=voice_file.file_id)
    await dp.bot.send_message(ADMIN_CHAT_ID, text=f'Поступил вопрос от сотрудника!\n'
                                                  f'Данные о сотруднике:\n'
                                                  f'город #{city}, отдел #{group}\n\n')
    await message.reply("Твой вопрос успешно передан!")
    logging.info(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} {message.from_user.url} @{message.from_user.username} отправил кружок | Задал вопрос')
    await state.finish()