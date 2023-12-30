from vk_api import VkApi

import tg.posting
from vk.post import wait_for_posts
from main import dp


async def run_vk(cfg, group_channel, tg_channel):
    try:
        await main(cfg, group_channel, tg_channel)
    except KeyboardInterrupt:
        pass


async def main(cfg, group_channel, tg_channel):
    group_ids = [group_channel]

    access_token = cfg['vk_token']
    delay = cfg['vk_delay']

    vk_session = VkApi(token=access_token)
    api = vk_session.get_api()

    row = {}

    for group_id in group_ids:
        group_id = int(group_id)
        group_id = -group_id if group_id > 0 else group_id
        wall = api.wall.get(owner_id=group_id, filter='all', extended=1, count=1)

        try:
            row.update({group_id: wall['items'][0]['id']})
        except IndexError:
            print('Error: Возможно в группе', group_id, 'нет постов')

    print('Бот ждёт постов...')

    try:
        while True:
            text_post = await wait_for_posts(api, row, delay)
            if text_post is not None:
                await tg.posting.cmd_post(text_post, int(tg_channel))

    except KeyboardInterrupt:
        exit(0)