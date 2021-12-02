import itertools
from aocd import get_data
from dataclasses import dataclass
from parse import parse

@dataclass
class Position:
    horizontal: int = 0
    vertical: int = 0

    def distance(self) -> int:
        return self.horizontal * self.vertical

@dataclass
class Movement:
    type: str
    unit: int = 0

if __name__ == '__main__':
    data = [
        "forward 5",
        "down 5",
        "forward 8",
        "up 3",
        "down 8",
        "forward 2"
    ]

    tracker = Position()
    movements = []
    for line in data:
        direction, value = parse("{} {}", line)
        movements.append(Movement(direction, int(value)))
    print(movements)


    directions = {
        "vertical": ["up", "down"],
        "horizontal": ["forward"]
    }




    # data = [int(i) for i in list(get_data(day=1).splitlines())]
    #
    # pairs = list(itertools.pairwise(data))
    # diffs = [second - first for first, second in pairs]
    # increments = [entry for entry in diffs if entry > 0]
    # print(f'Part 1: Increments: {len(increments)}')
    #
    # triples = []
    # # I don't like this, but group does uniques
    # # so do it the brutey force way
    # for index, first_value in enumerate(data):
    #     if index + 2 >= len(data):
    #         break
    #     second_value = data[index + 1]
    #     third_value = data[index + 2]
    #     triples.append((first_value, second_value,third_value))
    #
    # triple_sums = [first + second + third for first, second, third in triples]
    # second_pairs = list(itertools.pairwise(triple_sums))
    # diffs = [second - first for first, second in second_pairs]
    # increments = [entry for entry in diffs if entry > 0]
    # print(f'Part 2: Increments: {len(increments)}')

