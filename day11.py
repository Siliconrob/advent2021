from collections import deque
from dataclasses import dataclass
import numpy as np
import pandas
from aocd import get_data
from tabulate import tabulate


@dataclass
class Bounds:
    min_row: int = np.inf
    max_row: int = np.inf
    min_column: int = np.inf
    max_column: int = np.inf

    def cell_count(self):
        return (self.max_row + 1) * (self.max_column + 1)


@dataclass
class Point:
    row: int = np.inf
    column: int = np.inf


def is_valid_cell_location(point_location: Point, grid_bounds: Bounds) -> bool:
    if point_location.column < grid_bounds.min_column or point_location.column > grid_bounds.max_column:
        return False
    if point_location.row < grid_bounds.min_row or point_location.row > grid_bounds.max_row:
        return False
    return True


def possible_neighbors(start_row: int, start_column: int) -> list:
    return [
        Point(column=start_column - 1, row=start_row - 1),
        Point(column=start_column - 1, row=start_row),
        Point(column=start_column - 1, row=start_row + 1),
        Point(column=start_column, row=start_row - 1),
        Point(column=start_column + 1, row=start_row),
        Point(column=start_column + 1, row=start_row - 1),
        Point(column=start_column, row=start_row + 1),
        Point(column=start_column + 1, row=start_row + 1)
    ]


def current_bounds(grid_to_search: pandas.DataFrame) -> Bounds:
    grid_bounds = Bounds()
    grid_bounds.min_column = min(grid_to_search.columns)
    grid_bounds.max_column = max(grid_to_search.columns)
    grid_bounds.min_row = 0
    grid_bounds.max_row = grid_to_search[0].count() - 1
    return grid_bounds


def available_neighbors(current_grid: pandas.DataFrame, possibilities: list) -> list:
    bounds = current_bounds(current_grid)
    available = []
    for possibility in possibilities:
        if is_valid_cell_location(possibility, bounds):
            available.append(possibility)
    return available


def match_positions(grid_to_search: pandas.DataFrame, search_value: int) -> list:
    match_locations = []
    for current_column in grid_to_search.columns:
        row_match = grid_to_search[grid_to_search[current_column] == search_value].index.tolist()
        match_locations.extend([Point(column=current_column, row=current_row) for current_row in row_match])
    return match_locations


if __name__ == '__main__':
    # data = [
    #     "5483143223",
    #     "2745854711",
    #     "5264556173",
    #     "6141336146",
    #     "6357385478",
    #     "4167524645",
    #     "2176841721",
    #     "6882881134",
    #     "4846848554",
    #     "5283751526"
    # ]
    data = get_data(day=11, year=2021).splitlines()
    data_points = [[int(point) for point in line] for line in data]
    grid = pandas.DataFrame(data_points)
    grid_bounds = current_bounds(grid)

    part1_flashes = 0
    round_index = 0
    part2_solution = 0
    part1_solution = 0
    while round_index < 100 or part2_solution == 0:
        grid = grid.apply(lambda x: x + 1)
        tens = grid.ge(10).sum().sum()
        while tens > 0:
            grid.replace(10, 0, inplace=True)
            current_round_flashes = deque(match_positions(grid, 0))
            while current_round_flashes:
                todo = len(current_round_flashes)
                flash_position = current_round_flashes.popleft()
                for neighbor in available_neighbors(grid, possible_neighbors(flash_position.row, flash_position.column)):
                    current_value = grid.iat[neighbor.row, neighbor.column]
                    if current_value == 0:
                        continue
                    current_value += 1
                    if current_value == 10:
                        current_value = 0
                        current_round_flashes.append(neighbor)
                    grid.iat[neighbor.row, neighbor.column] = current_value
            tens = grid.ge(10).sum().sum()
        round_index += 1
        round_flash = grid.eq(0).sum().sum()
        part1_flashes += round_flash
        if round_index == 100:
            part1_solution = part1_flashes
        if round_flash == grid_bounds.cell_count():
            print(tabulate(grid, headers='keys', tablefmt='psql'))
            part2_solution = round_index
    print(f'Part 1: {part1_solution}')
    print(f'Part 2: {part2_solution}')
