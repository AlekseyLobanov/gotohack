import json
import sys
from collections import OrderedDict

import requests

vkToken = sys.argv[3]

pazanIds = None

pazansFileName = sys.argv[1]
with open(pazansFileName) as file:
	pazanIds = [int(line) for line in file]

artistStats = dict()

def save():
	with open(sys.argv[2], "w", encoding="utf-8") as file:
		data = OrderedDict(sorted(artistStats.items(), key=lambda item: item[1]["count"], reverse=True))
		file.write(json.dumps(data, sort_keys=False))
	print("saving")

try:
	for index, pazanId in enumerate(pazanIds):
		print(index)
		jsonData = requests.get("https://api.vk.com/method/{}?{}&access_token={}".format("audio.get", "owner_id={}&need_user={}&count={}".format(pazanId, 0, 100), vkToken)).json()
		if "error" not in jsonData:
			for audio in jsonData["response"][1:]:
				audioName = audio["artist"] + audio["title"]
				artistStatsItem = artistStats.get(audioName, {
					"url": audio["url"],
					"count": 0
				})
				artistStatsItem["count"] += 1
				artistStats[audioName] = artistStatsItem
		elif jsonData["error"]["error_code"] != 19:
			print(jsonData["error"])
			print("Press any key")
			input()

		if index % 10 == 0:
			save()
except Exception as e:
	print(e)

save()
