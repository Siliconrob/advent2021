from collections import Counter
from dataclasses import dataclass
from aocd import get_data


@dataclass
class InputLine:
    line: str = ""

    def signals(self) -> list:
        return ["".join(sorted(result)) for result in str.strip(self.line.split('|').pop(0)).split(' ')]

    def output(self) -> list:
        return ["".join(sorted(result)) for result in str.strip(self.line.split('|').pop()).split(' ')]

@dataclass
class InputSignal:
    A: str = ''
    B: str = ''
    C: str = ''
    D: str = ''
    E: str = ''
    F: str = ''
    G: str = ''

@dataclass
class DigitDisplay:
    Zero: str = "abcefg"
    One: str = "cf"
    Two: str = "acdeg"
    Three: str = "acdfg"
    Four: str = "bcdf"
    Five: str = "abdfg"
    Six: str = "abdefg"
    Seven: str = "acf"
    Eight: str = "abcdefg"
    Nine: str = "abcdfg"

    def match(self, output_value: str) -> int:
        options = [self.Zero, self.One, self.Two, self.Three, self.Four, self.Five, self.Six, self.Seven, self.Eight, self.Nine]
        return options.index(output_value)


def part1_count(output_values: list, search_digit_patterns: list) -> int:
    total_uniques = 0
    digit_lengths = [len(digit_pattern) for digit_pattern in search_digit_patterns]
    for output_value in output_values:
        output_digits = [len(output_digit) for output_digit in output_value]
        total_uniques += sum([v if k in digit_lengths else 0 for k, v in Counter(output_digits).items()])
    return total_uniques


def create_signal_input(signal_line: list) -> InputSignal:
    # Known pattern signals
    signal_cf = set(list(filter(lambda x: (len(x) == 2), signal_line)).pop())  # 1
    signal_bcdf = set(list(filter(lambda x: (len(x) == 4), signal_line)).pop())  # 4
    signal_acf = set(list(filter(lambda x: (len(x) == 3), signal_line)).pop())  # 7
    signal_abcdefg = set(list(filter(lambda x: (len(x) == 7), signal_line)).pop())  # 8

    # multiple options
    three_five_two_options = five_segment_options = list(filter(lambda x: (len(x) == 5), signal_line))
    zero_six_nine_options = list(filter(lambda x: (len(x) == 6), signal_line))

    # five signal pattern common elements
    signal_adg = set.intersection(*map(set, three_five_two_options))
    # six signal pattern common elements
    signal_bdefg = set.intersection(*map(set, zero_six_nine_options))

    # make a lookup table
    signal_table = InputSignal()
    signal_table.A = set.difference(signal_acf, signal_cf)
    signal_table.B = set.difference(set.difference(signal_bcdf, signal_cf), signal_adg)
    signal_table.C = set.difference(signal_cf, signal_bdefg)
    signal_table.D = set.intersection(signal_bcdf, signal_adg)
    signal_table.E = set.difference(set.difference(signal_abcdefg, signal_adg), signal_bcdf)
    signal_table.F = set.intersection(signal_bdefg, signal_cf)
    signal_table.G = set.difference(set.intersection(signal_bdefg, signal_adg), signal_bcdf)
    return signal_table


def new_display_lines(signal_table: InputSignal) -> DigitDisplay:
    # reassign the input signal characters according to set intersection, union, difference of common signals
    current_display = DigitDisplay()
    current_display.Zero = "".join(sorted(
        set.union(signal_table.A, signal_table.B, signal_table.C, signal_table.E, signal_table.F, signal_table.G)))
    current_display.One = "".join(sorted(set.union(signal_table.C, signal_table.F)))
    current_display.Two = "".join(
        sorted(set.union(signal_table.A, signal_table.C, signal_table.D, signal_table.E, signal_table.G)))
    current_display.Three = "".join(
        sorted(set.union(signal_table.A, signal_table.C, signal_table.D, signal_table.F, signal_table.G)))
    current_display.Four = "".join(sorted(set.union(signal_table.B, signal_table.C, signal_table.D, signal_table.F)))
    current_display.Five = "".join(
        sorted(set.union(signal_table.A, signal_table.B, signal_table.D, signal_table.F, signal_table.G)))
    current_display.Six = "".join(sorted(
        set.union(signal_table.A, signal_table.B, signal_table.D, signal_table.E, signal_table.F, signal_table.G)))
    current_display.Seven = "".join(sorted(set.union(signal_table.A, signal_table.C, signal_table.F)))
    current_display.Eight = "".join(sorted(
        set.union(signal_table.A, signal_table.B, signal_table.C, signal_table.D, signal_table.E, signal_table.F,
                  signal_table.G)))
    current_display.Nine = "".join(sorted(
        set.union(signal_table.A, signal_table.B, signal_table.C, signal_table.D, signal_table.F, signal_table.G)))
    return current_display


if __name__ == '__main__':
    # data = [
    # "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",
    # "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",
    # "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg",
    # "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb",
    # "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea",
    # "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb",
    # "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe",
    # "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef",
    # "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb",
    # "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"
    # ]
    data = get_data(day=8, year=2021).splitlines()

    digits = DigitDisplay()
    inputs = [InputLine(line) for line in data]
    outputs = [input.output() for input in inputs]
    part1_result = part1_count(outputs, [digits.One, digits.Four, digits.Seven, digits.Eight])
    print(f'Part 1: {part1_result}')

    part2_result = 0
    for input in inputs:
        outputs = input.output()
        # lookup the values for this iteration display
        current_display = new_display_lines(create_signal_input(input.signals()))
        line_entry_value = int("".join([str(current_display.match(output_value)) for output_value in outputs]))
        print(line_entry_value)
        part2_result += line_entry_value
    print(f'Part 2: {part2_result}')
