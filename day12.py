from collections import deque
from collections import Counter
from dataclasses import dataclass
from aocd import get_data
import networkx as nx

@dataclass
class LineSegment:
    start: str
    end: str

    def is_terminal_path(self) -> bool:
        return self.start == "start" or self.end == "end"

    def is_bidirectional(self) -> bool:
        return (self.end.isupper() or self.start.isupper()) and not self.is_terminal_path()


def parse_input_line(input_line: str) -> LineSegment:
    coords = input_line.split("-")
    return LineSegment(start=coords[0], end=coords[1])


def calculate_paths(path_instructions: dict, current_paths: list, path_in_progress: list, allow_duplicates: bool):
    current_node = path_in_progress[-1]
    if current_node == 'end':
        # End means the path is done add to the in progress current paths
        current_paths.append(current_node)
    else:
        # Remove the start node from each possible path of neighbors
        availables = set.difference(path_instructions[current_node], set(['start']))
        # If a lower case node is in the path already remove it from the list of available
        repeats = [node for node in availables if node.islower() and node in path_in_progress]
        if allow_duplicates and current_node.islower() and current_node in path_in_progress:
            # not working
            z = Counter(path_in_progress)[current_node]
            if z > 1:
                repeats.remove(current_node)
        repeats = set(repeats)
        availables = set.difference(availables, repeats)
        # # all available recurse for paths
        for available in availables:
            calculate_paths(path_instructions, current_paths, path_in_progress + [available], allow_duplicates)

def all_paths(path_instructions: dict, allow_duplicates: bool) -> int:
    current_paths = []
    calculate_paths(path_instructions, current_paths, ['start'], allow_duplicates)
    return len(current_paths)


if __name__ == '__main__':
    # data = [
    #     "start-A",
    #     "start-b",
    #     "A-c",
    #     "A-b",
    #     "b-d",
    #     "A-end",
    #     "b-end"
    # ]
    data = get_data(day=12, year=2021).splitlines()
    input_paths = [parse_input_line(line) for line in data]

    G = nx.Graph()
    for input_path in input_paths:
        print(f'{input_path.start}-{input_path.end} <-> {input_path.is_bidirectional()}')
        if input_path.start not in G:
            G.add_node(input_path.start)
        if input_path.end not in G:
            G.add_node(input_path.end)
        G.add_edge(input_path.start, input_path.end)

    path_sets = {}
    for node in G.nodes:
        path_sets[node] = set(G.neighbors(node))

    part1_solution = all_paths(path_sets, False)
    print(f'Part 1: {part1_solution}')

    part2_solution = all_paths(path_sets, True)
    print(f'Part 2: {part2_solution}') # not working
