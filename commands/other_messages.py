import re

import vk_api


def get_vk_id(vk_link, access_token):
    match = re.search(r'^https:\/\/vk\.com\/(?P<group_name>[a-zA-Z0-9_]+)$', vk_link)
    if match:
        group_name = match.group('group_name')

        vk_session = vk_api.VkApi(token=access_token)

        try:
            group_info = vk_session.method('groups.getById', {'group_ids': group_name})
            if group_info:
                group_id = group_info[0]['id']
                return group_id
        except vk_api.VkApiError as e:
            print(f"Ошибка VK API: {e}")

    return None