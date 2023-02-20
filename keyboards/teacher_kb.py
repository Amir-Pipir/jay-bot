from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

teacher_kb = ReplyKeyboardMarkup(resize_keyboard=True)

teacher_kb.add('Посмотреть расписание','Посмотреть ДЗ',).row('Редактировать расписание')