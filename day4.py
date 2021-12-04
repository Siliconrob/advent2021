import itertools
import pandas
import pandas as pd
from aocd import get_data
from parse import parse


def create_bingo_card(input_rows: str) -> pandas.DataFrame:
    input_matrix = []
    card_rows = [row for row in input_rows.split('\n')]
    for row_data in card_rows:
        row = [int(value) for value in parse('{} {} {} {} {}', row_data)]
        input_matrix.append(row)
    return pd.DataFrame(input_matrix)


def is_column_complete(card_to_check: pandas.DataFrame, zero_marker: float) -> pandas.DataFrame:
    for column in list(card_to_check):
        column_values = card_to_check[column].values.tolist()
        marked = sum(i < 0 for i in column_values)
        if marked == len(column_values):
            card_to_check.replace(zero_marker, 0, True)
            return card_to_check
    return None


def is_row_complete(card_to_check: pandas.DataFrame, zero_marker: float) -> pandas.DataFrame:
    for row in card_to_check.values.tolist():
        marked = sum(i < 0 for i in row)
        if marked == len(row):
            card_to_check.replace(zero_marker, 0, True)
            return card_to_check
    return None


def is_complete(card_to_check: pandas.DataFrame, zero_marker: float) -> pandas.DataFrame:
    checked_card = is_column_complete(card_to_check, zero_marker)
    if checked_card is not None:
        return checked_card
    return is_row_complete(card_to_check, zero_marker)


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

    mark_zero = -.1
    complete_card = None
    winning_number = None
    for draw_number in draw_numbers:
        replace_number = mark_zero if draw_number == 0 else draw_number * -1
        for bingo_card in bingo_cards:
            bingo_card.replace(draw_number, replace_number, True)
            complete_card = is_complete(bingo_card, mark_zero)
            if complete_card is not None:
                break
        if complete_card is not None:
            winning_number = draw_number
            break
    flattened = list(itertools.chain(*complete_card.values.tolist()))
    unmarked = list(filter(lambda x: (x > 0), flattened))
    unmarked_sum = sum([int(x) for x in unmarked])
    print(f'Part 1 {unmarked_sum * winning_number}')
