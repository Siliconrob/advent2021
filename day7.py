import numpy as np
from aocd import get_data

if __name__ == '__main__':
    #data = "16,1,2,0,4,2,7,1,2,14"
    data = get_data(day=7, year=2021)

    data_points = np.array([int(x) for x in data.split(',')])
    data_points.sort()
    current_distance = np.inf

    for current_target in range(data_points.min(), data_points.max()):
        move_fn = lambda z: abs(z - current_target)
        fuel_costs = move_fn(data_points)
        fuel_cost = np.sum(fuel_costs).squeeze()
        if current_distance > fuel_cost:
            current_distance = fuel_cost
    print(current_distance)
