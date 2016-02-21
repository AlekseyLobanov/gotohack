import json
import sys
from collections import OrderedDict
import vk_api

artistStats = dict()


def save():
	with open(sys.argv[2], "w", encoding="utf-8") as file:
		data = OrderedDict(sorted(artistStats.items(), key=lambda item: item[1]["count"], reverse=True))
		file.write(json.dumps(data, sort_keys=False))
	print("saving")


# getting pazans
pazanIds = None
pazansFileName = sys.argv[1]
with open(pazansFileName) as file:
	pazanIds = [int(line) for line in file]

# getting music
vk = vk_api.VkApi(token=sys.argv[3], app_id=sys.argv[4])

for index, pazanId in enumerate(pazanIds, start=(sys.argv[5] if len(sys.argv) > 5 else 0)):
	try:
		print(index)
		jsonData = vk.method("audio.get", {"owner_id": pazanId, "need_user": 0, "count": 100})
		for audio in jsonData["items"]:
			audioName = audio["artist"] + " - " + audio["title"]
			artistStatsItem = artistStats.get(audioName, {
				"url": audio["url"],
				"genre_id": audio.get("genre_id", ""),
				"count": 0
			})
			artistStatsItem["count"] += 1
			artistStats[audioName] = artistStatsItem

		if index % 100 == 0:
			save()
	except vk_api.ApiError as e:
		if e.code != 201:
			print(e)
			break
	except Exception as e:
		print(e)
		break

save()
