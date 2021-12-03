from aocd import get_data
from dataclasses import dataclass
from parse import parse

@dataclass
class Position:
    horizontal: int = 0
    vertical: int = 0
    aim: int = 0

    def distance(self) -> int:
        return self.horizontal * self.vertical

@dataclass
class Movement:
    type: str
    unit: int = 0

if __name__ == '__main__':
    # data = [
    #     "forward 5",
    #     "down 5",
    #     "forward 8",
    #     "up 3",
    #     "down 8",
    #     "forward 2"
    # ]

    data = get_data(day=2).splitlines()

    movements = []
    for line in data:
        direction, value = parse("{} {}", line)
        movements.append(Movement(direction, int(value)))

    dive_tracker = Position()
    aimed_tracker = Position()

    for movement in movements:
        to_add = movement.unit
        if movement.type == "up":
            to_add = to_add * -1
        if movement.type in ["up", "down"]:
            dive_tracker.vertical = dive_tracker.vertical + to_add
            aimed_tracker.aim = aimed_tracker.aim + to_add
        else:
            dive_tracker.horizontal = dive_tracker.horizontal + to_add
            aimed_tracker.horizontal = aimed_tracker.horizontal + to_add
            aimed_tracker.vertical = aimed_tracker.aim * to_add + aimed_tracker.vertical

    print(f"Part 1 {dive_tracker.distance()}")
    print(f"Part 2 {aimed_tracker.distance()}")

