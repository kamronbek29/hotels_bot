import asyncio
import redis
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import BOT_TOKEN

loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, loop=loop)

users_db = redis.StrictRedis(host='localhost', port=6379, db=1)

ADMIN_ID = 653391824
LIST_ADMIN_COMMANDS = ['send_everyone', 'admin', 'new_file']


class AdminSendEveryOne(StatesGroup):
    post = State()
    ask_send = State()


class AdminNewFile(StatesGroup):
    ask_file = State()


class AskUserInfo(StatesGroup):
    price = State()
    schengen = State()
    people = State()
    days = State()
    sea = State()
    sure = State()



