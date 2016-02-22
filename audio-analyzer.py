import json
import sys
from collections import Counter

from nltk import RegexpTokenizer
from nltk.stem.snowball import RussianStemmer

counter = Counter()
tokenizer = RegexpTokenizer(r"[A-Za-zА-Яа-я]+")
stemmer = RussianStemmer()

musicFileName = sys.argv[0]
with open(musicFileName, "r") as file:
	for line in file:
		jsonData = json.loads(line, encoding="utf8")
		for song in jsonData.values()[0]:
			key = "".join([stemmer.stem(token).lower() for token in tokenizer.tokenize("{} {}".format(song["artist"], song["title"]))])
			counter[key] += 1

for item in counter.most_common():
	print(item)
