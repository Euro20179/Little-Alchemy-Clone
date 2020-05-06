import pygame;pygame.init()
from pygame.locals import *
import tkinter as tk
from tkinter import messagebox
import json
import random

with open("window.json", "r") as windowJ:
    data = json.load(windowJ)

winWidth = data["width"]
winHeight = data["height"]

defaultWH = tuple(data["itemWH"])

MFont = pygame.font.SysFont(data["font"], data["fontSize"])

pygame.mixer.music.load(r"C:\Windows\Media\tada.wav")

bgColor = tuple(data["bgColor"]) 

class Item:
    def __init__(self, name, recipe, color, WH, *args, **kwargs):
        self.width = self.height = 74
        self.name = name
        self.recipe = recipe
        self.pos = (random.randint(0, winWidth - 75), random.randint(0, winHeight - 75))
        self.WH = WH
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.WH[0], self.WH[1])
        self.color = color
        if not kwargs.get("textColor"):
            self.textColor = (0, 0, 0)
        else:
            self.textColor = kwargs["textColor"]
        self.label = MFont.render(f'{self.name}', True, self.textColor)
        self.kwargs = kwargs
        self.args = args
        self.recentlyDragged = False
    def setRect(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
    def setPos(self, x, y):
        self.pos = (x, y)
        self.setRect(self.pos[0], self.pos[1], self.WH[0], self.WH[1])
    def setRecentlyDragged(self):
        self.recentlyDragged = False if self.recentlyDragged else True
    def info(self):
        if self.kwargs.get("tags"):
            return [self.name, self.recipe] + [x for x in self.kwargs["tags"]]
        return [self.name, self.recipe, None]

def loadGame(defaultWH):
    items = []
    with open('items.json') as itemJSON:
        data = json.load(itemJSON)
    for item in data["items"]:
        WH = defaultWH
        if item.get("w"):
            WH = (item["w"], item["h"])
        if not item.get("color"):
            color = [150, 150, 150]
        else:
            color = item["color"]
        if item.get("recipe"):
            if type(item["recipe"][0]) is list:
                for r in item["recipe"]:
                    items.append(Item(item["name"], r, color, WH, tags=item.get("tags"), textColor=item.get("textColor"), image=item.get("image")))
                continue
            recipe = item["recipe"]
        else:
            recipe = [None, None]
        items.append(Item(item["name"], recipe, color, WH, tags=item.get("tags"), textColor=item.get("textColor"), image=item.get("image")))
    return items

def addItem(root, e):
    item = e.get().split(",")
    root.destroy()
    if "!all" in item:
        for x in archInv:
            inv.append(x)
        return
    for i in item:
        for x in archInv:
            if i == x.name:
                inv.append(x)
                archInv.remove(x)
                break
def getItem(root, item, e):
    item = e.get()
    root.destroy()
    for x in inv:
        if x.name == item:
            name, recipe, *tags = x.info()
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo(f'{name}', f'Name: {name}\nRecipe: {recipe[0]} + {recipe[1]}\nother: {tags}')
            break
    else:
        messagebox.showwarning("Don't Have", f"you don't have {item}\nor {item} doesn't exist ")
    root.destroy()

items = loadGame(defaultWH)
totalItems = len({x.name for x in items})

inv = [items[0], items[1], items[3], items[4]]
archInv = set()

dragging = None

xtraInfo = False
debug = False

win = pygame.display.set_mode((winWidth,winHeight))
def loadSave(file):
    try:
        with open('{}.txt'.format(file), "r") as f:
            inv.clear()
            for x in f:
                x = x[0:-1]
                for y in items:
                    if x == y.name:
                        archInv.add(y)
                        break
    except Exception as e:
        print(e)

Run = True
while Run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            Run = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                MPos = pygame.mouse.get_pos()
                for x in inv:
                    if x.rect.collidepoint(MPos):
                        if dragging:
                            dragging = None
                            x.setRecentlyDragged()
                            break
                        else:
                            dragging = x   
                            x.setRecentlyDragged()
                            break
                        print(x.recentlyDragged)

            if event.button == pygame.BUTTON_MIDDLE:
                MPos = pygame.mouse.get_pos()
                for x in inv:
                    if x.rect.collidepoint(MPos):
                        inv.remove(x)
                        if x not in archInv:
                            archInv.add(x)


            if event.button == pygame.BUTTON_RIGHT:
                MPos = pygame.mouse.get_pos()
                for x in inv:
                    if x.rect.collidepoint(MPos):
                        inv.append(Item(x.name, x.recipe, x.color, (x.WH[0], x.WH[1]), textColor=x.textColor))
                        break

            if event.button == pygame.BUTTON_WHEELDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.KMOD_SHIFT]: inc = 10
                else: inc = 1
                if keys[pygame.K_r] and r >= inc:
                    r -= inc
                if keys[pygame.K_g] and g >= inc:
                    g -= inc
                if keys[pygame.K_b] and b >= inc:
                    b -= inc
            if event.button == pygame.BUTTON_WHEELUP:
                keys = pygame.key.get_pressed()
                if keys[pygame.KMOD_SHIFT]: inc = 10
                else: inc = 1
                if keys[pygame.K_r] and r <= inc:
                    r += inc
                if keys[pygame.K_g] and g <= inc:
                    g += inc
                if keys[pygame.K_b] and b <= inc:
                    b += inc


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                root = tk.Tk()
                root.focus()
                e = tk.Entry(root)
                e.pack()
                e.focus()
                doneButton = tk.Button(root, text="done", command=lambda: addItem(root, e))
                doneButton.pack()
                root.bind("<Return>", lambda x: addItem(root, e))
                root.mainloop()
            if event.key == pygame.K_r:
                items = loadGame(defaultWH)
                totalItems = len({x.name for x in items})

            if event.key == pygame.K_s:
                fileName = input("File Name: ")
                with open('{}.txt'.format(fileName), "w") as f:
                    sitems = {x.name for x in inv} | {x.name for x in archInv}
                    for x in sitems:
                        f.write(x + "\n")

            if event.key == pygame.K_l:
                loadSave(input("file name: "))

            if event.key == pygame.K_z:
                for x in set(inv) | archInv:
                    print(x.name)

            if event.key == pygame.K_i:
                root = tk.Tk()
                item = tk.StringVar()
                e = tk.Entry(root)
                e.pack()
                e.focus()
                doneButton = tk.Button(root, text="done", command=lambda: getItem(root, item, e))
                doneButton.pack()
                root.bind("<Return>", lambda x: getItem(root, item, e))
                root.mainloop()

                        
    if Run:
        colFound = False
        
        totalItemsOwned = len({r.name for r in inv} | {r.name for r in archInv})

        with open("allItems.txt", "r") as f:
            totalItems = len(f.read().split("\n"))

        for x in inv:
            if dragging:
                if x == dragging:
                    MPos = pygame.mouse.get_pos()
                    x.setPos(MPos[0] - x.WH[0] / 2, MPos[1] - x.WH[1] / 2)
                    break
            else:
                for y in inv:
                    if y is x:
                        continue
                    if x.rect.colliderect(y.rect) or y.rect.colliderect(x.rect):
                        colFound = True
                        for place, z in enumerate(items):
                            intersect = set(z.recipe) & {x.name, y.name}
                            if (len(intersect) == 2 or (z.recipe[0] == z.recipe[1] and x.name == y.name and x.name == z.recipe[0] and x.name == z.recipe[1])):
                                if z.name not in [a.name for a in inv]:
                                    inv.append(z)
                                    pygame.mixer.music.play()

        win.fill(bgColor)
        for x in reversed(inv):
            if x.kwargs.get("image"):
                img = pygame.image.load(x.kwargs["image"])
                win.blit(img, x.pos)
            else:
                pygame.draw.rect(win, x.color, x.rect)
            win.blit(x.label, (int(x.pos[0]), int(x.pos[1])))
            win.blit(MFont.render(f'{totalItemsOwned}/{totalItems}', True, (255, 255, 255)), (0, winHeight - 20))
        pygame.display.update()