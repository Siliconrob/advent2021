from collections import Counter
from dataclasses import dataclass
from aocd import get_data


@dataclass
class InputLine:
    line: str

    def signals(self) -> list:
        return str.strip(self.line.split('|').pop(0)).split(' ')

    def output(self) -> list:
        return str.strip(self.line.split('|').pop()).split(' ')

@dataclass
class DigitDisplay:
    Zero:str = "abcefg"
    One: str = "cf"
    Two: str = "acdeg"
    Three: str = "acdfg"
    Four: str = "bcdf"
    Five: str = "abdfg"
    Six: str = "abdefg"
    Seven: str = "acf"
    Eight: str = "abcdefg"
    Nine: str = "abcdfg"


def part1_count(output_values: list, search_digit_patterns: list) -> int:
    total_uniques = 0
    digit_lengths = [len(digit_pattern) for digit_pattern in search_digit_patterns]
    for output_value in output_values:
        output_digits = [len(output_digit) for output_digit in output_value]
        total_uniques += sum([v if k in digit_lengths else 0 for k, v in Counter(output_digits).items()])
    return total_uniques


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
    data_lines = [InputLine(line) for line in data]
    part1_result = part1_count([data_line.output() for data_line in data_lines], [digits.One, digits.Four, digits.Seven, digits.Eight])
    print(f'Part 1: {part1_result}')
