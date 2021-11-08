from tree import RGBXmasTree
from time import sleep
import sys
from colorzero import Hue, Color
from random import randint, random, choice

TOP_LED = 3

tree = RGBXmasTree()
tree.brightness = 0.05


def red_green_blue(duration):
    colors = [Color('red'), Color('green'), Color('blue')]
    seconds = 0
    while seconds < duration:
        for color in colors:
            tree.color = color
            tree[TOP_LED].color = Color('white')
            sleep(1)
            seconds += 1



def main():
    switch_case = {
        1: red_green_blue,
        2: all_colors,
        3: sparkle,
    }
    while True:
        duration = randint(5, 20)
        current = randint(1, len(switch_case))
        current = 3
        switch_case[current](duration)


try:
    main()
    tree.off()
except KeyboardInterrupt:
    tree.off()
    sys.exit(0)
