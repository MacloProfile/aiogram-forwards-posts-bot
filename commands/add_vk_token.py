import requests


# add VK token
async def cmd_token(dp, message):

    token = message.get_args()
    if is_vk_token_valid(token):
        await dp['db'].save_vk_token(message.from_user.id, token)
        return "Success"

    return "invalid token"


def is_vk_token_valid(token):
    params = {
        'access_token': token,
        'v': '5.131',  # Версия API
    }

    try:
        response = requests.get('https://api.vk.com/method/users.get', params=params)
        response.raise_for_status()
        data = response.json()

        if 'error' in data:
            return False
        else:
            return True

    except requests.RequestException:
        return False