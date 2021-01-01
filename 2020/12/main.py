import os

CWD = os.path.dirname(os.path.abspath(__file__))
INPUT = [l.rstrip() for l in open(f"{CWD}/input.txt", "r").readlines()]

DIRECTIONS = ["E", "S", "W", "N"]

MOVE = {
    "E": lambda point, _, dist: point + dist,
    "S": lambda point, _, dist: point - dist * 1j,
    "W": lambda point, _, dist: point - dist,
    "N": lambda point, _, dist: point + dist * 1j,
}


def part1_move_forward(point, dir_index, dist):
    fn = MOVE[DIRECTIONS[dir_index]]
    return fn(point, dir_index, dist)


MOVE["F"] = part1_move_forward


def part1_apply_instruction(point, dir_index, instruction):
    if instruction[0] in ["R", "L"]:
        steps = int(instruction[1:]) // 90
        if instruction[0] == "L":
            steps = -steps
        dir_index = (dir_index + steps) % len(DIRECTIONS)
    else:
        fn = MOVE[instruction[0]]
        point = fn(point, dir_index, int(instruction[1:]))
    return point, dir_index


def print_part1_ans(input):
    point = 0
    dir_index = 0
    for instruction in input:
        point, dir_index = part1_apply_instruction(
            point, dir_index, instruction.rstrip()
        )
    print(round(abs(point.real) + abs(point.imag)))


def part2_apply_instruction(ship, waypoint, instruction):
    if instruction[0] in ["R", "L"]:
        steps = int(instruction[1:]) // 90
        for _ in range(steps):
            if instruction[0] == "R":
                waypoint *= -1j
            else:
                waypoint *= 1j
    elif instruction[0] == "F":
        dist = int(instruction[1:])
        ship = ship + dist * waypoint
    else:
        fn = MOVE[instruction[0]]
        waypoint = fn(waypoint, None, int(instruction[1:]))
    return ship, waypoint


def print_part2_ans(input):
    ship = 0
    waypoint = 10 + 1j
    for instruction in input:
        ship, waypoint = part2_apply_instruction(ship, waypoint, instruction.rstrip())
    print(round(abs(ship.real) + abs(ship.imag)))


print_part1_ans(INPUT)
print_part2_ans(INPUT)
