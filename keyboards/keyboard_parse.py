from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

sites = {'work_ua': 'https://www.work.ua/jobs-dnipro-python+developer/'}


worker_sites = InlineKeyboardMarkup(row_width=2)\
                                .row(InlineKeyboardButton('Work.ua', callback_data='site_work_ua'))
