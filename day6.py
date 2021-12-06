import numpy as np
from aocd import get_data

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
    spawn_days = []
    for spawn_day in range(9):
        count = sum(map(lambda x: x == spawn_day, fish))
        spawn_days.append(count)

    for day in range(256):
        to_add = spawn_days[0]
        spawn_days = spawn_days[1:]
        spawn_days.append(to_add)
        spawn_days[6] += to_add
    print(f'Part 2: {sum(spawn_days)}')


