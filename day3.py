from aocd import get_data
from dataclasses import dataclass

@dataclass
class Power:
    decimal: int
    binary: str

if __name__ == '__main__':
    #data = ['00100','11110','10110','10111','10101','01111','00111','11100','10000','11001','00010','01010']
    data = get_data(day=3).splitlines()

    columns = []
    column_count = 0
    for line in data:
        if column_count == 0:
            column_count = len(line)
            columns = [[] for i in range(column_count)]
        for index, current_bit in enumerate(line):
            columns[index].append(current_bit)

    gamma_values = []
    epsilon_values = []
    for column in columns:
        gamma_values.append(max(set(column), key=column.count))
        epsilon_values.append(min(set(column), key=column.count))
    gamma_text = "".join(gamma_values)
    epsilon_text = "".join(epsilon_values)

    gamma = Power(int(gamma_text, 2), gamma_text)
    epsilon = Power(int(epsilon_text, 2), epsilon_text)

    print(f"Part 1 {gamma.decimal * epsilon.decimal}")
