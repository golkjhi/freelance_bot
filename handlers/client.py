from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from sql_commands.sqlite_main import *
from create_bot import bot
from keyboards import kb_client
import aiohttp
import random
import asyncio

costumer_users_offer = {}




class DeveloperUser(StatesGroup):
    name = State()
    age = State()
    country = State()
    language_and_experience = State()
    english_lvl = State()
    summary = State()
    contacts = State()
    photo = State()



async def find_work(message : types.Message):
    if await check_profile(message.from_user.id):
        global costumer_users_offer
        costumer_users_offer[message.from_user.id] = 0
        user_index = costumer_users_offer[message.from_user.id]
        customers = await urders_of_users(int(message.from_user.id))
        if customers:
            customers_id = [i[0] for i in customers]
            customers_text = [i[1] for i in customers]
            if not kb_client.customer_for_next.inline_keyboard:
                kb_client.customer_for_next.inline_keyboard.append([InlineKeyboardButton(text='Дальше',
                                                                                        callback_data=f'customer_')])

            if len(customers)>1:
                await bot.send_message(chat_id=message.from_user.id,
                                    text=f"{customers_text[user_index]}",
                                    parse_mode='markdown',
                                    reply_markup=kb_client.customer_for_next)
            else:
                end_mess = await bot.send_message(chat_id=message.from_user.id,
                                    text=f"{customers_text[user_index]}",
                                    parse_mode='markdown',
                                    )
                
                await end_mess.reply('Больше вакансий нету',
                                     reply_markup=kb_client.kb_start)
        else:
            await message.answer('Подходящих вакансий нету')
    else:
        await message.answer('У вас нету анкеты, заполните ее')
        await profile_message(message)

    costumer_users_offer[message.from_user.id] += 1


async def next_customer(callback : types.CallbackQuery):
    global costumer_users_offer
    customers = await urders_of_users(callback.from_user.id)
    user_index = costumer_users_offer[callback.from_user.id]

    try:
        next_index = customers[user_index+1]
    except:
        a = await bot.edit_message_text(chat_id=callback.message.chat.id,
                                text=f"{customers[user_index][1]}",
                                message_id=callback.message.message_id,
                                parse_mode='markdown')
        await a.reply('Больше офферов нету')
    else:
        kb_client.customer_for_next.inline_keyboard[0] = [InlineKeyboardButton(text='Дальше',
                                                                               callback_data=f'customer_')]
        await bot.edit_message_text(chat_id=callback.message.chat.id,
                                text=f"{customers[user_index][1]}",
                                message_id=callback.message.message_id,
                                parse_mode='markdown',
                                reply_markup=kb_client.customer_for_next)
    finally:
        costumer_users_offer[callback.from_user.id]+=1


# @dp.message_handler(Text(equals='Анкета'))
async def profile_message(message : types.Message):
    if await check_profile(message.from_user.id) and message.text != 'Изменить анкету':
        result = await profile_user(message.from_user.id)
        user_prof = await bot.send_photo(chat_id=message.from_user.id,
                             photo=result['photo'],
                             caption=f'''Имя: {result['name']}\nВозраст: {result['age']}\nСтрана: {result['country']}\nЯзык программирования и опыт: {result['language_and_experience']}\nУровень английского: {result['english_lvl']}\nСсылки для связи: {result['contacts']}''')
        await user_prof.reply_document(document=result['summary'],
                                       caption='Резюме')
    else:
        await DeveloperUser.name.set()
        await message.answer('Как тебя зовут??',
                             reply_markup=kb_client.knb_can)
        

# @dp.message_handler(Text(equals='отмена'), state='*')
async def cancel_message(message : types.Message, state : FSMContext):
    await message.reply(text='Заполнение анкеты прервано',
                        reply_markup=kb_client.kb_start)
    await state.finish()


# @dp.message_handler(state=DeveloperUser.name)
async def name_message(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    
    await message.answer('Сколько тебе лет?')
    await DeveloperUser.next()


# @dp.message_handler(lambda x: x.text.isdigit(), state=DeveloperUser.age)
async def age_message(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    
    await message.answer('В какой стране ты живешь?')
    await DeveloperUser.next()


# @dp.message_handler(state=DeveloperUser.country)
async def country_message(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['country'] = message.text
    
    await message.answer('Твой язык программирования и твой опыт\nПример: _1.Python, Опыт: 2 года_\nНужно описать все именно так (с учетом цифр и пробелов, т.к дальнейшие алгоритмы по поиску заказов для тебя будут определаться именно по этим полям)', parse_mode='markdown',
                         reply_markup=kb_client.inlint_kb_language)
    await message.answer('Вибери хоч 1',
                         reply_markup=kb_client.kb_next)
    await DeveloperUser.next()


# @dp.callback_query_handler(lambda x: x.data.startswith('language_'), state=DeveloperUser.language_and_experience)
async def language_and_experience_message(callback : types.CallbackQuery, state : FSMContext):
    lang = callback.data[callback.data.find('_')+1:]
    async with state.proxy() as data:
        res = data.get('language_and_experience', '')
        if lang not in res.split():
            res += lang+' '
            data['language_and_experience'] = res

            await callback.answer(f'Добавлен {lang}')
        else:
            await callback.answer(f'{res[:]} Уже есть')


# @dp.message_handler(Text(equals='Дальше'), state=DeveloperUser.language_and_experience)
async def language_and_experience_message_next(message : types.Message, state : FSMContext):
    
    await message.answer('Опиши свой опыт', 
                         reply_markup=kb_client.knb_can,
                        )


async def experience_message(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        
        data['language_and_experience'] += f' Опыт: {message.text}'
    
    await message.answer('Какой уровень английского??', 
                         reply_markup=kb_client.inlint_kb_en_lvl,
                        )
    await DeveloperUser.next()


# @dp.callback_query_handler(lambda x: x.data.startswith('lvl_'), state=DeveloperUser.english_lvl)
async def english_lvl_message(callback : types.CallbackQuery, state : FSMContext):
    async with state.proxy() as data:
        data['english_lvl'] = callback.data[callback.data.find('_')+1:]

        await callback.answer(data['english_lvl'])
    await callback.message.answer('Скинь свое резюме в формате .pdf',
                                  reply_markup=kb_client.knb_can)
    await DeveloperUser.next()


# @dp.message_handler(content_types=['document'], state=DeveloperUser.summary)
async def summary_message(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['summary'] = message.document.file_id
    
    await message.answer('Скинь ссылки на свои соц.сети')
    await DeveloperUser.next()


# @dp.message_handler(state=DeveloperUser.contacts)
async def contacts_message(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['contacts'] = message.text
    
    await message.answer('Скинь свое фото')
    await DeveloperUser.next()


# @dp.message_handler(content_types=['photo'], state=DeveloperUser.photo)
async def photo_message(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await bot.send_photo(chat_id=message.from_user.id,
                                photo=data['photo'],
                                caption='Вот твой документ',
                                reply_markup=kb_client.kb_start,
                                )
    await edit_profile(state, message.from_user.id)
    
    await message.answer('Принял')
    await state.finish()


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(profile_message, Text(equals='Изменить анкету'))
    dp.register_message_handler(profile_message, Text(equals='Анкета'))
    dp.register_message_handler(cancel_message, Text(equals='отменить'), state='*')
    dp.register_message_handler(find_work, Text(equals='Поиск вакансий'))
    dp.register_message_handler(language_and_experience_message_next, Text(equals='Дальше'), state=DeveloperUser.language_and_experience)
    dp.register_callback_query_handler(next_customer, lambda x: x.data.startswith('customer_'))
    dp.register_message_handler(name_message, state=DeveloperUser.name)
    dp.register_message_handler(age_message, lambda x: x.text.isdigit(), state=DeveloperUser.age)
    dp.register_message_handler(country_message, state=DeveloperUser.country)
    dp.register_callback_query_handler(language_and_experience_message, lambda x: x.data.startswith('language_'), state=DeveloperUser.language_and_experience)
    dp.register_message_handler(experience_message, state=DeveloperUser.language_and_experience)
    dp.register_callback_query_handler(english_lvl_message, lambda x: x.data.startswith('lvl_'), state=DeveloperUser.english_lvl)
    dp.register_message_handler(summary_message, content_types=['document'], state=DeveloperUser.summary)
    dp.register_message_handler(contacts_message, state=DeveloperUser.contacts)
    dp.register_message_handler(photo_message, content_types=['photo'], state=DeveloperUser.photo)