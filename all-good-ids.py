#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import sys
import json
import os

all_ids = {}

for dirpath, dirnames, filenames in os.walk(sys.argv[1]):
    for f in filenames:
        fp = os.path.join(dirpath, f)
        for uid in open(fp):
            uid = int(uid)
            if uid in all_ids:
                all_ids[uid] += 1
            else:
                all_ids[uid] = 1

f_out = open(sys.argv[2],'w')
f_out.write(json.dumps(all_ids))
