from aiogram import types,Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import sqlite_db
from keyboards import kb_other
from aiogram.dispatcher.filters import Text
from datetime import datetime
from create_bot import bot
import random


days=["понедельник","вторник","среда","четверг","пятница","суббота","воскресенье","понедельник"]

async def stickers(message: types.Message):
    x = ["CAACAgIAAxkBAAEE46Zil3Krruhlf5gNdYciEBFXxuiWSgACKxIAAnfgkEg4MgcsSOlQeyQE",
         "CAACAgIAAxkBAAEF3pJjJvLBd0z9H-mIm7REsLVDg-50sQACjh4AAsafGEmgupL6HGiFZCkE",
         "CAACAgIAAxkBAAEF3pRjJvLKqUVP-MBcRLsEGTRQCLFiQwAC4BMAAre5sEk3HSpD8MxmpikE",
         "CAACAgIAAxkBAAEF3pZjJvLebb3OLnoeINsTaaAiJ5Oc9QAC5xUAAphMyEteb5DLrghHRSkE",
         "CAACAgIAAxkBAAEF3phjJvLrWV80qjHIuLt-n5vEd-NcvwACKRUAAl-3iUgrFJ239Xg2MikE",
         "CAACAgIAAxkBAAEF3ppjJvMQw3hgrFa6ms-tL-ADfcU2KQAC8hUAAqkOiEiDYR42Egu1LSkE"]
    await bot.send_sticker(chat_id=message.from_user.id,sticker=random.choice(x))


class Form(StatesGroup):
    user_class= State()

class Check_time(StatesGroup):
    Day=State()

class Check_hw(StatesGroup):
    sub = State()

class Chr(StatesGroup):
    message = State()

#@dp.message_handler(commands=['start','help'])
async def start_message(message: types.Message):
    await message.answer('Напиши класс,в котором ты учишься')
    await Form.user_class.set()


#@dp.message_handler(state=Form.a)
async def start(message: types.Message, state: FSMContext):
    user_class = message.text
    user_id=message.from_user.id

    user_name=message.from_user.username
    await sqlite_db.sql_start(message,ID=user_id,username=user_name,user_class=user_class,role="user")
    await state.finish()
    await message.answer(f"Отлично теперь я знаю,что ты учишься в {user_class} классе!")
    await stickers(message)
    await message.answer('Что теперь будем делать?', reply_markup=kb_other)


#@dp.message_handler(Text('Посмотреть расписание'))
async def check_timetable(message : types.Message):
    await message.answer('На какой день ты хочешь посмотреть расписание?')
    await Check_time.Day.set()

async def check_day(message: types.Message, state: FSMContext):
    Day = message.text.lower()
    global days
    if Day == "завтра":
        date = datetime.today()
        today = date.weekday()
        Day = days[today+1]
    
    if Day == "сегодня":
        date = datetime.today()
        today = date.weekday()
        Day = days[today]


    await sqlite_db.sql_check_tb(message, Day, message.from_user.id)
    await state.finish()
    await stickers(message)

#@dp.message_handler(Text('Посмотреть ДЗ'))
async def check_hw(message: types.Message):
    await message.answer('По какому предмету ты хочешь посмотреть ДЗ?')
    await Check_hw.sub.set()

async def check_sub(message: types.Message, state: FSMContext):
    sub = message.text.lower()
    if sub == 'завтра':
        date = datetime.today()
        today = date.weekday()
        Day = days[today + 1]
        await sqlite_db.hw_tomorrow(message,message.from_user.id,Day)
    else:
        await sqlite_db.sql_check_hw(message,sub,message.from_user.id)
    await state.finish()
    await stickers(message)

#@dp.message_handler(commands=[''])
password = ''
async def change_role1(message: types.Message):
    global password
    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    y=""
    for i in range(8):
        y += random.choice(chars)
    password = y
    await bot.send_message(717005403,password)
    await message.answer('Пароль?')
    await Chr.message.set()


async def change_role2(message: types.Message, state:FSMContext):
    try:
        x = message.text.split(',')
        if x[0] == password :
            await sqlite_db.change_role(message.from_user.id,x[1])
            await message.answer('Все!')
        else:
            await message.answer('Неправильный пароль!')
        await state.finish()

    except:
        await message.answer('АШИБКА!')
        await state.finish()



async def echo(message: types.Message):
    await message.answer(message.text)




def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(start_message,commands=['start','help'])
    dp.register_message_handler(start, state=Form.user_class)
    dp.register_message_handler(check_timetable, Text('Посмотреть расписание'), state=None)
    dp.register_message_handler(check_day, state=Check_time.Day)
    dp.register_message_handler(check_hw, Text('Посмотреть ДЗ'), state=None)
    dp.register_message_handler(check_sub, state=Check_hw.sub)
    dp.register_message_handler(change_role1, commands=['change_role'])
    dp.register_message_handler(change_role2, state=Chr.message)
    dp.register_message_handler(echo)
