#!/usr/bin/python
# -*- coding: utf-8 -*- 

import sys
import os
from os.path import join

all_ids = set()

for dirpath, dirnames, filenames in os.walk(sys.argv[1]):
    for f in filenames:
        fp = os.path.join(dirpath, f)
        for uid in open(fp):
            all_ids.add(int(uid))

f_out = open(sys.argv[2],'w')
for uid in all_ids:
    f_out.write(str(uid) + '\n')
