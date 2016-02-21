import re
import sys
import os
import pymongo

dirWithIds = sys.argv[1]

pazansMongo = pymongo.MongoClient("equal.cf")
pazansDb = pazansMongo['pazans']
pazansCollection = pazansDb['pazans']

# gotoMongo = pymongo.MongoClient("goto.reproducible.work")
# gotoDb = gotoMongo['vk']
# gotoUserCollection = gotoDb['users']
usersJsonFile = sys.argv[2]

ids = set()

idsFile = sys.argv[3]
if not os.path.isfile(idsFile):
	idsRegex = re.compile('\\"_id\\": (.+?),')
	with open(usersJsonFile, "r") as fileName:
		for line in fileName:
			groups = idsRegex.search(line)
			id = int(groups.group(1))
			ids.add(id)

	with open(idsFile, "w") as fileName:
		for id in ids:
			fileName.write(str(id) + "\n")
else:
	with open(idsFile, "r") as fileName:
		for line in fileName:
			ids.add(int(line))

for fileName in os.listdir(dirWithIds):
	print("parsing", fileName)

	with open(os.path.join(dirWithIds, fileName)) as file:
		for line in file:
			id = int(line)
			if id in ids:
				pazan = pazansCollection.find_one(id)
				if pazan is None:
					pazansCollection.insert_one({"_id": id, "groups": [fileName]})
				elif fileName not in pazan["groups"]:
					pazan["groups"].append(fileName)
					pazansCollection.update_one(
							{"_id": pazan["_id"]},
							{"$set": {"groups": pazan["groups"]}}
					)

	print("- done")
