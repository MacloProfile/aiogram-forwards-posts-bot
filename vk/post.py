import asyncio


async def wait_for_posts(api, row, delay):
    for i in range(1):
        for group_id, latest_post_id in row.items():
            wall = api.wall.get(owner_id=group_id, filter='all', extended=1, count=1)
            post = wall['items'][0] if wall['items'] else None

            try:
                post = wall['items'][0]
            except IndexError:
                group = wall['groups'][0]
                print('Группа', group['name'], '(vk.com/' + group['screen_name'] + ') ' +
                      'будет проигнорирована, т.к у нее больше нет постов.')

            if post and post['id'] > latest_post_id:
                row.update({group_id: post['id']})
                print("Новый пост в группе", group_id)
                return post

        await asyncio.sleep(delay)