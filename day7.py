import types
import numpy as np
from aocd import get_data


def part2_move(inputs: np.array, target: int) -> np.array:
    results = []
    diffs = abs(inputs - target)
    for diff in diffs:
        step_index = 1
        move_cost = 0
        for current_unit in range(0, diff):
            move_cost += step_index
            step_index += 1
        results.append(move_cost)
    return np.array(results)


def part1_move(inputs: np.array, target: int) -> np.array:
    diffs = abs(inputs - target)
    return np.array(diffs)


def compute_distance(the_data_points: np.array, compute_fn: types.FunctionType) -> int:
    distance = np.inf
    for current_target in range(the_data_points.min(), the_data_points.max()):
        fuel_cost = compute_fn(the_data_points, current_target)
        fuel_cost = np.sum(fuel_cost).squeeze()
        if distance > fuel_cost:
            distance = fuel_cost
    return distance


if __name__ == '__main__':
    #data = "16,1,2,0,4,2,7,1,2,14"
    data = get_data(day=7, year=2021)
    data_points = np.array([int(x) for x in data.split(',')])
    current_distance_part1 = compute_distance(data_points, part1_move)
    print(f'Part 1 {current_distance_part1}')
    current_distance_part2 = compute_distance(data_points, part2_move)
    print(f'Part 2 {current_distance_part2}')
    
