from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage
#import os
#from dotenv import load_dotenv,find_dotenv

#load_dotenv(find_dotenv())

storage=MemoryStorage

#bot = Bot(token=os.getenv('BOT_TOKEN'))
bot = Bot('5306404487:AAGg_XQJw51JJfHNhU6C_XcMh7XE7X9vUPs')
dp = Dispatcher(bot, storage=MemoryStorage())

#DB_URI=os.getenv("DB_URI")
DB_URI = ('postgres://bxilbbud:SsuWC0gTuxiD4tg3GtnsVFL__Jt1BhMk@manny.db.elephantsql.com/bxilbbud')
