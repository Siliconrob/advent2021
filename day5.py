import itertools
import types
from dataclasses import dataclass
import pandas
import pandas as pd
from aocd import get_data


@dataclass
class Point:
    x: int = 0
    y: int = 0


@dataclass
class Line:
    start: Point = Point()
    end: Point = Point()


def compute_part2(line_def: Line) -> list:
    line_coords = compute_part1(line_def)
    if len(line_coords) > 0:
        return line_coords
    min_max_x = [line_def.start.x, line_def.end.x]
    x_increments = max(min_max_x) - min(min_max_x)
    min_max_y = [line_def.start.y, line_def.end.y]
    y_increments = max(min_max_y) - min(min_max_y)
    if x_increments != y_increments:
        return line_coords
    for inc in range(x_increments + 1):
        x_change = (1 if line_def.start.x < line_def.end.x else -1) * inc
        y_change = (1 if line_def.start.y < line_def.end.y else -1) * inc
        line_coords.append((line_def.start.y + y_change, line_def.start.x + x_change))
    return line_coords


def compute_part1(line_def: Line) -> list:
    line_coords = []
    if line_def.start.x == line_def.end.x:
        min_max_y = [line_def.start.y, line_def.end.y]
        return [(y, line_def.start.x) for y in range(min(min_max_y), max(min_max_y) + 1, 1)]
    if line_def.start.y == line_def.end.y:
        min_max_x = [line_def.start.x, line_def.end.x]
        return [(line_def.start.y, x) for x in range(min(min_max_x), max(min_max_x) + 1, 1)]
    return line_coords


def parse_coordinate(input_coord: str) -> Point:
    coordinate = input_coord.split(',')
    return Point(x=int(coordinate[0]), y=int(coordinate[1]))


def parse_line(line_endpoints: str) -> Line:
    coords = line_endpoints.split('->')
    return Line(start=parse_coordinate(str.strip(coords[0])), end=parse_coordinate(str.strip(coords[1])))


def new_grid(input_coords: list) -> pandas.DataFrame:
    x_range, y_range = [0], [0]
    for input_coord in input_coords:
        x_range = list(itertools.chain(x_range, [input_coord.start.x, input_coord.end.x]))
        y_range = list(itertools.chain(x_range, [input_coord.start.y, input_coord.end.y]))
    empty_frame = pd.DataFrame(index=range(max(y_range) + 1), columns=range(max(x_range) + 1))
    empty_frame.fillna(0, inplace=True)
    return empty_frame


def plot_lines(current_grid: pandas.DataFrame, input_lines: list, line_fn: types.FunctionType) -> pandas.DataFrame:
    the_grid = current_grid.copy(deep=True)
    for input_line in input_lines:
        line_coords = line_fn(input_line)
        if len(line_coords) == 0:
            continue
        for line_coord in line_coords:
            the_grid.iat[line_coord[0], line_coord[1]] += 1
    return the_grid


if __name__ == '__main__':
#     data = """0,9 -> 5,9
# 8,0 -> 0,8
# 9,4 -> 3,4
# 2,2 -> 2,1
# 7,0 -> 7,4
# 6,4 -> 2,0
# 0,9 -> 2,9
# 3,4 -> 1,4
# 0,0 -> 8,8
# 5,5 -> 8,2"""
    data = get_data(day=5, year=2021)
    lines = [parse_line(line_input) for line_input in data.splitlines()]
    plot_grid = new_grid(lines)
    part1_grid = plot_lines(plot_grid, lines, compute_part1)
    print(f'Part 1 {sum(part1_grid.ge(2).sum())}')
    part2_grid = plot_lines(plot_grid, lines, compute_part2)
    print(f'Part 2 {sum(part2_grid.ge(2).sum())}')