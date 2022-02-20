import json
import pprint

with open("good.json") as file:
	data = json.load(file)
pprint.pprint(data)
print("Equipment data has been successfully retrieved.")