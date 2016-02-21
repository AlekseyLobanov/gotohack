import json
import sys
from nltk.stem.snowball import RussianStemmer
from nltk.tokenize import RegexpTokenizer

# load pazans
pazansGroups = None

pazansFileName = sys.argv[2]
with open(pazansFileName) as file:
	pazansGroups = json.loads(file.read())

# analyze statues
statusStats = dict()

tokenizer = RegexpTokenizer(r"[A-Za-zА-Яа-я]+")
stemmer = RussianStemmer()

usersFileName = sys.argv[1]
with open(usersFileName) as file:
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
with open(sys.argv[3], "w", encoding="utf-8") as file:
	for item in sorted(statusStats.items(), key=lambda item: item[1]["count-boys"] + item[1]["count-girls"], reverse=True):
		file.write(item[1]["full"] + "\n")
		file.write("\tboys: " + str(item[1]["count-boys"]) + "\n")
		file.write("\tgirls: " + str(item[1]["count-girls"]) + "\n")
