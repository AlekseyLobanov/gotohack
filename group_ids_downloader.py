#!/usr/bin/python3
# -*- coding: utf-8 -*- 
'''
group_ids_downloader.py VK_LOGIN VK_PASSWORD APP_ID INPUT_FILENAME
where INPUT_FILENAME is file with one id of group per line
'''
import sys

import vk_api

def getIdsByGroup(group_id):
    ids = []
    res = vk.method("groups.getMembers", {"group_id":group_id,"count":1000})
    count = res['count'] - 1000
    ids += res['items']
    cur_offset = 1000
    while count > 0:
        res = vk.method("groups.getMembers", {"group_id":group_id,
            "count":1000,"offset":cur_offset, "sort":"id_asc"})
        count = count - 1000
        cur_offset += 1000
        ids += res['items']
    return ids

vk_login, vk_password = sys.argv[1], sys.argv[2]
vk = vk_api.VkApi(vk_login, vk_password, app_id=sys.argv[3])

vk.authorization()

for group_id in open(sys.argv[4]):
    group_id = group_id.strip()
    good_ids = getIdsByGroup(group_id)
    open('out/' + str(group_id),'w').write('\n'.join([str(i) for i in good_ids]))
