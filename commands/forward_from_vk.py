import asyncio

current_vk_task = None


async def restart_vk_task(dp, user_id, vk_channels, tg_channel):
    from vk import main_vk
    global current_vk_task

    if current_vk_task:
        current_vk_task.cancel()

    current_vk_task = asyncio.create_task(main_vk.run_vk(dp, user_id, vk_channels, tg_channel))
    return current_vk_task


async def cmd_add(dp, message, user_id):

    text_after_command = message.get_args().split(" ")
    first = int(text_after_command[0])
    second = int(text_after_command[1])

    # unique pair
    channel_pair_exists = await dp['db'].check_channel_pair_exists(second, first)
    if channel_pair_exists:
        return "Values already exist in the database"

    tg_channel = await dp['db'].take_tg()
    vk_channels = await dp['db'].take_vk(tg_channel)

    # Restart the task with new parameters
    await restart_vk_task(dp, user_id, vk_channels, tg_channel)
    return "Great!"