import commands.forward_from_vk


def text_help():
    text = "/add 'vk_id' 'tg_id' - добавить пересылку из группы вк в тг канал\n"\
           + "/token 'kate mobile token' - токен вк аккаунта из kate mobile\n"\
            + "test"
    return text


def text_profile(id):
    text = "Your Id: " + str(id)
    return text


async def restart(dp, user_id):
    tg_channel = await dp['db'].take_tg(user_id)
    vk_channels = await dp['db'].take_vk(user_id)
    try:
        await commands.forward_from_vk.restart_vk_task(dp, user_id, vk_channels)
    except Exception as e:
        return "error"
    return "Success!"