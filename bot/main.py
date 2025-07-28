import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoAPI.settings')

import asyncio
import logging
from os import getenv
from os.path import join
from pathlib import Path
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from bot.handlers import router

import django

django.setup()

path = Path(__file__).parent.parent
ENV_PATH = join(path, '.env')

load_dotenv(ENV_PATH)
BOT_TOKEN = getenv('BOT_TOKEN')

dp = Dispatcher()


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(
        *[router]
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
