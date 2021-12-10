from collections import deque
from dataclasses import dataclass
from aocd import get_data

@dataclass
class Chunk:
    open_tag: str
    close_tag: str
    points: int = 0


@dataclass
class InvalidSyntax:
    tag: Chunk
    invalid: str
    input_line: str


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
        Chunk(open_tag="(", close_tag=")", points=3),
        Chunk(open_tag="<", close_tag=">", points=25137),
        Chunk(open_tag="[", close_tag="]", points=57),
        Chunk(open_tag="{", close_tag="}", points=1197)
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
