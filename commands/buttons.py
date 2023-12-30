def text_help():
    text = "/add 'vk_id' 'tg_id' - добавить пересылку из группы вк в тг канал\n"\
           + "/token 'kate mobile token' - токен вк аккаунта из kate mobile\n"\
            + "test"
    return text


def text_profile(id):
    text = "Your Id: " + str(id)
    return text