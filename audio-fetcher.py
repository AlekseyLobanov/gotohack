#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import json
import sys
import time

import vk_api


def captcha_handler(captcha):
	key = input("Enter Captcha {0}: ".format(captcha.get_url())).strip()
	return captcha.try_again(key)

# getting pazans
pazanIds = None
pazansFileName = sys.argv[1]
with open(pazansFileName, "r") as file:
	jsonData = json.loads(file.read())
	pazanIds = [item[0] for item in sorted(jsonData.items(), key=lambda item: len(item[1]), reverse=True)]

vk = vk_api.VkApi(token=sys.argv[3], app_id=sys.argv[4], captcha_handler=captcha_handler)

for index, pazanId in enumerate(pazanIds, start=(int(sys.argv[5]) if len(sys.argv) > 5 else 0)):
	done = False
	while not done:
		try:
            pazanSongs = []
            
			print(index, pazanId)
			
			jsonData   = vk.method("execute.getMusic", {"id": pazanId})
			for audio in jsonData["items"]:
				pazanSong = {
					"artist"  : audio["artist"],
					"title"   : audio["title"],
					"genre_id": audio.get("genre_id", None),
					"url"     : audio["url"],
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
