import numpy as np
from aocd import get_data


def part2_move(inputs: np.array, target: int):
    results = []
    diffs = abs(inputs - target)
    for index, diff in enumerate(diffs):
        step_index = 1
        move_cost = 0
        for current_unit in range(0, diff):
            move_cost += step_index
            step_index += 1
        results.append(move_cost)
    return np.array(results)


if __name__ == '__main__':
    #data = "16,1,2,0,4,2,7,1,2,14"
    data = get_data(day=7, year=2021)
    data_points = np.array([int(x) for x in data.split(',')])

    current_distance_part1 = np.inf
    current_distance_part2 = np.inf

    for current_target in range(data_points.min(), data_points.max()):
        move_fn_part1 = lambda z: abs(z - current_target)
        fuel_costs_part1 = move_fn_part1(data_points)
        fuel_cost_part1 = np.sum(fuel_costs_part1).squeeze()
        if current_distance_part1 > fuel_cost_part1:
            current_distance_part1 = fuel_cost_part1
        fuel_costs_part2 = part2_move(data_points, current_target)
        fuel_cost_part2 = np.sum(fuel_costs_part2).squeeze()
        if current_distance_part2 > fuel_cost_part2:
            current_distance_part2 = fuel_cost_part2

    print(f'Part 1 {current_distance_part1}')
    print(f'Part 2 {current_distance_part2}')
