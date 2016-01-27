#!/usr/bin/python3

# clumping factor test. Creates a forest with certain size and terrain regularity based on settings
# Copyright Thomas van der Berg 2016, released under GNU GPLv3(see LICENSE)

import random

# settings
w = 25 # width of world
h = 21 # height of world
trees = 75 # number of trees in forest. If more than num of tiles in world, rest is ignored
clumping_factor = 1.5 # higher: more round and regular terrain, lower: more irregular terrain. should be > 0.0
four_border = False # use four border tiles instead of 8. Makes things square

# data
_map = [] # map to print on terminal
forest = set() # coordinates of trees already selected
forest_border = dict() # keys: coordinates of empty spaces next to trees. values: weights(used to put more trees here)
max_weight = 0 # sum of all weights

def out_of_bounds(x, y):
    return (x < 0 or x >= w or y < 0 or y >= h)

def create_forest(x, y):
    global max_weight
    if out_of_bounds(x, y):
        print("ERROR!", x, "and", y, "out of bounds!")
        return False
    _map[y][x] = '#'
    if (x, y) in forest_border:
        max_weight -= forest_border[(x, y)]
        del forest_border[(x, y)]
    forest.add((x, y))
    try_add_forest_border(x - 1, y)
    try_add_forest_border(x + 1, y)
    try_add_forest_border(x, y - 1)
    try_add_forest_border(x, y + 1)
    if not four_border:
        try_add_forest_border(x - 1, y - 1)
        try_add_forest_border(x + 1, y - 1)
        try_add_forest_border(x - 1, y + 1)
        try_add_forest_border(x + 1, y + 1)
    return True

def try_add_forest_border(x, y):
    global max_weight
    if not out_of_bounds(x, y) and (x, y) not in forest:
        if (x, y) not in forest_border:
            forest_border[(x, y)] = 1
            max_weight += 1
        else:
            weight = forest_border[(x, y)]
            max_weight -= weight
            weight *= clumping_factor
            max_weight += weight
            forest_border[(x, y)] = weight

# initialize map
for y in range(h):
    _map.append(['.'] * w)

# initial tree
create_forest(w // 2, h // 2)

# create every tree
for tree in range(1, trees):
    if len(forest_border) == 0:
        break
    random_factor = random.uniform(0, max_weight)
    found = False
    for place in forest_border.items():
        random_factor -= place[1]
        if random_factor < 0:
            tile = place[0]
            found = True
            break
    if found:
        create_forest(tile[0], tile[1])
    else:
        print("Error placing tree")

# print map
for y in range(h):
    print(" ".join(_map[y]))
