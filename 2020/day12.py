class Point(object):
    def __init__(self, east, north):
        self.east = east
        self.north = north


INPUT = open("day12_input.txt", "r").readlines()

DIRECTIONS = ["E", "S", "W", "N"]

MOVE = {
    "E": lambda point, _, dist: Point(point.east + dist, point.north),
    "S": lambda point, _, dist: Point(point.east, point.north - dist),
    "W": lambda point, _, dist: Point(point.east - dist, point.north),
    "N": lambda point, _, dist: Point(point.east, point.north + dist),
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
    point = Point(0, 0)
    dir_index = 0
    for instruction in input:
        point, dir_index = part1_apply_instruction(
            point, dir_index, instruction.rstrip()
        )
    print(abs(point.east) + abs(point.north))


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
            ship.east + dist * waypoint.east, ship.north + dist * waypoint.north
        )
    else:
        fn = MOVE[instruction[0]]
        waypoint = fn(waypoint, None, int(instruction[1:]))
    return ship, waypoint


def print_part2_ans(input):
    ship = Point(0, 0)
    waypoint = Point(10, 1)
    for instruction in input:
        ship, waypoint = part2_apply_instruction(ship, waypoint, instruction.rstrip())
    print(abs(ship.east) + abs(ship.north))


print_part1_ans(INPUT)
print_part2_ans(INPUT)
