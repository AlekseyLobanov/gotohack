import json
import sys

import time
import vk_api

# getting pazans
pazanIds = None
pazansFileName = sys.argv[1]
with open(pazansFileName) as file:
	pazanIds = [int(line) for line in file]

# getting music
vk = vk_api.VkApi(token=sys.argv[3], app_id=sys.argv[4])

for index, pazanId in enumerate(pazanIds, start=(int(sys.argv[5]) if len(sys.argv) > 5 else 0)):
	done = False
	while not done:
		try:
			print(index)
			pazanSongs = []
			jsonData = vk.method("audio.get", {"owner_id": pazanId, "need_user": 0, "count": 100})
			for audio in jsonData["items"]:
				pazanSong = {
					"artist": audio["artist"],
					"title": audio["title"],
					"genre_id": audio.get("genre_id", None),
					"url": audio["url"],
				}
				pazanSongs.append(pazanSong)
			with open(sys.argv[2], "a", encoding="utf-8") as file:
				file.write(json.dumps({pazanId: pazanSongs}, ensure_ascii=False) + "\n")
			done = True
		except vk_api.ApiError as e:
			if e.code == 9:
				print("waiting")
				time.sleep(60)
			elif e.code == 201 or e.code == 15:
				done = True
			else:
				raise e
