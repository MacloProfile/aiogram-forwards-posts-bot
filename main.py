import asyncio
import logging
from aiogram import Bot, Dispatcher, types

from bd.database import Database
from vk import main_vk, config

cfg = config.load()

API_TOKEN = cfg['tg_token']

# # channels VK - TELEGRAM
# group_channel = {}

# Данные для подключения к базе данных PostgreSQL
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'admin',
    'database': 'bot',
}

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
database = Database(None)


async def on_startup(dp):
    await database.create_pool(DB_CONFIG)
    dp['db'] = database


async def on_shutdown(dp):
    await dp['db'].pool.close()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("hi")


async def is_valid_channel_id(channel_id):
    try:
        chat_info = await bot.get_chat(chat_id=channel_id)
        return chat_info.type == types.ChatType.CHANNEL
    except Exception as e:
        return False


@dp.message_handler(commands=['add'])
async def cmd_start(message: types.Message):
    text_after_command = message.get_args().split(" ")
    first = int(text_after_command[0])
    second = int(text_after_command[1])

    if first != second:
        await dp['db'].save_channel_to_db(first, second)
        print("Data saved to the database")

    group_channel = (await dp['db'].take_group())[0]
    print("All group channels:", group_channel)

    tg_channel = await dp['db'].take_channel(group_channel)

    vk_task = asyncio.create_task(main_vk.run_vk(cfg, group_channel, tg_channel))
    await vk_task


async def main():
    await on_startup(dp)
    try:
        await dp.start_polling()
    finally:
        await on_shutdown(dp)


if __name__ == '__main__':
    asyncio.run(main())