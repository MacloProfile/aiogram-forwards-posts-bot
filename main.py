import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
BOT_TOKEN = config.get('token')

if BOT_TOKEN is None:
    raise ValueError("Токен не найден в файле config.json")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Я эхо-бот. Отправь мне что-нибудь, и я повторю.")


@dp.message_handler()
async def echo_message(message: types.Message):
    await message.reply(message.text)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
