from collections import Counter
from aocd import get_data
import itertools


if __name__ == '__main__':
    # data = [
    #     "NNCB",
    #     "",
    #     "CH -> B",
    #     "HH -> N",
    #     "CB -> H",
    #     "NH -> C",
    #     "HB -> C",
    #     "HC -> B",
    #     "HN -> C",
    #     "NN -> C",
    #     "BH -> H",
    #     "NC -> B",
    #     "NB -> B",
    #     "BN -> B",
    #     "BB -> N",
    #     "BC -> B",
    #     "CC -> N",
    #     "CN -> C"
    # ]
    data = get_data(day=14, year=2021).splitlines()
    spacer = data.index('')
    splits = [data[:spacer], data[spacer + 1:]]

    templates = splits.pop()
    current_input = splits.pop()[0]
    template_rules = {}
    for rule in templates:
        rule_parts = rule.split('->')
        (first_letter, second_letter) = str.strip(rule_parts[0])
        template_rules[(first_letter, second_letter)] = str.strip(rule_parts[1])
    for index in range(10):
        current_chars = [current_char for current_char in current_input]
        pairs = list(itertools.pairwise(current_chars))
        revised_input = []
        for pair_index, (letter_1, letter_2) in enumerate(pairs):
            if (letter_1, letter_2) in template_rules:
                revised_input = revised_input[:-1]
                revised_input += f'{letter_1}{template_rules[(letter_1, letter_2)]}{letter_2}'
            else:
                revised_input += f'{letter_1}{letter_2}'
        current_input = revised_input
        print(f'Step {index}: {"".join(current_input)}')

    counts = Counter(current_input).most_common()
    (most_chemical, most_common) = counts[0]
    (least_chemical, least_common) = counts[-1]
    part1_solution = most_common - least_common
    print(f'Part 1 solution: {(most_chemical, most_common)} - {(least_chemical, least_common)} = {part1_solution}')
