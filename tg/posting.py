from main import bot
import yt_dlp
import os


async def cmd_post(post, CHANNEL_ID):
    try:
        text = post.get('text', '')
        photo_url = None
        video_url = None

        if 'attachments' in post:
            for attachment in post['attachments']:
                if attachment['type'] == 'photo':
                    photo_sizes = attachment['photo']['sizes']
                    photo_url = photo_sizes[-1]['url']

                elif attachment['type'] == 'video':
                    owner_id = post['attachments'][0]['video']['owner_id']
                    video_id = post['attachments'][0]['video']['id']
                    video_url = f"https://vk.com/video{owner_id}_{video_id}"

        if photo_url:
            await bot.send_photo(chat_id=CHANNEL_ID, photo=photo_url, caption=text)
        elif video_url is not None:
            await send_video(CHANNEL_ID, video_url, text)
        elif text:
            await bot.send_message(chat_id=CHANNEL_ID, text=text)

    except Exception as e:
        print(f"Ошибка: {e}")


async def send_video(channel_id, video_url, text):
    try:
        video_path = download_video(video_url)
        with open(video_path, 'rb') as video_file:
            await bot.send_video(channel_id, video_file, caption=text)
        os.remove(video_path)
    except Exception as e:
        print(f"Ошибка при отправке видео: {e}")


def download_video(video_url):
    try:
        ydl_opts = {'outtmpl': 'downloads/%(title)s.%(ext)s', 'progress_hooks': [], 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            return os.path.join('downloads', f"{info['title']}.{info['ext']}")
    except:
        print("Произошла ошибка при скачивании видео")
        return None
