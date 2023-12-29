from vk_api import VkApi
import config
from post import wait_for_posts


def main():
    cfg = config.load()

    group_ids = cfg['group_ids']
    access_token = cfg['token']
    delay = cfg['delay']

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
        wait_for_posts(api, row, delay)
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
