import asyncio
import logging
from aiogram import Bot, Dispatcher, types

import bd.bd_config
from bd.database import Database
from bot_commands import cmd_add
from vk import main_vk, config

cfg = config.load()

API_TOKEN = cfg['tg_token']

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
database = Database(None)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("hi")


async def on_startup(dp):
    await database.create_pool(bd.bd_config.DB_CONFIG)
    dp['db'] = database


async def on_shutdown(dp):
    await dp['db'].pool.close()


@dp.message_handler(commands=['add'])
async def cmd_add_wrapper(message: types.Message):
    await cmd_add(dp, message, cfg)


async def main():
    await on_startup(dp)
    try:
        await dp.start_polling()
    finally:
        await on_shutdown(dp)


if __name__ == '__main__':
    asyncio.run(main())