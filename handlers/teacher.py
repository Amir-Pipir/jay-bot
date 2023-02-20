from aiogram import types,Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import sqlite_db
from keyboards import teacher_kb
from aiogram.dispatcher.filters import Text

class Teacher(StatesGroup):
    time_table=State()

#@dp.message_handler(commands=['teacher'])
async def teacher_start(message: types.Message):
    x=await sqlite_db.check_for_admin(message.from_user.id)
    if  x == "teacher":
        await message.answer('Что будем делать?',reply_markup=teacher_kb)
    else:
        await message.answer('Ты не учитель!')

#@dp.message_handler(Text('Редактировать расписание'))
async def redact_timetable(message: types.Message):
    x = await sqlite_db.check_for_admin(message.from_user.id)
    if x == "teacher":
        await message.answer('Какое расписание?')
        await Teacher.time_table.set()
    else:
        await message.answer('Ты не учитель!')


#@dp.message_handler(state=Teacher.time_table)
async def redact_timetable1(message: types.Message, state: FSMContext):
    x = message.text.split()
    Day = x[0].lower()
    l_1=x[1]
    l_2=x[2]
    l_3=x[3]
    l_4=x[4]
    l_5=x[5]
    l_6=x[6]
    l_7=x[7]
    user_class=x[8]
    await sqlite_db.sql_time_table(Day=Day,l_1=l_1,l_2=l_2,l_3=l_3,l_4=l_4,l_5=l_5,l_6=l_6,l_7=l_7,user_class=user_class)
    await state.finish()
    await message.answer('Готово!')

def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(teacher_start,commands=['teacher'])
    dp.register_message_handler(redact_timetable, Text('Редактировать расписание'))
    dp.register_message_handler(redact_timetable1, state=Teacher.time_table)

