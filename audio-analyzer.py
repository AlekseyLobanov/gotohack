import json
import sys
import pymongo

pazanIds = None

pazansFileName = sys.argv[1]
with open(pazansFileName) as file:
	pazanIds = json.loads(file.read()).keys()

artistStats = dict()

audioCollection = pymongo.MongoClient("goto.reproducible.work")["vk"]["audio"]
for pazanId in pazanIds:
	for audio in audioCollection.find({"owner_id": pazanId}, {"artist": 1, "title": 1, "url": 1}):
		audioName = audio["artist"] + audio["title"]
		artistStatsItem = artistStats.get(audioName, {
			"url": audio["url"],
			"count": 0
		})
		artistStatsItem["count"] += 1
		artistStats[audioName] = artistStatsItem

with open(sys.argv[2], "w", encoding="utf-8") as file:
	for item in sorted(artistStats.items(), key=lambda item: item[1]["count"], reverse=True):
		file.write(item[0] + "\n")
		file.write("\tcount: " + str(item[1]["count"]) + "\n")
		file.write("\turl: " + str(item[1]["url"]) + "\n")
