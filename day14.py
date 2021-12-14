from collections import Counter, defaultdict
from aocd import get_data
import itertools


def part2_rule_keyset(original_data: list) -> dict:
    rules = {}
    spacer = data.index('')
    for rule_letters in [original_data[:spacer], original_data[spacer + 1:]].pop():
        rule_parts = rule_letters.split('->')
        rules["".join(str.strip(rule_parts[0]))] = str.strip(rule_parts[1])
    return rules


def build_pair_counts(start_line: str) -> dict:
    current_input = start_line
    current_chars = [current_char for current_char in current_input]
    pair_keys = []
    for pair_index, pair_key in enumerate(list(itertools.pairwise(current_chars))):
        pair_keys.append("".join(pair_key))
    return dict(Counter(pair_keys))

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
    initial_input = splits.pop()[0]
    template_rules = {}
    for rule in templates:
        rule_parts = rule.split('->')
        (first_letter, second_letter) = str.strip(rule_parts[0])
        template_rules[(first_letter, second_letter)] = str.strip(rule_parts[1])

    current_input = initial_input
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
        print(f'Step {index}')

    counts = Counter(current_input).most_common()
    (most_chemical, most_common) = counts[0]
    (least_chemical, least_common) = counts[-1]
    part1_solution = most_common - least_common
    print(f'Part 1 solution: {(most_chemical, most_common)} - {(least_chemical, least_common)} = {part1_solution}')

    pair_counts_dict = build_pair_counts(initial_input)
    part2_rules = part2_rule_keyset(data)

    # Use bucketing because can't do this iteratively
    for index in range(40):
        current_pair_counts = defaultdict(int)
        for pair_count in pair_counts_dict:
            new_polymer = part2_rules[pair_count]
            # buckets count letters produced and match on start and endings
            first_letter, second_letter = pair_count[0], pair_count[1]
            first_pair = first_letter + new_polymer
            second_pair = new_polymer + second_letter
            # Match as end polymer
            current_pair_counts[first_pair] += pair_counts_dict[pair_count]
            # Match as polymer start
            current_pair_counts[second_pair] += pair_counts_dict[pair_count]
        # Reset the dictionary with latest
        pair_counts_dict = current_pair_counts

    letter_count = defaultdict(int)
    # Add the last character from initial input as it has no accompanying pair for the counting buckets of
    # the dictionary
    letter_count[initial_input[-1]] += 1
    for k, v in pair_counts_dict.items():
        letter = k[0]
        if letter in letter_count:
            letter_count[letter] += v
        else:
            letter_count[letter] = v

    part2_counts = Counter(letter_count).most_common()
    (most_chemical, most_common) = part2_counts[0]
    (least_chemical, least_common) = part2_counts[-1]
    part2_solution = most_common - least_common
    print(f'Part 2 solution: {(most_chemical, most_common)} - {(least_chemical, least_common)} = {part2_solution}')

