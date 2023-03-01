from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sql_commands.sql_costumer import *


start_push = ReplyKeyboardMarkup(resize_keyboard=True)\
                                .row(KeyboardButton('Начать рассылку'), KeyboardButton('Главная страница')).\
                                add(KeyboardButton('Изменить'))


kb_finder = ReplyKeyboardMarkup(resize_keyboard=True).\
                            row(KeyboardButton('Моя анкета'), KeyboardButton('Изменить анкету заказчика')).\
                            row(KeyboardButton('Найти исполнителя'), KeyboardButton('Главная страница')).\
                            add(KeyboardButton('Мои задания'))

start_mess = ReplyKeyboardMarkup(resize_keyboard=True)\
                                    .add(KeyboardButton('Я заказчик'))\
                                    .add(KeyboardButton('Я фрилансер'))

kb_continue = ReplyKeyboardMarkup(resize_keyboard=True).\
                                  add(KeyboardButton('Пропустить')).add(KeyboardButton('отмена'))

kb_company_can = ReplyKeyboardMarkup(resize_keyboard=True).\
                                  add(KeyboardButton('отмена'))


