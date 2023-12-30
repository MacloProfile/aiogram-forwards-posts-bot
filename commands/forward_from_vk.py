import asyncio

current_vk_task = None


async def cmd_add(dp, message, user_id):
    from vk import main_vk
    from existing import is_valid_telegram_channel

    global current_vk_task

    text_after_command = message.get_args().split(" ")
    first = int(text_after_command[0])
    second = int(text_after_command[1])

    # unique pair
    channel_pair_exists = await dp['db'].check_channel_pair_exists(second, first)
    if channel_pair_exists:
        return "Values already exist in the database"

    # cancel previous cycle
    if current_vk_task:
        current_vk_task.cancel()

    await dp['db'].save_channel_to_db(first, second)
    print("Data saved to the database")

    tg_channel = (await dp['db'].take_tg())
    vk_channels = await dp['db'].take_vk(tg_channel)

    current_vk_task = asyncio.create_task(main_vk.run_vk(dp, user_id, vk_channels, tg_channel))
    await current_vk_task
    return "great!"
