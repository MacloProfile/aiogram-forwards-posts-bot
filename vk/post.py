import asyncio
import tg.posting


async def wait_for_posts(api, row, delay, dp):
    for group_id, latest_post_id in row.items():
        wall = api.wall.get(owner_id=group_id, filter='all', extended=1, count=1)
        post = wall['items'][0] if wall['items'] else None

        if not post:
            group = wall['groups'][0]
            print('Группа', group['name'], '(vk.com/' + group['screen_name'] + ') ' +
                  'будет проигнорирована, т.к у нее больше нет постов.')
            continue

        if post['id'] > latest_post_id:
            row.update({group_id: post['id']})
            print("Новый пост в группе", group_id)
            if post is not None:
                tg_channels = await dp['db'].take_tg_by_vk(group_id * -1)
                for tg_id in tg_channels:
                    await tg.posting.cmd_post(post, tg_id)

    await asyncio.sleep(delay)
