import pandas
from aocd import get_data
import networkx as nx

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
    grid = pandas.DataFrame([[int(point) for point in line] for line in data])
    max_coord = len(grid.columns) - 1
    G = nx.Graph()
    for col_index, column in enumerate(grid.columns):
        for row_index, row in enumerate(grid[col_index]):
            node_weight = grid.iat[row_index, col_index]
            if (row_index, col_index) not in G:
                G.add_node((row_index, col_index))
            for neighbor in coord_neighbors(row_index, col_index, 0, max_coord):
                neighbor_column, neighbor_row = neighbor
                if (neighbor_row, neighbor_column) not in G:
                    G.add_node((neighbor_row, neighbor_column))
                G.add_edge((row_index, col_index), (neighbor_row, neighbor_column), weight=node_weight)

    path = nx.dijkstra_path(G, (0, 0), (max_coord, max_coord))
    path_weights = []
    for path_index, coord in enumerate(path):
        row, col = coord
        node_weight = grid.iat[row, col]
        if path_index > 0:
            path_weights.append(node_weight)
    part1_solution = (sum(path_weights))
    print(f'Part 1 {part1_solution}')




