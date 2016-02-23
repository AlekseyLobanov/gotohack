#!/usr/bin/python3
# -*- coding: utf-8 -*- 

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
pazan_groups = vk.method('groups.getById', {'group_ids': req_s})
f_publs_norm = open('full_publs_norm.txt')
for q in pazan_groups:
    f_publs_norm.writelines(str(q['id']))
    print(str(q['id']))
print(req_s)
