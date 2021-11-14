from tree import RGBXmasTree
from time import sleep
from colorzero import Hue, Color
from random import randint, random, choice
from datetime import datetime
import sys


DOWN = 0
BRANCHES = [[0, 1, 2], [22, 23, 24], [19, 20, 21], [4, 5, 6], [10, 11, 12], [16, 17, 18], [13, 14, 15], [7, 8, 9]]
SIDES = [[0, 1, 2, 22, 23, 24], [19, 20, 21, 4, 5, 6], [10, 11, 12, 16, 17, 18], [13, 14, 15, 7, 8, 9]]
TOP_LED = 3
UP = 1

tree = RGBXmasTree()
tree.brightness = 0.05


def color_side_swirl(duration):
    base_colors = [Color('blue'), Color('yellow'), Color('red'), Color('green')]
    seconds = 0
    i = 0
    while seconds < duration:
        colors = [Color('white') for x in list(range(0, 25))]
        for side in SIDES:
            for light in side:
                colors[light] = base_colors[i % 4]
            i = i + 1
        i = i + 1
        colors[TOP_LED] = Color('white')
        tree.value = colors
        sleep(0.5)
        seconds += 1


def all_colors(duration):
    hue = 1.0
    t = 0
    tree.color = Color.from_hsv(hue, 1, .4)
    while t < duration * 8:
        step = t % 100
        tree.color = Color.from_hsv(1 - step / 100, 1, 0.4)
        t = t + 1
        sleep(0.05)


def red_green_blue(duration):
    colors = [Color('red'), Color('green'), Color('blue')]
    seconds = 0
    while seconds < duration:
        for color in colors:
            tree.color = color
            tree[TOP_LED].color = Color('white')
            sleep(0.8)
            seconds += 1


def sparkle(duration):
    t = 0
    color = randint(0, 2)
    base_colors = [0, 0.33, 0.66]
    brightness = [random() for x in range(len(tree))]
    toward = [randint(DOWN, UP) for x in range(len(tree))]
    while t < duration * 8:
        for i in range(len(tree)):
            if toward[i] == DOWN:
                brightness[i] = brightness[i] - 0.1
                if brightness[i] < 0.1:
                    toward[i] = UP
            else:
                brightness[i] = brightness[i] + 0.1
                if brightness[i] > 0.9:
                    toward[i] = DOWN
        colors = [Color.from_hsv(base_colors[color], 1, b) for b in brightness]
        colors[TOP_LED] = Color.from_hsv(0, 0, brightness[TOP_LED])
        tree.value = colors
        t = t + 1
        sleep(0.05)


def main():
    switch_case = {
        1: red_green_blue,
        2: all_colors,
        3: sparkle,
        4: color_side_swirl,
    }
    while True:
        duration = 10
        current = randint(1, len(switch_case))
        now = datetime.now()
        print(current)
        print(now.strftime("%d/%m/%Y %H:%M:%S"))
        switch_case[current](duration)


try:
    main()
    tree.off()
except KeyboardInterrupt:
    tree.off()
    sys.exit(0)
