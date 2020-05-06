import collections

with open("allItems.txt", "r") as f:
    allItems = f.read().split("\n")

input([item for item, count in collections.Counter(allItems).items() if count > 1])