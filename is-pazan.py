import sys

import vk_api


vk_login, vk_password = sys.argv[1], sys.argv[2]
vk = vk_api.VkApi(vk_login, vk_password, app_id=sys.argv[3])

vk.authorization()

groups = vk.method("groups.get", {'domain': 'omrigan'})
print(groups['items'])
req_s = ''
for w in open('full_publs.txt'):
    req_s = req_s + w + ','
azaza = vk.method('groups.getById', {'group_ids': req_s})
f = open('full_publs_norm.txt')
for q in azaza:
    f.writelines(str(q['id']))
    print(str(q['id']))
print(req_s)
