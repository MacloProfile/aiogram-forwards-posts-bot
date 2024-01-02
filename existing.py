import vk_api
import requests

def download_vk_video(video_url, output_path='download/video.mp4'):
    try:
        # Разбираем URL видео и получаем необходимую информацию
        video_id = video_url.split('_')[1].split('?')[0]
        owner_id = video_url.split('-')[1].split('_')[0]

        # Авторизация в VK
        vk_session = vk_api.VkApi(token='vk1.a.zhhZwm56ortt3aDydy8tHQr_fssb3snptMlgTOL2LBvJpC-1AKQ8n47QEa-rwvy_y5PFlaYc30K-0AEIQrHgXGMC8DD9HMmcSyXXzi_qBAC6vhvnCTT7eGpzxqPhtXS8cz2xJICdKNieLyfV3E3hk8SSXoTHnUlU9CJ0y4rL4_-vwyXwyPlp_pZ05z6PMYlCqssBSRbRwNvBLu0lrxRoRQ')  # Замените 'YOUR_ACCESS_TOKEN' на ваш токен VK
        vk = vk_session.get_api()

        # Получаем информацию о видео
        video_info = vk.video.get(owner_id=owner_id, videos=owner_id + '_' + video_id, extended=1)

        if 'items' in video_info and len(video_info['items']) > 0:
            # Получаем прямую ссылку на видео
            direct_url = video_info['items'][0]['player']

            # Скачиваем видео
            response = requests.get(direct_url)
            if response.status_code == 200:
                with open(output_path, 'wb') as video_file:
                    video_file.write(response.content)
                print(f"Видео успешно скачано и сохранено по пути: {output_path}")
            else:
                print(f"Не удалось скачать видео. Статус код: {response.status_code}")
        else:
            print("Не удалось получить информацию о видео. Проверьте правильность URL.")
    except Exception as e:
        print(f"Произошла ошибка при получении информации о видео: {e}")

# Пример использования
video_url = 'https://vk.com/video-223802102_456239075?list=f51cf7450373fd0705'
download_vk_video(video_url)
