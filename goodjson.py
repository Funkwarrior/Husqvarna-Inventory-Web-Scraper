import json

with open("good.json") as file:
	data = json.load(file)

print("Equipment data has been successfully retrieved.")