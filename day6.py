import numpy as np
from aocd import get_data

if __name__ == '__main__':
    #data = "3,4,3,1,2"
    data = get_data(day=6, year=2021)
    fish = np.array([int(x) for x in data.split(',')])
    current_fish_count = fish.size

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