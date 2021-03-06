from collections import deque
from dataclasses import dataclass
import numpy as np
import numpy
import pandas
from aocd import get_data

@dataclass
class Point:
    row: int = np.inf
    column: int = np.inf


@dataclass
class LowPoints(Point):
    value: int = np.inf


@dataclass
class Bounds:
    min_row: int = np.inf
    max_row: int = np.inf
    min_column: int = np.inf
    max_column: int = np.inf


def possible_neighbors(row: int, column: int) -> list:
    return [
        (column - 1, row),
        (column + 1, row),
        (column, row - 1),
        (column, row + 1)
    ]


def is_valid_cell_location(point_location: Point, grid_bounds: Bounds) -> bool:
    if point_location.column < grid_bounds.min_column or point_location.column > grid_bounds.max_column:
        return False
    if point_location.row < grid_bounds.min_row or point_location.row > grid_bounds.max_row:
        return False
    return True


def find_low_points(the_grid: pandas.DataFrame) -> (list, Bounds):
    low_points = []
    the_grid_bounds = Bounds()
    the_grid_bounds.min_column = min(the_grid.columns)
    the_grid_bounds.max_column = max(the_grid.columns)
    for col_index in range(the_grid.columns.size):
        for row_index in range(the_grid[col_index].size):
            target_cell = the_grid.iat[row_index, col_index]
            adjacency = []
            if the_grid_bounds.min_row == np.inf:
                the_grid_bounds.min_row = 0
                the_grid_bounds.max_row = the_grid[col_index].count() - 1
            for col_x, row_y in possible_neighbors(row_index, col_index):
                if is_valid_cell_location(Point(row=row_y, column=col_x), the_grid_bounds):
                    adjacency.append(the_grid.iat[row_y, col_x])
            if all(x > target_cell for x in adjacency):
                low_points.append(LowPoints(row=row_index, column=col_index, value=target_cell))
    return low_points, the_grid_bounds


def find_basins(the_low_points: list, start_grid: pandas.DataFrame, current_bounds: Bounds) -> list:
    basins = []
    for low_point in the_low_points:
        start_location = Point(low_point.row, low_point.column)
        # print(start_location)
        cells_to_check = deque([start_location])
        temp_grid = start_grid.copy(deep=True)
        while len(cells_to_check) > 0:
            target_cell = cells_to_check.popleft()
            temp_grid.iat[target_cell.row, target_cell.column] = np.inf
            for col_x, row_y in possible_neighbors(target_cell.row, target_cell.column):
                if is_valid_cell_location(Point(row=row_y, column=col_x), current_bounds) is False:
                    continue
                if temp_grid.iat[row_y, col_x] < 9:
                    cells_to_check.append(Point(row_y, col_x))
        basins.append(temp_grid.eq(np.inf).sum().sum())
        basins.sort()
    return basins


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
    low_points, bounds = find_low_points(grid)
    part1_answer = sum([low_point.value + 1 for low_point in low_points])
    print(f'Part 1 {part1_answer}')
    found_basins = find_basins(low_points, grid, bounds)
    print(f'Part 2: {numpy.prod(found_basins[-3:])}')