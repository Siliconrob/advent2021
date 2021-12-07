import numpy as np
from aocd import get_data
from collections import deque

if __name__ == '__main__':
    #data = "3,4,3,1,2"
    data = get_data(day=6, year=2021)
    fish = np.array([int(x) for x in data.split(',')])
    current_fish_count = fish.size

    # the hard way grows the list exponentially
    for day in range(80):
        move_day = lambda z: z - 1
        fish = move_day(fish)
        new_fish_count = (fish < 0).sum()
        to_add = []
        for x in range(new_fish_count):
            to_add.append(8)
        if len(to_add) > 0:
            fish = np.append(fish, to_add)
        fish = np.where(fish < 0, 6, fish)
    print(f'Part 1: {fish.size}')

    # only care about the day totals so move that along
    fish = [int(x) for x in data.split(',')]
    sums = [sum(map(lambda x: x == spawn_day, fish)) for spawn_day in range(9)]
    spawn_day_totals = deque(sums)
    for day in range(256):
        to_add = spawn_day_totals[0]
        spawn_day_totals.rotate(-1)
        spawn_day_totals[6] += to_add
    print(f'Part 2: {sum(spawn_day_totals)}')