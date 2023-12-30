import asyncio
import logging
from aiogram import Bot, Dispatcher, types

import bd.bd_config
from bd.database import Database
from commands.add_vk_token import cmd_token
from commands.forward_from_vk import cmd_add
from vk import config

cfg = config.load()

API_TOKEN = cfg['tg_token']

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
database = Database(None)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    # added user id to BD
    user_id = message.from_user.id
    await dp['db'].save_user_to_db(user_id)

    await message.answer("Hi")


@dp.message_handler(commands=['get_users'])
async def cmd_start(message: types.Message):
    users = await dp['db'].get_all_users()
    await message.answer(users)


@dp.message_handler(commands=['token'])
async def cmd_token_wrapper(message: types.Message):
    text = await cmd_token(dp, message)
    await message.answer(text)


@dp.message_handler(commands=['add'])
async def cmd_add_wrapper(message: types.Message):
    text = await cmd_add(dp, message, message.from_user.id)
    await message.answer(text)


async def on_startup(dp):
    await database.create_pool(bd.bd_config.DB_CONFIG)
    dp['db'] = database


async def on_shutdown(dp):
    await dp['db'].pool.close()


async def main():
    await on_startup(dp)
    try:
        await dp.start_polling()
    finally:
        await on_shutdown(dp)


if __name__ == '__main__':
    asyncio.run(main())
