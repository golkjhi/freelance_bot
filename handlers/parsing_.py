# from aiogram import types, Dispatcher
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
# from aiogram.dispatcher.filters import Text
# from sql_commands.sqlite_main import *
# from create_bot import bot
# from keyboards import keyboard_parse
# import aiohttp
# import asyncio
# from bs4 import BeautifulSoup



# async def parse_vakancy(message : types.Message):
#     await message.answer('Модуль в разработке')
#     # await message.answer('Выбери сайт с которого парсить', 
#     #                      reply_markup=keyboard_parse.worker_sites)


# async def for_chat(message : types.Message):
#     a = await message.answer(message)
#     if len(a.entities)>0:
#         await message.delete()
#     else:
#         pass
    

# async def sites_callback(callback : types.CallbackQuery):
#     result_lst = ''
#     site = callback.data[callback.data.find('_')+1:]
#     url = keyboard_parse.sites[site]
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             soup = BeautifulSoup(await response.read(), 'lxml')
#             block = soup.find_all(class_="card card-hover card-visited wordwrap job-link")
#             for i in block:
#                 result_lst+=f"*{i.h2.text.strip()}* - https://www.work.ua/{i.a.get('href')}"+'\n'
#     await callback.message.answer(result_lst, 
#                                   disable_web_page_preview=True,
#                                   parse_mode='markdown')
    

# def register_handlers_parsing(dp : Dispatcher):
#     dp.register_message_handler(parse_vakancy, Text(equals='Спарсить вакансии'))
#     dp.register_message_handler(for_chat)
#     dp.register_callback_query_handler(sites_callback, lambda x: x.data.startswith('site_'))