from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from create_bot import bot
from keyboards import kb_company, kb_client
from sql_commands import sqlite_main
from sql_commands.sql_costumer import *


class CreateProfileCompany(StatesGroup):
    name_company = State()
    about_company = State()
    links = State()


async def all_my_tasks(message : types.Message):
    if await profile_company(message.from_user.id):
        tasks = await tasks_company(message.from_user.id)
        for i in tasks:
            a = await message.answer(text=i[2],
                                 reply_markup=InlineKeyboardMarkup(row_width=2).\
                                    add(InlineKeyboardButton('Удалить', callback_data=f'del_{i[0]}')))
            
async def del_task_message(callback : types.CallbackQuery):
    order_id = int(callback.data[callback.data.find('_')+1:])
    await del_task(order_id)
    await callback.answer('Запись успешно была удалена')


async def profile_company_message(message : types.Message, state=None):
    res_profile_comp = await profile_company(message.from_user.id)
    if message.text == 'Изменить анкету заказчика' or not res_profile_comp:
        await CreateProfileCompany.name_company.set()
        if not res_profile_comp:
            await message.answer("У вас нету анкеты, поэтому заполните ее или нажмите кнопку 'отмена'")
        await message.answer('Введите название вашей компании (Если вы не предоставляете компанию - ваше имя)',
                                reply_markup=kb_company.kb_company_can)
    else:
        res_txt = await profile_company(message.from_user.id)
        await message.answer(text=f"*Имя заказчика/компании*: {res_txt[1]}\n*О заказчике*: {res_txt[2]}\n*Ссылки для связи*: {res_txt[3]}\n*Рейтинг*: {res_txt[-1]}",
                             reply_markup=kb_company.kb_finder,
                             parse_mode='markdown',
                             )

async def name_company_message(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['name_company'] = message.text
    await CreateProfileCompany.next()
    await message.answer('Расскажите о вашей компании/о себе')

async def about_company_message(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['about_company'] = message.text
    await CreateProfileCompany.next()
    await message.answer('Ссылки для связи с вами (телеграм, гитхаб тд.)')

async def links_company_message(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['links'] = message.text
    await edit_company_profile(state, message.from_user.id)
    await message.answer('Отлично, ты создал анкету, теперь можешь найти исполнителя',
                         reply_markup=kb_company.kb_finder)
    await state.finish()


# работа с созданием анкеты
# ---------------------------------------------------------------------------
# работа с поиском исполнителя



class FindDev(StatesGroup):
    title = State()
    technical_task = State()
    language_pr = State()
    eng_lvl = State()
    deadline = State()
    contacts = State()


async def cancel_message_company(message : types.Message, state : FSMContext):
    await message.reply(text='Заполнение анкеты прервано',
                        reply_markup=kb_company.kb_finder)
    await state.finish()


async def start_message(message : types.Message):
    if await profile_company(message.from_user.id):
        await FindDev.title.set()
        await message.answer('Кого вы ищите (если вы ищете фрилансера, напишите задачу которую нужно решить)',
                            reply_markup=kb_company.kb_company_can)
    else:
        await profile_company_message(message)


async def title_message(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text

    await FindDev.next()
    await message.answer('Опишите тех.задание')


async def technical_task_pr_message(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['technical_task'] = message.text

    await FindDev.next()
    await message.answer('Языки программирования которыми должен обладать фрилансер',
                         reply_markup=kb_client.inlint_kb_language)
    await message.answer('Выбери минимум один', 
                                  reply_markup=kb_client.kb_next)
    


async def language_pr_message(callback : types.CallbackQuery, state : FSMContext):
    lang = callback.data[callback.data.find('_')+1:]
    async with state.proxy() as data:
        res = data.get('language_and_experience', '')
        if lang not in res.split():
            res += lang+' '
            data['language_and_experience'] = res

            await callback.answer(f'Добавлен {lang}')
        else:
            await callback.answer(f'{lang} Уже есть')


async def language_pr_message_next(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        res = data.get('language_and_experience', '')
        if not res:
            await message.answer('Ты не выбрал ни один язык, Выбери минимум 1 чтобы ПРОДОЛЖИТЬ', 
                                 reply_markup=kb_client.inlint_kb_language)
        else:
    
            await FindDev.next()
            await message.answer('Какой уровень английского??', 
                                reply_markup=kb_client.inlint_kb_en_lvl,
                                )
            await message.answer('Если уровень не важен, нажмите кнопку ПРОПУСТИТЬ',
                                 reply_markup=kb_company.kb_continue)


async def engl_pr_message(callback : types.CallbackQuery, state : FSMContext):
    async with state.proxy() as data:
        data['eng_lvl'] = callback.data[callback.data.find('_')+1:]
        await callback.answer()

    await FindDev.next()
    await callback.message.answer('Сроки выполнения работы',
                         reply_markup=kb_company.kb_company_can)
    

async def engl_pr_message_continue(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        eng = data.get('eng_lvl', '')+'a1 a2 b1 b2 c1'
        data['eng_lvl'] = eng

    await FindDev.next()
    await message.answer('Сроки выполнения работы',
                         reply_markup=kb_company.kb_company_can)
    

async def deadline_message(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['deadline'] = message.text

    await FindDev.next()
    await message.answer('Напишите контакты для связи с вами')
    
async def contacts_message(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['contacts'] = message.text

        await bot.send_message(chat_id=message.from_user.id,
                               text=f"*{data['title']}*\n*ТЗ*: {data['technical_task']}\n*Языки*: {data['language_and_experience']}\n*Уровень английского*: {data['eng_lvl']}\n*Дедлайн*: {data['deadline']}\n*Контакты для связи*: {data['contacts']}",
                               parse_mode='markdown',
                               reply_markup=kb_company.start_push)
        

async def start_push_messages(message : types.Message, state : FSMContext):
    lang = None
    async with state.proxy() as data:
        lang = data['language_and_experience']
        eng_lvl = data['eng_lvl']

        lang_user = await sqlite_main.user_for_push(lang)
        eng_lvl_users = await sqlite_main.user_for_push_eng(eng_lvl)
        res = await sqlite_main.result_push(eng_lvl_users, lang_user)

        if res:

            text = f"*{data['title']}*\n*ТЗ*: {data['technical_task']}\n*Языки*: {data['language_and_experience']}\n*Уровень английского*: {data['eng_lvl']}\n*Дедлайн*: {data['deadline']}\n*Контакты для связи*: {data['contacts']}"

            await add_order(message.from_user.id, res, text)
            await message.answer('Фрилансерам было отправлено ваше сообщение',
                                 reply_markup=kb_company.kb_finder)
        else:
            await message.answer('К сожалению у нас нету фрилансеров с данными параметрами',
                                 reply_markup=kb_company.kb_finder)
            
    await state.finish()





def register_handlers_company(dp : Dispatcher):
    dp.register_message_handler(cancel_message_company, Text(equals='отмена'), state='*')
    dp.register_message_handler(start_message, Text(equals='Изменить'))  
    dp.register_message_handler(start_message, Text(equals='Найти исполнителя'))  
    dp.register_message_handler(profile_company_message, Text(equals='Моя анкета'))
    dp.register_message_handler(all_my_tasks, Text(equals='Мои задания'))
    dp.register_message_handler(profile_company_message, Text(equals='Изменить анкету заказчика'))
    dp.register_message_handler(name_company_message, state=CreateProfileCompany.name_company)
    dp.register_message_handler(about_company_message, state=CreateProfileCompany.about_company)
    dp.register_message_handler(links_company_message, state=CreateProfileCompany.links)
    dp.register_message_handler(engl_pr_message_continue, Text(equals='Пропустить'), state=FindDev.eng_lvl)
    dp.register_message_handler(language_pr_message_next, Text(equals='Дальше'), state=FindDev.language_pr)
    dp.register_message_handler(start_push_messages, Text(equals='Начать рассылку'), state=FindDev.contacts)
    dp.register_callback_query_handler(del_task_message, lambda x: x.data.startswith('del_'))
    dp.register_callback_query_handler(language_pr_message, lambda x: x.data.startswith('language_'), state=FindDev.language_pr)
    dp.register_callback_query_handler(engl_pr_message, lambda x: x.data.startswith('lvl_'), state=FindDev.eng_lvl)
    dp.register_message_handler(title_message, state=FindDev.title)
    dp.register_message_handler(technical_task_pr_message, state=FindDev.technical_task)
    dp.register_message_handler(deadline_message, state=FindDev.deadline)
    dp.register_message_handler(contacts_message, state=FindDev.contacts) 