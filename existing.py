from main import bot
from aiogram import types


async def is_valid_telegram_channel(id):
    try:
        chat_info = await bot.get_chat(chat_id=id)
        return chat_info.type == types.ChatType.CHANNEL
    except Exception as e:
        return False


async def is_vk_group_exists(api, group_id):
    try:
        group_info = api.groups.getById(group_id=group_id)
        return True
    except Exception as e:
        if e.code == 125:
            return False
        else:
            raise


