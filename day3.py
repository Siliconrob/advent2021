import types
import pandas
from aocd import get_data
from dataclasses import dataclass
import pandas as pd


@dataclass
class BitTranslator:
    values: []

    def as_string(self) -> str:
        return "".join(self.values)

    def inverted(self) -> int:
        return int(self.as_string().translate(str.maketrans("10", "01")), 2)

    def current(self) -> int:
        return int(self.as_string(), 2)


def get_power(current_columns: list) -> BitTranslator:
    bit_values = []
    for column in current_columns:
        bit_values.append(max(set(column), key=column.count))
    return BitTranslator(bit_values)


def lines_as_matrix(input_data: list) -> list:
    output_matrix = []
    for current_line in input_data:
        row = []
        for char in current_line:
            row.append(char)
        output_matrix.append(row)
    return output_matrix


def oxygen_filter(ones_count: int, zeros_count: int, column_name: int, filter_frame: pandas.DataFrame) -> pandas.DataFrame:
    if zeros_count > ones_count:
        return filter_frame.loc[filter_frame[column_name] == '0']
    return filter_frame.loc[filter_frame[column_name] == '1']


def co2_filter(ones_count: int, zeros_count: int, column_name: int, filter_frame: pandas.DataFrame) -> pandas.DataFrame:
    if ones_count < zeros_count:
        return filter_frame.loc[filter_frame[column_name] == '1']
    return filter_frame.loc[filter_frame[column_name] == '0']


def find_bit_row(input_matrix: list, columns_in_frame: int, filter: types.FunctionType) -> BitTranslator:
    bit_frame = pd.DataFrame(input_matrix)
    for current_column in range(columns_in_frame):
        if len(bit_frame) == 1:
            break
        bit_counts = bit_frame[current_column].value_counts()
        ones = bit_counts['1']
        zeros = bit_counts['0']
        bit_frame = filter(ones, zeros, current_column, bit_frame)
    return BitTranslator(bit_frame.head(1).values[0])


if __name__ == '__main__':
    # data = ['00100', '11110', '10110', '10111', '10101', '01111', '00111', '11100', '10000', '11001', '00010', '01010']
    data = get_data(day=3, year=2021).splitlines()
    columns = []
    column_count = 0
    for line in data:
        if column_count == 0:
            column_count = len(line)
            columns = [[] for i in range(column_count)]
        for index, current_bit in enumerate(line):
            columns[index].append(current_bit)
    power = get_power(columns)
    print(f"Part 1 {power.current() * power.inverted()}")
    # Part 2
    matrix = lines_as_matrix(data)
    oxygen = find_bit_row(matrix, column_count, oxygen_filter)
    co2 = find_bit_row(matrix, column_count, co2_filter)
    print(f"Part 2 {oxygen.current() * co2.current()}")
