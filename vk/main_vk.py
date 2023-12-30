from vk_api import VkApi
import tg.posting
from vk.post import wait_for_posts


async def run_vk(dp, user_id, vk_channels, tg_channel):
    try:
        await main(dp, user_id, vk_channels, tg_channel)
    except KeyboardInterrupt:
        pass


async def main(dp, user_id, vk_channels, tg_channel):
    db_token = await dp['db'].get_vk_token(user_id)
    if db_token:
        access_token = db_token
    else:
        print("Токен ВК не найден в базе данных.")
        return

    vk_session = VkApi(token=access_token)
    api = vk_session.get_api()

    row = {}

    for group_id in vk_channels:
        print(group_id)

        group_id = -group_id if group_id > 0 else group_id
        wall = api.wall.get(owner_id=group_id, filter='all', extended=1, count=1)

        try:
            row.update({group_id: wall['items'][0]['id']})
        except IndexError:
            print('Error: Возможно в группе', group_id, 'нет постов')

    print('Бот ждёт постов...')

    try:
        while True:
            text_post = await wait_for_posts(api, row, 3)
            if text_post is not None:
                await tg.posting.cmd_post(text_post, int(tg_channel))

    except KeyboardInterrupt:
        exit(0)