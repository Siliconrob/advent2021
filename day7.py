import numpy as np
from aocd import get_data

if __name__ == '__main__':
    #data = "16,1,2,0,4,2,7,1,2,14"
    data = get_data(day=7, year=2021)
    data_points = np.array([int(x) for x in data.split(',')])
    data_points.sort()

    current_distance_part1 = np.inf
    current_distance_part2 = np.inf

    for current_target in range(data_points.min(), data_points.max()):
        move_fn_part1 = lambda z: abs(z - current_target)
        fuel_costs_part1 = move_fn_part1(data_points)
        fuel_cost_part1 = np.sum(fuel_costs_part1).squeeze()
        if current_distance_part1 > fuel_cost_part1:
            current_distance_part1 = fuel_cost_part1
    print(f'Part 1 {current_distance_part1}')
    print(f'Part 2 {current_distance_part2}')
