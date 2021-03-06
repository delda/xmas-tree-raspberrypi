# !/usr/bin/env python3
#
# Christmas Tree RaspberryPi is a script
# that does multiple patterns in a random order
# on Xmas Tree RaspberryPi.
#
# delda - Davide Dell'Erba
# Version: v1.4 (15/11/2021)
#
# Needs the GPIO Zero Library
#

from tree import RGBXmasTree
from time import sleep
from colorzero import Color
from random import randint, random, uniform, shuffle
from datetime import datetime, timedelta
import numpy as np
import sys


BRANCHES = [[0, 1, 2], [22, 23, 24], [19, 20, 21], [4, 5, 6], [10, 11, 12], [16, 17, 18], [13, 14, 15], [7, 8, 9]]
DOWN = 0
SECONDS_DURATION = 10
SIDES = [[0, 1, 2, 22, 23, 24], [19, 20, 21, 4, 5, 6], [12, 11, 10, 18, 17, 16], [15, 14, 13, 9, 8, 7]]
SPIRAL = [[0, 24, 19, 6, 12, 16, 15, 7], [1, 23, 20, 5, 11, 17, 14, 8], [2, 22, 21, 4, 10, 18, 9, 13], [3]]
TOP_LED = 3
UP = 1

tree = RGBXmasTree()
tree.brightness = 0.05


# all the tree with all the chromatic range
def all_colors(duration):
    hue = 1.0
    t = 0
    tree.color = Color.from_hsv(hue, 1, .4)
    finish_time = datetime.now() + timedelta(seconds=duration)
    while datetime.now() < finish_time:
        step = t % 100
        tree.color = Color.from_hsv(1 - step / 100, 1, 0.4)
        t = t + 1
        sleep(0.05)


# different color for every face with swirl effect
def circle_of_latitude(duration):
    base_colors = [Color('blue'), Color('yellow'), Color('red'), Color('green')]
    i = 0
    finish_time = datetime.now() + timedelta(seconds=duration)
    colors = [Color('white') for x in list(range(0, 25))]
    while datetime.now() < finish_time:
        i = i + 1
        for circle in SPIRAL:
            i = i + 1
            for light in circle:
                colors[light] = base_colors[i % 4]
        tree.value = colors
        sleep(0.5)


def circle_of_latitude_appear_disappear(duration):
    base_colors = [Color('blue'), Color('yellow'), Color('red'), Color('green')]
    colors = [Color('white') for x in list(range(0, 25))]
    color = 0
    finish_time = datetime.now() + timedelta(seconds=duration)
    while datetime.now() < finish_time:
        color = color + 1
        for i in range(4):
            circle = SPIRAL[i]
            for light in circle:
                colors[light] = base_colors[color % 4]
            tree.value = colors
            sleep(0.5)
        for i in reversed(range(4)):
            circle = SPIRAL[i]
            for light in circle:
                colors[light] = Color('white')
            tree.value = colors
            sleep(0.5)


# different color for every face with swirl effect
def color_side_swirl(duration):
    base_colors = [Color('blue'), Color('yellow'), Color('red'), Color('green')]
    i = 0
    finish_time = datetime.now() + timedelta(seconds=duration)
    while datetime.now() < finish_time:
        i = i + 1
        current_color = i
        colors = [Color('white') for x in list(range(0, 25))]
        for side in SIDES:
            current_color = current_color + 1
            for light in side:
                colors[light] = base_colors[current_color % 4]
        colors[TOP_LED] = Color('white')
        tree.value = colors
        sleep(0.25)


# a spiral from bottom to top with a color followed by a spiral from bottom to top with another color
def colored_spiral(duration):
    finish_time = datetime.now() + timedelta(seconds=duration)
    base_colors = [Color('blue'), Color('yellow'), Color('red'), Color('green')]
    spiral_ordered = []
    color = 0
    for parallel in SPIRAL:
        for light in parallel:
            spiral_ordered.append(light)
    while datetime.now() < finish_time:
        color = color + 1
        for light in spiral_ordered:
            tree[light].color = base_colors[color % 3]
            sleep(0.01)


# light alternate red and green
def even_and_odd(duration):
    base_colors = [Color('red'), Color('green')]
    color_idx = 0
    colors = [Color('black') for x in list(range(0, 25))]
    finish_time = datetime.now() + timedelta(seconds=duration)
    while datetime.now() < finish_time:
        for light in range(0, 25):
            colors[light] = Color(base_colors[(light + color_idx) % len(base_colors)])
        tree.value = colors
        color_idx += 1
        sleep(0.5)


# a spiral from bottom to top with white lights followed by a spiral from bottom to top with off lights
def on_off_spiral(duration):
    finish_time = datetime.now() + timedelta(seconds=duration)
    spiral_ordered = []
    for parallel in SPIRAL:
        for light in parallel:
            spiral_ordered.append(light)
    while datetime.now() < finish_time:
        for light in spiral_ordered:
            tree[light].color = Color('white')
            sleep(0.01)
        for light in spiral_ordered:
            tree[light].off()
            sleep(0.01)


# one light at time like a snake
def ordered_lights_on(duration):
    finish_time = datetime.now() + timedelta(seconds=duration)
    base_colors = [Color('blue'), Color('yellow'), Color('red'), Color('green')]
    while datetime.now() < finish_time:
        for color in base_colors:
            for light in tree:
                light.color = color


# a spiral from bottom to top with 25 different colors in order
def rainbow_spiral(duration):
    finish_time = datetime.now() + timedelta(seconds=duration)
    spiral_ordered = []
    for parallel in SPIRAL:
        for light in parallel:
            spiral_ordered.append(light)
    while datetime.now() < finish_time:
        counter = 1
        for light in spiral_ordered:
            tree[light].color = Color.from_hsv(counter / 25, 1, 1)
            counter = counter + 1
            sleep(0.01)
        sleep(3)
        tree.off()


def random_value(duration):
    finish_time = datetime.now() + timedelta(seconds=duration)
    while datetime.now() < finish_time:
        led = randint(0, 24)
        tree[led].value = Color.from_hsv(uniform(0, 1), 1, 0.4)
        sleep(0.1)


# all the tree with one color at time: red, green or blue
def red_green_blue(duration):
    finish_time = datetime.now() + timedelta(seconds=duration)
    colors = [Color('red'), Color('green'), Color('blue')]
    while datetime.now() < finish_time:
        for color in colors:
            tree.color = color
            tree[TOP_LED].color = Color('yellow')
            sleep(0.8)


# only one face illuminated at time
def single_face_swirl(duration):
    len_size = len(SIDES)
    base_colors = [Color('blue'), Color('blue'), Color('red'), Color('red'), Color('green'), Color('green')]
    color_idx = 0
    colors = [Color('black') for x in list(range(0, 25))]
    colors[TOP_LED] = Color('yellow')
    finish_time = datetime.now() + timedelta(seconds=duration)
    while datetime.now() < finish_time:
        for i in range(0, len_size):
            for light in SIDES[i % len_size]:
                colors[light] = Color(base_colors[color_idx % len(base_colors)])
            for light in SIDES[(i - 1) % len_size]:
                colors[light] = Color('black')
            tree.value = colors
            sleep(0.1)
        color_idx += 1


# a red lights go in spiral from bottom to top on a green tree
def single_light_spiral(duration):
    finish_time = datetime.now() + timedelta(seconds=duration)
    spiral_ordered = []
    for parallel in SPIRAL:
        for light in parallel:
            spiral_ordered.append(light)
    while datetime.now() < finish_time:
        for i in range(25):
            tree[spiral_ordered[i]].color = Color('red')
            tree[spiral_ordered[(i-1) % 25]].color = Color('green')
            sleep(0.01)


# single point moving like snake on the tree
def single_point(duration):
    finish_time = datetime.now() + timedelta(seconds=duration)
    tree.color = Color('green')
    previous = 3
    while datetime.now() < finish_time:
        current = randint(0, 24)
        tree[previous].value = Color('green')
        tree[current].value = Color('red')
        previous = current
        sleep(0.25)


# snake single color
def snake(duration):
    finish_time = datetime.now() + timedelta(seconds=duration)
    spiral_ordered = []
    for side in SIDES:
        for light in side:
            spiral_ordered.append(light)
    colors = [Color('red'), Color('green'), Color('blue')]
    i = 0
    while datetime.now() < finish_time:
        i = i + 1
        for light in spiral_ordered:
            tree[light].value = colors[i % 3]
            sleep(0.1)


# all the tree with sparkle lights in one of three colors (red, blue or green)
def sparkle(duration):
    color = randint(0, 2)
    base_colors = [0, 0.33, 0.66]
    brightness = [random() for x in range(len(tree))]
    toward = [randint(DOWN, UP) for x in range(len(tree))]
    finish_time = datetime.now() + timedelta(seconds=duration)
    while datetime.now() < finish_time:
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
        sleep(0.05)


def main():
    switch_case = {
        1:  red_green_blue,
        2:  all_colors,
        3:  sparkle,
        4:  color_side_swirl,
        5:  rainbow_spiral,
        6:  on_off_spiral,
        7:  colored_spiral,
        8:  circle_of_latitude,
        9:  single_point,
        10: single_light_spiral,
        11: snake,
        12: circle_of_latitude_appear_disappear,
        13: ordered_lights_on,
        14: single_face_swirl,
        15: even_and_odd,
        16: random_value,
    }
    while True:
        patterns = [x for x in range(1, len(switch_case))]
        shuffle(patterns)
        for pattern in patterns:
            now = datetime.now()
            print(pattern, ' - ', now.strftime("%d/%m/%Y %H:%M:%S"))
            switch_case[pattern](SECONDS_DURATION)


try:
    main()
    tree.off()
except KeyboardInterrupt:
    tree.off()
    sys.exit(0)
