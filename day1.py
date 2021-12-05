import itertools
from aocd import get_data

if __name__ == '__main__':
    #data = [199,200,208,210,200,207,240,269,260,263]

    data = [int(i) for i in list(get_data(day=1, year=2021).splitlines())]

    pairs = list(itertools.pairwise(data))
    diffs = [second - first for first, second in pairs]
    increments = [entry for entry in diffs if entry > 0]
    print(f'Part 1: Increments: {len(increments)}')

    triples = []
    # I don't like this, but group does uniques
    # so do it the brutey force way
    for index, first_value in enumerate(data):
        if index + 2 >= len(data):
            break
        second_value = data[index + 1]
        third_value = data[index + 2]
        triples.append((first_value, second_value,third_value))

    triple_sums = [first + second + third for first, second, third in triples]
    second_pairs = list(itertools.pairwise(triple_sums))
    diffs = [second - first for first, second in second_pairs]
    increments = [entry for entry in diffs if entry > 0]
    print(f'Part 2: Increments: {len(increments)}')

