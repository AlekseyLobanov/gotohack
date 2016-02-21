#!/usr/bin/python
# -*- coding: utf-8 -*- 
'''
pazan_groups.py IDS_LIST FOLDER_WITH_PUBLICS OUTPUT_FILE
where FOLDER_WITH_PUBLICS folder with files with one id of group per line
'''
import sys
import json
import os
from os.path import join

all_ids = set([int(i) for i in open(sys.argv[1]).read().split()])

paz_ids = {} # id -> pazan groups

for dirpath, dirnames, filenames in os.walk(sys.argv[2]):
    for f in filenames:
        fp = os.path.join(dirpath, f)
        cur_publ_ids = set([int(i) for i in open(fp).read().split()])
        good_ids = cur_publ_ids.intersection(all_ids)
        for uid in good_ids:
            if uid in paz_ids:
                paz_ids[uid].append(f)
            else:
                paz_ids[uid] = [f]

f_out = open(sys.argv[3],'w')
f_out.write(json.dumps(paz_ids))
print("There are {} pazans".format(len(paz_ids)))
