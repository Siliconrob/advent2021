from aocd import get_data

# Wrote this printout function to do compare with Part 1 test outputs
# luckily that was the part 2.  WoooHOOO
def printout(current_paper: dict, fold_cmd: str, max_x: int, max_y: int):
    in_process = [["." for x in range(max_x)] for y in range(max_y)]
    for dot in current_paper:
        dot_x, dot_y = dot[0], dot[1]
        in_process[dot_y][dot_x] = "#"
    print(f'Fold {fold_cmd}')
    for line in ["".join(row) for row in in_process]:
        print(line)


if __name__ == '__main__':
    # test_data_dots = [
    #     "6,10",
    #     "0,14",
    #     "9,10",
    #     "0,3",
    #     "10,4",
    #     "4,11",
    #     "6,0",
    #     "6,12",
    #     "4,1",
    #     "0,13",
    #     "10,12",
    #     "3,4",
    #     "3,0",
    #     "8,4",
    #     "1,10",
    #     "2,14",
    #     "8,10",
    #     "9,0"
    # ]
    # test_data_folds = [
    #     "fold along y=7",
    #     "fold along x=5"
    # ]
    data = get_data(day=13, year=2021).split("\n\n")
    folds = [(fold[0][-1], int(fold[-1])) for fold in [fold_instr.split("=") for fold_instr in data.pop().splitlines()]]
    dots = [(int(pos[0]), int(pos[1])) for pos in [coord.split(",") for coord in data.pop().splitlines()]]
    #folds = [(fold[0][-1], int(fold[-1])) for fold in [fold_instr.split("=") for fold_instr in test_data_folds]]
    #dots = [(int(pos[0]), int(pos[1])) for pos in [coord.split(",") for coord in test_data_dots]]

    paper = {} # use dictionary because coords are jagged
    for dot in dots:
        paper[(dot[0], dot[1])] = True

    the_keys = paper.keys()
    max_x = max([key[0] for key in the_keys]) + 1
    max_y = max([key[1] for key in the_keys]) + 1

    for index, fold in enumerate(folds):
        if index == 1: # Part 1 answer only
            printout(paper, fold, max_x, max_y)
            part1_solution = len(paper.keys())
        fold_axis, fold_value = fold
        folded_paper = {}
        if fold_axis == "x":
            for (x, y) in paper:
                if x < fold_value: # coord is above the fold
                    folded_paper[(x, y)] = True
                else:
                    # Subtract the fold value from the current coord to mirror it
                    folded_x = fold_value - (x - fold_value)
                    print(f'Change from {x} to {folded_x}')
                    folded_paper[(folded_x, y)] = True
            max_x = max_x - (fold_value + 1)
        else:
            for (x, y) in paper:
                if y < fold_value:
                    folded_paper[(x, y)] = True
                else:
                    # Subtract the fold value from the current coord to mirror it
                    folded_y = fold_value - (y - fold_value)
                    print(f'Change from {y} to {folded_y}')
                    folded_paper[(x, folded_y)] = True
            max_y = max_y - (fold_value + 1)
        paper = folded_paper
    print(f'Part 1: {part1_solution}')

    the_keys = paper.keys()
    max_x = max([key[0] for key in the_keys]) + 1
    max_y = max([key[1] for key in the_keys]) + 1
    printout(paper, 'final', max_x, max_y)