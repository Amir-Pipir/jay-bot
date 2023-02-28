from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import sqlite_db
from keyboards import kb_admin
from aiogram.dispatcher.filters import Text


class HW(StatesGroup):
    message = State()


# @dp.message_handler(commands=['admin'])
async def admin_start(message: types.Message):
    x = await sqlite_db.check_for_admin(message.from_user.id)
    if x == 'admin':
        await message.answer('Приветствую админа!', reply_markup=kb_admin)
    else:
        await message.answer('Ты не админ!')


# @dp.message_handler(Text('Редактировать ДЗ'))
async def insert_hw(message: types.Message):
    x = await sqlite_db.check_for_admin(message.from_user.id)
    if x == 'admin' or x == 'teacher':
        await message.answer('Какое ДЗ?')
        await HW.message.set()
    else:
        await message.answer('Ты не админ!')


# @dp.message_handler(state=HW.message)
async def hw_message(message: types.Message, state: FSMContext):
    try:
        x = message.text.split(':')
        sub = x[0]
        hw = x[1]
        Class = await sqlite_db.check_class(message.from_user.id)

        await sqlite_db.sql_home_work(subject=sub, homework=hw, user_class=Class)
        await state.finish()
        await message.answer('Готово!')
    except:
        await message.answer('Ошибка!Попробуйте еще раз!')
        await state.finish()




def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=['admin'])
    dp.register_message_handler(insert_hw, Text('Редактировать ДЗ'))
    dp.register_message_handler(hw_message, state=HW.message)
    #dp.register_message_handler(hw_photo, content_types=['photo'], state=HW.photo)
