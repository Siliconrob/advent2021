from collections import Counter
from dataclasses import dataclass
import pandas
from aocd import get_data


if __name__ == '__main__':
    # data = [
    # "2199943210",
    # "3987894921",
    # "9856789892",
    # "8767896789",
    # "9899965678"
    # ]
    data = get_data(day=9, year=2021).splitlines()

    data_points = [[int(point) for point in line] for line in data]
    grid = pandas.DataFrame(data_points)
    low_points = []
    min_col_x = min(grid.columns)
    max_col_x = max(grid.columns)
    for col_index in range(grid.columns.size):
        for row_index in range(grid[col_index].size):
            target_cell = grid.iat[row_index, col_index]
            adjacency = []
            min_row_y = 0
            max_row_y = grid[col_index].count() - 1

            possibilities = [
                (col_index - 1, row_index),
                 (col_index + 1, row_index),
                 (col_index, row_index - 1),
                 (col_index, row_index + 1)
            ]
            for col_x, row_y in possibilities:
                if col_x < min_col_x or col_x > max_col_x:
                    continue
                if row_y < min_row_y or row_y > max_row_y:
                    continue
                try:
                    adjacency.append(grid.iat[row_y, col_x])
                except:
                    print(col_x)
                    print(row_y)
                    print(target_cell)
            if all(x > target_cell for x in adjacency):
                low_points.append(target_cell)
    risk = sum([low_point + 1 for low_point in low_points])
    print(f'Part 1 {risk}')
