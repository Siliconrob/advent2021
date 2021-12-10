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
    corrupt_lines = []
    endings = [syntax.close_tag for syntax in chunk_syntax]
    for navigation_line in data:
        parsed_items = deque([navigation_line[0]])
        for chunk_char in navigation_line[1:]:
            if chunk_char not in endings:
                parsed_items.append(chunk_char)
                continue
            active_chunk = list(filter(lambda syntax: syntax.close_tag == chunk_char, chunk_syntax)).pop()
            current_tag = parsed_items.pop()
            if active_chunk.open_tag != current_tag:
                corrupt_lines.append(InvalidSyntax(tag=active_chunk, input_line=navigation_line, invalid=chunk_char))
    part1_values = sum([corrupt_line.tag.points for corrupt_line in corrupt_lines])
    print(f'Part 1: {part1_values}')

    incomplete_lines = list(set(data) - set([corrupt_line.input_line for corrupt_line in corrupt_lines]))
    line_endings = []
    for incomplete_line in incomplete_lines:
        parsed_items = deque([incomplete_line[0]])
        for chunk_char in incomplete_line[1:]:
            if chunk_char not in endings:
                parsed_items.append(chunk_char)
                continue
            active_chunk = list(filter(lambda syntax: syntax.close_tag == chunk_char, chunk_syntax)).pop()
            current_tag = parsed_items.pop()
        tags_to_complete = []
        while len(parsed_items) > 0:
            parsed_tag = parsed_items.pop()
            match_chunk = list(filter(lambda syntax: syntax.open_tag == parsed_tag, chunk_syntax)).pop()
            tags_to_complete.append(match_chunk)
        line_endings.append(SyntaxCompletion(input_line=incomplete_line, required_tags=tags_to_complete))

    line_scores = []
    for ending in line_endings:
        line_score = 0
        for index, end_tag in enumerate(ending.required_tags):
            line_score = (line_score * 5) + end_tag.completion_points
        line_scores.append(line_score)
    line_scores.sort()
    mid = math.floor(len(line_scores) / 2)
    middle_score = line_scores[mid]
    print(f'Part 2: {middle_score}')

