import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from vk import main_vk, config

cfg = config.load()

API_TOKEN = cfg['tg_token']

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("hi")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text, parse_mode=ParseMode.MARKDOWN)


async def main():
    vk_task = asyncio.create_task(main_vk.run_vk(cfg))

    await dp.start_polling()
    await vk_task

if __name__ == '__main__':
    asyncio.run(main())
