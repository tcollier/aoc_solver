INPUT = open("day12_input.txt", "r").readlines()

DIRECTIONS = ["E", "S", "W", "N"]

MOVE = {
    "E": lambda east, north, _, dist: (east + dist, north),
    "S": lambda east, north, _, dist: (east, north - dist),
    "W": lambda east, north, _, dist: (east - dist, north),
    "N": lambda east, north, _, dist: (east, north + dist),
}


def part1_move_forward(east, north, dir_index, dist):
    fn = MOVE[DIRECTIONS[dir_index]]
    return fn(east, north, dir_index, dist)


MOVE["F"] = part1_move_forward


def part1_apply_instruction(east, north, dir_index, instruction):
    if instruction[0] in ["R", "L"]:
        steps = int(instruction[1:]) // 90
        if instruction[0] == "L":
            steps = -steps
        dir_index = (dir_index + steps) % len(DIRECTIONS)
    else:
        fn = MOVE[instruction[0]]
        east, north = fn(east, north, dir_index, int(instruction[1:]))
    return east, north, dir_index


def print_part1_ans(input):
    east = north = dir_index = 0
    for instruction in input:
        east, north, dir_index = part1_apply_instruction(east, north, dir_index, instruction.rstrip())
    print(abs(east) + abs(north))


class Point(object):
    def __init__(self, east, north):
        self.east = east
        self.north = north


def part2_apply_instruction(ship, waypoint, instruction):
    if instruction[0] in ["R", "L"]:
        steps = int(instruction[1:]) // 90
        for _ in range(steps):
            if instruction[0] == "R":
                waypoint = Point(waypoint.north, -waypoint.east)
            else:
                waypoint = Point(-waypoint.north, waypoint.east)
    elif instruction[0] == "F":
        dist = int(instruction[1:])
        ship = Point(
            ship.east + dist * waypoint.east,
            ship.north + dist * waypoint.north
        )
    else:
        fn = MOVE[instruction[0]]
        east, north = fn(waypoint.east, waypoint.north, None, int(instruction[1:]))
        waypoint = Point(east, north)
    return ship, waypoint


def print_part2_ans(input):
    ship = Point(0, 0)
    waypoint = Point(10, 1)
    for instruction in input:
        ship, waypoint = part2_apply_instruction(ship, waypoint, instruction.rstrip())
    print(abs(ship.east) + abs(ship.north))


print_part2_ans(INPUT)
