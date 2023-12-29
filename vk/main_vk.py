from vk_api import VkApi
from vk.post import wait_for_posts


async def run_vk(cfg):
    try:
        await main(cfg)
    except KeyboardInterrupt:
        pass


async def main(cfg):
    group_ids = cfg['vk_group_ids']
    access_token = cfg['vk_token']
    delay = cfg['vk_delay']

    vk_session = VkApi(token=access_token)
    api = vk_session.get_api()

    row = {}

    for group_id in group_ids:
        group_id = -group_id if group_id > 0 else group_id
        wall = api.wall.get(owner_id=group_id, filter='all', extended=1, count=1)

        try:
            row.update({group_id: wall['items'][0]['id']})
        except IndexError:
            print('Error: Возможно в группе', group_id, 'нет постов')

    print('Бот ждёт постов...')

    try:
        await wait_for_posts(api, row, delay)
    except KeyboardInterrupt:
        exit(0)