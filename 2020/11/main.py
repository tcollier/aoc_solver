import os

CWD = os.path.dirname(os.path.abspath(__file__))
INPUT = [l.rstrip() for l in open(f"{CWD}/input.txt", "r").readlines()]

DIRECTIONS = [-1 - 1j, -1j, 1 - 1j, -1, 1, -1 + 1j, 1j, 1 + 1j]

FLOOR = "."
EMPTY = "L"
OCCUPIED = "#"


def part1_occupied_count(occupied, floor, seat, max_seat):
    num_occupied = 0
    for direction in DIRECTIONS:
        neighbor = seat + direction
        if 0 <= neighbor.real < max_seat.real and 0 <= neighbor.imag < max_seat.imag:
            if neighbor in occupied:
                num_occupied += 1
    return num_occupied


def part2_occupied_count(occupied, floor, seat, max_seat):
    num_occupied = 0
    for direction in DIRECTIONS:
        neighbor = seat + direction
        while 0 <= neighbor.real < max_seat.real and 0 <= neighbor.imag < max_seat.imag:
            if neighbor in occupied:
                num_occupied += 1
                break
            elif neighbor not in floor:
                break
            neighbor += direction
    return num_occupied


def iterate(occupied, floor, max_seat, visible_threshold, occupiend_count_fn):
    next_occupied = set()
    for row in range(round(max_seat.imag)):
        for col in range(round(max_seat.real)):
            seat = col + row * 1j
            if seat in floor:
                continue
            num_occupied = occupiend_count_fn(occupied, floor, col + row * 1j, max_seat)
            if seat not in occupied and num_occupied == 0:
                next_occupied.add(seat)
            elif seat in occupied and num_occupied < visible_threshold:
                next_occupied.add(seat)
    return next_occupied


def print_ans(input, visible_threshold, occupied_count_fn):
    occupied = set()
    floor = set()
    for row, line in enumerate(input):
        for col, c in enumerate(line):
            if c == OCCUPIED:
                occupied.add(col + row * 1j)
            elif c == FLOOR:
                floor.add(col + row * 1j)

    prev_occupied = None
    while True:
        occupied = iterate(
            occupied,
            floor,
            len(input[0]) + len(input) * 1j,
            visible_threshold,
            occupied_count_fn,
        )
        if occupied == prev_occupied:
            break
        prev_occupied = occupied

    print(len(occupied))


print_ans(INPUT, 4, part1_occupied_count)
print_ans(INPUT, 5, part2_occupied_count)
