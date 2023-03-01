from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_start = ReplyKeyboardMarkup(resize_keyboard=True).\
                            row(KeyboardButton('Анкета'), KeyboardButton('Изменить анкету')).\
                            row(KeyboardButton('Поиск вакансий'), KeyboardButton('Спарсить вакансии')).\
                            add(KeyboardButton('Главная страница'))


customer_for_next = InlineKeyboardMarkup(row_width=2)


inlint_kb_language = InlineKeyboardMarkup(row_width=3).\
                            row(InlineKeyboardButton('Python🐍', callback_data='language_python'), 
                                InlineKeyboardButton('JavaScript', callback_data='language_javascript'), 
                                InlineKeyboardButton('Java', callback_data='language_java')).\
                            row(InlineKeyboardButton('C++', callback_data='language_c++'),
                                InlineKeyboardButton('Swift', callback_data='language_swift'))

inlint_kb_en_lvl = InlineKeyboardMarkup(row_width=3).\
                            row(InlineKeyboardButton('A1', callback_data='lvl_a1'), 
                                InlineKeyboardButton('A2', callback_data='lvl_a2'), 
                                InlineKeyboardButton('B1', callback_data='lvl_b1')).\
                            row(InlineKeyboardButton('B2', callback_data='lvl_b2'),
                                InlineKeyboardButton('C1', callback_data='lvl_c1'))

kb_next = ReplyKeyboardMarkup(resize_keyboard=True).\
                                  add(KeyboardButton('Дальше')).add(KeyboardButton('отмена'))


knb_can = ReplyKeyboardMarkup(resize_keyboard=True)\
                                .add(KeyboardButton('отменить'))
                                        

