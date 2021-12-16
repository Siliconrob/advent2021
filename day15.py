import pandas
from aocd import get_data
import networkx as nx
import itertools


def is_valid_coord(row: int, column: int, min: int, max: int) -> bool:
    return min <= column <= max and min <= row <= max


def coord_neighbors(row: int, column: int, min: int, max: int) -> list:
    start_possible = [
        (column - 1, row),
        (column + 1, row),
        (column, row - 1),
        (column, row + 1)
    ]
    valid = []
    for (new_column, new_row) in start_possible:
        if new_row < min:
            continue
        if new_row > max:
            continue
        if new_column < min:
            continue
        if new_column > max:
            continue
        valid.append((new_column, new_row))
    return valid


def get_path_risk(current_graph: nx.Graph, reference_grid: pandas.DataFrame, start: tuple, end: tuple) -> int:
    path = nx.dijkstra_path(current_graph, start, end)
    path_weights = []
    for path_index, coord in enumerate(path):
        current_row, current_column = coord
        grid_value = reference_grid.iat[current_row, current_column]
        if path_index > 0:
            path_weights.append(grid_value)
    return sum(path_weights)


def build_graph(the_grid: pandas.DataFrame) -> nx.Graph:
    G = nx.Graph()
    for col_index, column in enumerate(the_grid.columns):
        for row_index, row in enumerate(the_grid[col_index]):
            node_weight = the_grid.iat[row_index, col_index]
            if (row_index, col_index) not in G:
                G.add_node((row_index, col_index))
            for neighbor in coord_neighbors(row_index, col_index, 0, max_coord):
                neighbor_column, neighbor_row = neighbor
                if (neighbor_row, neighbor_column) not in G:
                    G.add_node((neighbor_row, neighbor_column))
                G.add_edge((row_index, col_index), (neighbor_row, neighbor_column), weight=node_weight)
    return G


def expand_data(input_data: list, expand_x_by: int, expand_y_by: int) -> list:
    expand_grid_columns = []
    for line_index, line in enumerate(input_data):
        current_line = []
        for y in range(expand_y_by):
            line_points = []
            for point in line:
                mod, rem = divmod(int(point) + (y if y > 0 else 0), 10)
                line_points.append(mod + rem)
            current_line.append(line_points)
        flat_list = list(itertools.chain(*current_line))
        expand_grid_columns.append("".join([str(val) for val in flat_list]))
    expand_grid = []
    for x in range(expand_x_by):
        for line in expand_grid_columns:
            if x == 0:
                expand_grid.append(line)
                continue
            new_line = []
            for current_point in [int(point) for point in line]:
                mod, rem = divmod(current_point + x, 10)
                new_line.append(mod + rem)
            expand_grid.append("".join([str(val) for val in new_line]))
    return expand_grid


if __name__ == '__main__':
    # data = [
    #         "1163751742",
    #         "1381373672",
    #         "2136511328",
    #         "3694931569",
    #         "7463417111",
    #         "1319128137",
    #         "1359912421",
    #         "3125421639",
    #         "1293138521",
    #         "2311944581"
    # ]
    data = get_data(day=15, year=2021).splitlines()
    part1_grid = pandas.DataFrame([[int(point) for point in line] for line in data])
    max_coord = len(part1_grid.columns) - 1
    part1_graph = build_graph(part1_grid)
    part1_solution = get_path_risk(part1_graph, part1_grid, (0, 0), (max_coord, max_coord))
    print(f'Part 1 {part1_solution}')

    part2_input = expand_data(data, 5, 5)
    part2_grid = pandas.DataFrame([[int(point) for point in line] for line in part2_input])
    max_coord = len(part2_grid.columns) - 1
    part2_graph = build_graph(part2_grid)
    part2_solution = get_path_risk(part2_graph, part2_grid, (0, 0), (max_coord, max_coord))
    print(f'Part 2 {part2_solution}')
