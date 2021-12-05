import itertools
from dataclasses import dataclass
import pandas
import pandas as pd
from aocd import get_data


@dataclass
class Point:
    x: int = 0
    y: int = 0


@dataclass
class GridDimensions:
    min_x: int = 0
    max_x: int = 0
    min_y: int = 0
    max_y: int = 0


@dataclass
class Line:
    start: Point = Point()
    end: Point = Point()

    def part1_valid(self) -> bool:
        if self.start.x == self.end.x or self.start.y == self.end.y:
            return True
        return False


def parse_coordinate(input_coord: str) -> Point:
    coordinate = input_coord.split(',')
    new_coordinate = Point()
    new_coordinate.x = int(coordinate[0])
    new_coordinate.y = int(coordinate[1])
    return new_coordinate


def parse_line(line_endpoints: str) -> Line:
    coords = line_endpoints.split('->')
    new_line = Line()
    new_line.start = parse_coordinate(str.strip(coords[0]))
    new_line.end = parse_coordinate(str.strip(coords[1]))
    return new_line


def new_grid(input_coords: list) -> pandas.DataFrame:
    x_range = [0]
    y_range = [0]
    for input_coord in input_coords:
        x_range = list(itertools.chain(x_range, [input_coord.start.x, input_coord.end.x]))
        y_range = list(itertools.chain(x_range, [input_coord.start.y, input_coord.end.y]))
    dimensions = GridDimensions()
    dimensions.max_x = max(x_range)
    dimensions.max_y = max(y_range)
    empty_frame = pd.DataFrame(index=range(max(y_range) + 1), columns=range(max(x_range) + 1))
    empty_frame.fillna(0, inplace=True)
    return empty_frame


def plot_part1(current_grid: pandas.DataFrame, part1_lines: list) -> pandas.DataFrame:
    the_grid = current_grid.copy(deep=True)
    for part1_line in part1_lines:
        if part1_line.start.x == part1_line.end.x:
            min_max = [part1_line.start.y, part1_line.end.y]
            for y in range(min(min_max), max(min_max) + 1, 1):
                the_grid.iat[y, part1_line.start.x] += 1
        elif part1_line.start.y == part1_line.end.y:
            min_max = [part1_line.start.x, part1_line.end.x]
            for x in range(min(min_max), max(min_max) + 1, 1):
                the_grid.iat[part1_line.start.y, x] += 1
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
    data = get_data(day=5)
    lines = [parse_line(line_input) for line_input in data.splitlines()]
    plot_grid = new_grid(lines)
    part1_grid = plot_part1(plot_grid, list(filter(lambda line: line.part1_valid(), lines)))
    print(f'Part 1 {sum(part1_grid.ge(2).sum())}')

