from main import bot


async def cmd_post(post, CHANNEL_ID):

    text = post.get('text', '')
    photo_url = None

    if 'attachments' in post:
        for attachment in post['attachments']:
            if attachment['type'] == 'photo':
                photo_sizes = attachment['photo']['sizes']
                photo_url = photo_sizes[-1]['url']

    if photo_url:
        await bot.send_photo(chat_id=CHANNEL_ID, photo=photo_url, caption=text)
    else:
        await bot.send_message(chat_id=CHANNEL_ID, text=text)