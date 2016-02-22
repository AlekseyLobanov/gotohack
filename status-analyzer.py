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
pazansGroups = None

pazansFileName = sys.argv[1]
with open(pazansFileName, "r") as file:
	pazansGroups = json.loads(file.read())

# analyze statues
statusStats = dict()

tokenizer = RegexpTokenizer(r"[A-Za-zА-Яа-я]+")
stemmer = RussianStemmer()

usersFileName = sys.argv[2]
with open(usersFileName, "r") as file:
	for line in file:
		user = json.loads(line)
		id = str(user["_id"])
		if id in pazansGroups:
			pazanGroups = pazansGroups[id]
			statusText = user.get("status", "")
			filteredStatusText = "".join([stemmer.stem(token).lower() for token in tokenizer.tokenize(statusText)])
			if len(filteredStatusText) > 1:
				statusStatsItem = statusStats.get(filteredStatusText, {
					"full": statusText,
					"count-boys": 0,
					"count-girls": 0,
				})
				statusStatsItem["count-boys"] += len(pazanGroups) * (1 if user["sex"] == 2 else 0)
				statusStatsItem["count-girls"] += len(pazanGroups) * (1 if user["sex"] == 1 else 0)
				statusStats[filteredStatusText] = statusStatsItem

# print result
destFileName = sys.argv[3]
with open(destFileName, "w", encoding="utf8") as file:
	sortKeyGetter = lambda item: item[1]["count-boys"] + item[1]["count-girls"]
	sortedStatues = [item[1] for item in sorted(statusStats.items(), key=sortKeyGetter, reverse=True)]
	data = OrderedDict([(item["full"], dictWithoutOneKey(item, "full")) for item in sortedStatues])
	file.write(json.dumps(data, ensure_ascii=False, indent=4))
