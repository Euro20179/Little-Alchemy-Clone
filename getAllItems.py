import json

with open("items.json", "r") as iJ:
    data = json.load(iJ)

names = [n["name"] for n in data["items"]]

with open("allItems.txt", "w") as f:
    for i in names:
        f.write(f'{i}\n')