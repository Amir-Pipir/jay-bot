from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

storage=MemoryStorage

bot = Bot(token='5306404487:AAHNVixDQRusl_jNpcAwt2Ws010YruG2Qxs')
dp = Dispatcher(bot, storage=MemoryStorage())
