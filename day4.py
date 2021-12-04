import itertools
import numpy as np
import pandas
import pandas as pd
from aocd import get_data
from parse import parse


def create_bingo_card(input_rows: str) -> pandas.DataFrame:
    input_matrix = []
    card_rows = [row for row in input_rows.split('\n')]
    for row_data in card_rows:
        row = [str.strip(value) for value in parse('{} {} {} {} {}', row_data)]
        input_matrix.append(row)
    return pd.DataFrame(input_matrix)


def is_column_complete(card_to_check: pandas.DataFrame) -> pandas.DataFrame:
    test_card = card_to_check.fillna('-0')
    for column in list(test_card):
        column_values = test_card[column].values.tolist()
        if sum(1 if i.startswith('-') else 0 for i in column_values) == len(column_values):
            return test_card
    return None


def is_row_complete(card_to_check: pandas.DataFrame) -> pandas.DataFrame:
    test_card = card_to_check.fillna('-0')
    for row_values in test_card.values.tolist():
        if sum(1 if i.startswith('-') else 0 for i in row_values) == len(row_values):
            return test_card
    return None


def is_complete(card_to_check: pandas.DataFrame) -> pandas.DataFrame:
    checked_card = is_column_complete(card_to_check)
    if checked_card is not None:
        return checked_card
    return is_row_complete(card_to_check)


def is_empty(current_cards: list) -> bool:
    nones = 0
    for current_card in current_cards:
        if current_card is None:
            nones += 1
    return nones == len(current_cards)


if __name__ == '__main__':
#     data = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1
#
# 22 13 17 11  0
#  8  2 23  4 24
# 21  9 14 16  7
#  6 10  3 18  5
#  1 12 20 15 19
#
#  3 15  0  2 22
#  9 18 13 17  5
# 19  8  7 25 23
# 20 11 10 24  4
# 14 21 16 12  6
#
# 14 21 17 24  4
# 10 16 15  9 19
# 18  8 23 26 20
# 22 11 13  6  5
#  2  0 12  3  7"""
    data = get_data(day=4)
    split_data = data.split("\n\n")
    draw_numbers = [int(x) for x in split_data[:1][0].split(',')]
    bingo_cards = []
    for card_input in split_data[1:]:
        new_playable_card = create_bingo_card(card_input)
        bingo_cards.append(new_playable_card)

    mark_zero = np.NAN
    complete_cards = []
    winning_numbers = []
    for draw_number in draw_numbers:
        if is_empty(bingo_cards):
            break
        replace_number = mark_zero if draw_number == 0 else str(draw_number * -1)
        index = 0
        for bingo_card in bingo_cards:
            if bingo_card is None:
                index += 1
                continue
            bingo_card.replace(str(draw_number), replace_number, True)
            complete_card = is_complete(bingo_card)
            if complete_card is not None:
                complete_cards.append(complete_card.copy(deep=True))
                winning_numbers.append(draw_number)
                bingo_cards[index] = None
            index += 1

    first_winner = list(itertools.chain(*complete_cards[:1][0].values.tolist()))
    unmarked = list(filter(lambda x: (int(x) > 0), first_winner))
    unmarked_sum = sum([int(x) for x in unmarked])
    part1 = unmarked_sum * winning_numbers[:1][0]
    print(f'Part 1 {part1}')

    last_winner = list(itertools.chain(*complete_cards[-1].values.tolist()))
    unmarked = list(filter(lambda x: (int(x) > 0), last_winner))
    unmarked_sum = sum([int(x) for x in unmarked])
    part2 = unmarked_sum * winning_numbers[-1]
    print(f'Part 2 {part2}')
