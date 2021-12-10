import math
from collections import deque
from dataclasses import dataclass
from aocd import get_data


@dataclass
class Chunk:
    open_tag: str
    close_tag: str
    points: int = 0,
    completion_points: int = 0


@dataclass
class InvalidSyntax:
    tag: Chunk
    invalid: str
    input_line: str


@dataclass
class SyntaxCompletion:
    input_line: str
    required_tags: list


def corrupt_lines(input_data: list, current_syntax: list) -> list:
    corrupted = []
    for navigation_line in input_data:
        parsed_items = deque([navigation_line[0]])
        for chunk_char in navigation_line[1:]:
            if chunk_char not in [syntax.close_tag for syntax in current_syntax]:
                parsed_items.append(chunk_char)
                continue
            active_chunk = list(filter(lambda syntax: syntax.close_tag == chunk_char, current_syntax)).pop()
            current_tag = parsed_items.pop()
            if active_chunk.open_tag != current_tag:
                corrupted.append(InvalidSyntax(tag=active_chunk, input_line=navigation_line, invalid=chunk_char))
    return corrupted


def to_complete_line(current_tags: deque, current_syntax: list, incomplete_line: str) -> SyntaxCompletion:
    tags_to_complete = []
    while len(current_tags) > 0:
        parsed_tag = current_tags.pop()
        match_chunk = list(filter(lambda syntax: syntax.open_tag == parsed_tag, current_syntax)).pop()
        tags_to_complete.append(match_chunk)
    return SyntaxCompletion(input_line=incomplete_line, required_tags=tags_to_complete)


def incomplete_lines(input_data: list, current_syntax: list) -> list:
    line_endings = []
    for incomplete_line in input_data:
        parsed_items = deque([incomplete_line[0]])
        for chunk_char in incomplete_line[1:]:
            if chunk_char not in [syntax.close_tag for syntax in current_syntax]:
                parsed_items.append(chunk_char)
                continue
            parsed_items.pop()
        line_endings.append(to_complete_line(parsed_items, current_syntax, incomplete_line))
    return line_endings


def score_incompletes(endings: list) -> int:
    line_scores = []
    for ending in endings:
        line_score = 0
        for index, end_tag in enumerate(ending.required_tags):
            line_score = (line_score * 5) + end_tag.completion_points
        line_scores.append(line_score)
    line_scores.sort()
    mid = math.floor(len(line_scores) / 2)
    return line_scores[mid]


if __name__ == '__main__':
    # data = [
    #     "[({(<(())[]>[[{[]{<()<>>",
    #     "[(()[<>])]({[<{<<[]>>(",
    #     "{([(<{}[<>[]}>{[]{[(<()>",
    #     "(((({<>}<{<{<>}{[]{[]{}",
    #     "[[<[([]))<([[{}[[()]]]",
    #     "[{[{({}]{}}([{[{{{}}([]",
    #     "{<[[]]>}<{[{[{[]{()[[[]",
    #     "[<(<(<(<{}))><([]([]()",
    #     "<{([([[(<>()){}]>(<<{{",
    #     "<{([{{}}[<[[[<>{}]]]>[]]"
    # ]
    data = get_data(day=10, year=2021).splitlines()
    chunk_syntax = [
        Chunk(open_tag="(", close_tag=")", points=3, completion_points=1),
        Chunk(open_tag="<", close_tag=">", points=25137, completion_points=4),
        Chunk(open_tag="[", close_tag="]", points=57, completion_points=2),
        Chunk(open_tag="{", close_tag="}", points=1197, completion_points=3)
    ]
    invalids = corrupt_lines(data, chunk_syntax)
    part1_values = sum([invalid.tag.points for invalid in invalids])
    print(f'Part 1: {part1_values}')
    incompletes = incomplete_lines(list(set(data) - set([invalid.input_line for invalid in invalids])), chunk_syntax)
    part2_value = score_incompletes(incompletes)
    print(f'Part 2: {part2_value}')
