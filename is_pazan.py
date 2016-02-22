import sys

import vk


vk_login, vk_password = sys.argv[1], sys.argv[2]
vk = vk_api.VkApi(vk_login, vk_password, app_id=sys.argv[3])

vk.authorization()