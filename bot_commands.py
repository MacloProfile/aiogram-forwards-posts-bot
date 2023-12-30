import asyncio

current_vk_task = None


async def cmd_add(dp, message, cfg):
    from vk import main_vk

    global current_vk_task

    text_after_command = message.get_args().split(" ")
    first = int(text_after_command[0])
    second = int(text_after_command[1])

    if current_vk_task:
        current_vk_task.cancel()

    if first != second:
        await dp['db'].save_channel_to_db(first, second)
        print("Data saved to the database")

    tg_channel = (await dp['db'].take_tg())
    vk_channels = await dp['db'].take_vk(tg_channel)

    current_vk_task = asyncio.create_task(main_vk.run_vk(cfg, vk_channels, tg_channel))
    await current_vk_task
