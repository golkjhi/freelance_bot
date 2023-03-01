from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from sql_commands.sqlite_main import *
from sql_commands.sql_costumer import *
from create_bot import bot
from keyboards import kb_client, kb_company
import aiohttp
import asyncio
import random


# async def check_user_chanel(message : types.Message):
#     await message.answer(f'Чтобы получить чек-лист, подпишись не телеграм канал @ksdaljgasdl',
#                          reply_markup=InlineKeyboardMarkup(row_width=2).\
#                             add(InlineKeyboardButton('Подписаться', url='https://t.me/ksdaljgasdl')).\
#                             add(InlineKeyboardButton('Проверить подписку', callback_data=f'check_{message.from_user.id}')))
    

# async def res_check_channel(callback : types.CallbackQuery):
#     user_ids = int(callback.data[callback.data.find('_')+1:])
#     status_user = await bot.get_chat_member(chat_id='@ksdaljgasdl', user_id=user_ids)
#     if status_user.status == 'left':
#         await callback.message.answer('Ты не подписался',
#                                       reply_markup=InlineKeyboardMarkup(row_width=2).\
#                             add(InlineKeyboardButton('Подписаться', url='https://t.me/ksdaljgasdl')).\
#                             add(InlineKeyboardButton('Проверить подписку', callback_data=f'check_{callback.from_user.id}')))
#     else:
#         await callback.message.answer('Привет, я бот. Помогу тебе в поиске работы или в поиске исполнителя, выбери что тебя интересует',
#                          reply_markup=kb_company.start_mess)
#         print(status_user.status)
#     await callback.answer()


# @dp.message_handler(commands=['start'])
async def start_message(message : types.Message):
    await create_profile(message.from_user.id)
    await message.answer('Привет, я бот. Помогу тебе в поиске работы или в поиске исполнителя, выбери что тебя интересует',
                         reply_markup=kb_company.start_mess)
    
async def finger_message(message : types.Message):
    await create_profile_company(message.from_user.id)
    await message.answer('Выбери кнопку внизу',
                         reply_markup=kb_company.kb_finder)
    

async def dev_message(message : types.Message):
    await create_profile(message.from_user.id)
    await message.answer('Привет, я бот. Помогу тебе в поиске работы или в поиске исполнителя, выбери что тебя интересует',
                         reply_markup=kb_client.kb_start)


def register_handlers_other(dp : Dispatcher):
    # dp.register_message_handler(check_user_chanel)
    # dp.register_callback_query_handler(res_check_channel, lambda x: x.data.startswith('check_'))
    dp.register_message_handler(start_message, commands=['start'])
    dp.register_message_handler(start_message, Text(equals='Главная страница'))
    dp.register_message_handler(finger_message, Text(equals='Я заказчик'))
    dp.register_message_handler(dev_message, Text(equals='Я фрилансер'))