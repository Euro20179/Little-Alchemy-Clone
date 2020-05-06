import numpy as np

with open("allItems.txt", "r") as f:
    allItems = f.read().split("\n")

with open("allItems2.txt", "r") as f2:
    allItems2 = f2.read().split("\n")

input(np.setdiff1d(allItems, allItems2))

