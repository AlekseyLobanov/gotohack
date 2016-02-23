#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import json
import sys

from nltk               import RegexpTokenizer, OrderedDict
from nltk.stem.snowball import RussianStemmer

genres = {
	1:  "Rock",
	2:  "Pop",
	3:  "Rap & Hip - Hop",
	4:  "Easy Listening",
	5:  "Dance & House",
	6:  "Instrumental",
	7:  "Metal",
	21: "Alternative",
	8:  "Dubstep",
	9:  "Jazz & Blues",
	10: "Drum & Bass",
	11: "Trance",
	12: "Chanson",
	13: "Ethnic",
	14: "Acoustic & Vocal",
	15: "Reggae",
	16: "Classical",
	17: "Indie Pop",
	19: "Speech",
	22: "Electropop & Disco",
	18: "Other"
}


def dictWithoutOneKey(d, key):
	new_d = d.copy()
	new_d.pop(key)
	return new_d

if __name__ == '__main__':
    musicFileName = sys.argv[1]
    destFileName  = sys.argv[2]

    tokenizer = RegexpTokenizer(r"[A-Za-zА-Яа-я]+")
    stemmer   = RussianStemmer()

    audioStats = dict()

    with open(musicFileName, "r", encoding="utf8") as f_music:
        for line in f_music:
            jsonData = json.loads(line, encoding="utf8")
            for song in list(jsonData.values())[0]:
                songName = "{} - {}".format(song["artist"], song["title"])
                filteredSongName = "".join(
                    [stemmer.stem(token).lower() for token in tokenizer.tokenize(songName)]
                )
                if len(filteredSongName) > 1:
                    audioStatsItem = audioStats.get(filteredSongName, {
                        "name": songName,
                        "url": song["url"],
                        "genre": genres.get(song["genre_id"], "Other"),
                        "count": 0
                    })
                    audioStatsItem["count"] += 1
                    audioStats[filteredSongName] = audioStatsItem

    with open(destFileName, "w", encoding="utf-8") as f_out:
        sortedSongs = [item[1] for item in sorted(audioStats.items(), key=lambda item: item[1]["count"], reverse=True)]
        data = OrderedDict([(item["name"], dictWithoutOneKey(item, "name")) for item in sortedSongs])
        f_out.write(json.dumps(data, ensure_ascii=False, indent=4))
