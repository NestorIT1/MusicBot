import logging
from aiogram import Bot, Dispatcher, executor
from config import BOT_TOKEN
from handlers import music, basic, basic2

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

basic.register_handlers_basic(dp)
music.register_handlers_music(dp)
basic2.register_handler_basic2(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
