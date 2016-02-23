#!/usr/bin/python
# -*- coding: utf-8 -*- 

import json
import sys
from collections import OrderedDict

from nltk.stem.snowball import RussianStemmer
from nltk.tokenize import RegexpTokenizer


def dictWithoutOneKey(d, key):
	new_d = d.copy()
	new_d.pop(key)
	return new_d


# load pazans
pazans_groups = None

pazans_file_name = sys.argv[1]
with open(pazans_file_name, "r") as file:
	pazans_groups = json.loads(file.read())

# analyze statues
status_stats = dict()

tokenizer = RegexpTokenizer(r"[A-Za-zА-Яа-я]+")
stemmer   = RussianStemmer()

users_file_name = sys.argv[2]
with open(users_file_name, "r") as file:
	for line in file:
		user = json.loads(line)
		uid = str(user["_id"])
		if uid in pazans_groups:
			pazan_groups = pazans_groups[uid]
			status_text  = user.get("status", "")
			filtered_status_text = "".join([stemmer.stem(token).lower() for token in tokenizer.tokenize(status_text)])
			if len(filtered_status_text) > 1:
				status_stats_item = status_stats.get(filtered_status_text, {
					"full": status_text,
					"count-boys": 0,
					"count-girls": 0,
				})
                if user["sex"] == 2:
                    status_stats_item["count-boys"]  += len(pazan_groups)
                if user["sex"] == 1:
                    status_stats_item["count-girls"] += len(pazan_groups)
				status_stats[filteredstatus_text] = status_stats_item

# print result
dest_file_name = sys.argv[3]
with open(dest_file_name, "w", encoding="utf-8") as file:
	sortKeyGetter = lambda item: item[1]["count-boys"] + item[1]["count-girls"]
	sortedStatues = [item[1] for item in sorted(status_stats.items(), key=sortKeyGetter, reverse=True)]
	data = OrderedDict([(item["full"], dictWithoutOneKey(item, "full")) for item in sortedStatues])
	file.write(json.dumps(data, ensure_ascii=False, indent=4))
