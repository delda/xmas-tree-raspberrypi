from tree import RGBXmasTree
from time import sleep
import sys
from colorzero import Hue, Color
from random import randint, random, choice

tree = RGBXmasTree()
tree.brightness = 0.05

def main(tree):
    switch_case = {
        1: red_green_blue,
    }
    while True:
        duration = randint(5, 20)
        current = randint(1, len(switch_case))
        switch_case[current](duration)

def red_green_blue(duration):
    colors = [Color('red'), Color('green'), Color('blue')]
    seconds = 0
    while seconds < duration:
        for color in colors:
            tree.color = color
            sleep(1)
            seconds += 1

try:
    main(tree)
    tree.off()
except KeyboardInterrupt:
    tree.off()
    sys.exit(0)

