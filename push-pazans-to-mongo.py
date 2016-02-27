#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os
import re
import sys

import pymongo


dirWithIds = sys.argv[1]

pazansMongo      = pymongo.MongoClient("equal.cf")
pazansDb         = pazansMongo['pazans']
pazansCollection = pazansDb['pazans']

# gotoMongo = pymongo.MongoClient("goto.reproducible.work")
# gotoDb = gotoMongo['vk']
# gotoUserCollection = gotoDb['users']
usersJsonFile = sys.argv[2]

ids = set()

idsFile = sys.argv[3]
if not os.path.isfile(idsFile):
    idsRegex = re.compile('\\"_id\\": (.+?),')
    with open(usersJsonFile, "r") as file_name:
        for line in file_name:
            groups = idsRegex.search(line)
            uid = int(groups.group(1))
            ids.add(uid)

    with open(idsFile, "w") as file_name:
        for uid in ids:
            file_name.write(str(uid) + "\n")
else:
    with open(idsFile, "r") as f_ids:
        for line in f_ids:
            f_ids.add(int(line))

for file_name in os.listdir(dirWithIds):
    print("parsing {}".format(file_name))

    with open(os.path.join(dirWithIds, file_name), "r") as f_out:
        for line in f_out:
            uid = int(line)
            if uid in ids:
                pazan = pazansCollection.find_one(uid)
                if pazan is None:
                    pazansCollection.insert_one({"_id": uid, "groups": [file_name]})
                elif file_name not in pazan["groups"]:
                    pazan["groups"].append(file_name)
                    pazansCollection.update_one(
                            {"_id": pazan["_id"]},
                            {"$set": {"groups": pazan["groups"]}}
                    )

    print("- done")
