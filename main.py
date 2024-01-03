import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from commands.other_messages import *

import bd.bd_config
from commands.buttons import text_profile, text_help, restart
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


def reply_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('🍂 Help'), KeyboardButton('🏝 Info'), KeyboardButton('🌾 Profile'))
    return keyboard


@dp.message_handler(lambda message: True, state="*")
async def cmd_unknown(message: types.Message):
    text_reply = "Sorry, I don't understand this command. Please use the available buttons or commands."
    if "https://vk.com/" in message.text:
        text_reply = get_vk_id(message.text, await dp['db'].get_vk_token(message.from_user.id))
    await message.answer(text_reply)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    # added user id to BD
    user_id = message.from_user.id
    await dp['db'].save_user_to_db(user_id)

    keyboard = reply_keyboard()

    await message.answer("Hi", reply_markup=keyboard)


@dp.message_handler(text=['🌾 Profile'], state="*")
@dp.message_handler(commands=['profile'])
async def cmd_start(message: types.Message):
    text = text_profile(message.from_user.id)
    await message.answer(text)


@dp.message_handler(text=['🍂 Help'], state="*")
@dp.message_handler(commands=['get_users'])
async def cmd_start(message: types.Message):
    text = text_help()
    await message.answer(text)


@dp.message_handler(text=['🏝 Info'], state="*")
@dp.message_handler(commands=['get_users'])
async def cmd_start(message: types.Message):
    users = await dp['db'].get_all_users()
    await message.answer("Users: " + str(users))


@dp.message_handler(commands=['token'])
async def cmd_token_wrapper(message: types.Message):
    text = await cmd_token(dp, message)
    await message.answer(text)


@dp.message_handler(commands=['add'])
async def cmd_add_wrapper(message: types.Message):
    text = await cmd_add(dp, message, message.from_user.id)
    await message.answer(text)


@dp.message_handler(commands=['restart'])
async def cmd_add_wrapper(message: types.Message):
    text = await restart(dp, message.from_user.id)
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
