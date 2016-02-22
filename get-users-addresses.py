#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""
get_users_addresses.py SCHOOL_IDS_FILE ADDRESSES_FILE USERS_IDS_JSON FULL_BASE_FILE OUTPUT_FILE
"""
import sys
import csv
import json
from urllib.parse import quote_plus


import requests

def getCoords(name):
    r = requests.get('https://geocode-maps.yandex.ru/1.x/?geocode='+quote_plus(name) + '&format=json')
    points = r.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()[::-1]
    return tuple([float(x) for x in points])


school_ids = {}
cnt = 0
with open(sys.argv[1],'r') as f:
    reader = csv.reader(f)
    for row in reader:
        cnt += 1
        if cnt == 1:
            continue
        if len(row[0].strip()) == 0 or len(row[3].strip()) == 0:
            continue
        school_ids[int(row[3])] = row[0]

addresses = {}
cnt = 0
with open(sys.argv[2],'r') as f:
    reader = csv.reader(f)
    for row in reader:
        cnt += 1
        if cnt == 1:
            continue
        if len((row[3] + row[2]).strip()) > 0:
            addresses[row[0]] = {"coord":(row[3],row[2]),"address":row[1]}
        else:
            addresses[row[0]] = {"coord":getCoords('Москва ' + row[1]),"address":row[1]}

pazans = json.loads(open(sys.argv[3]).read())

pazan_ids = set([int(i) for i in pazans.keys()])

pazan_schools = {}

print(sys.argv[4])
for line in open(sys.argv[4]):
    json_line = json.loads(line)
    uid = int(json_line['_id'])
    if uid in pazan_ids:
        if 'schools' not in json_line or len(json_line['schools']) == 0:
            continue
        school_id = int(json_line['schools'][-1]['id'])
        if school_id not in school_ids:
            continue
        school_name = school_ids[school_id]
        if school_name not in addresses:
            continue
        pazan_schools[uid] = addresses[school_name]

f_out = open(sys.argv[5],'w')
f_out.write(json.dumps(pazan_schools))
print("There are {} pazans with school".format(len(pazan_schools)))
