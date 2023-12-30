import asyncio
import logging
from aiogram import Bot, Dispatcher, types

from vk import main_vk, config

cfg = config.load()

API_TOKEN = cfg['tg_token']

# channels VK - TELEGRAM
group_channel = {}

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


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
    first = text_after_command[0]
    second = text_after_command[1]
    if first != second:
        group_channel.update({text_after_command[0]: text_after_command[1]})
    print(group_channel)
    vk_task = asyncio.create_task(main_vk.run_vk(cfg, group_channel))
    await vk_task


async def main():
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
