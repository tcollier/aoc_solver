INPUT = open("day11_input.txt", "r").readlines()

DIRECTIONS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]

FLOOR = "."
EMPTY = "L"
OCCUPIED = "#"


def part1_occupied_count(seats, row, col):
    num_occupied = 0
    for adj_row in range(max(0, row - 1), min(row + 2, len(seats))):
        for adj_col in range(max(0, col - 1), min(col + 2, len(seats[adj_row]))):
            if row == adj_row and col == adj_col:
                continue
            if seats[adj_row][adj_col] == OCCUPIED:
                num_occupied = num_occupied + 1
    return num_occupied


def part2_occupied_count(seats, row, col):
    num_occupied = 0
    for direction in DIRECTIONS:
        adj_row = row + direction[0]
        adj_col = col + direction[1]
        while (
            adj_row >= 0
            and adj_row < len(seats)
            and adj_col >= 0
            and adj_col < len(seats[adj_row])
        ):
            if seats[adj_row][adj_col] == OCCUPIED:
                num_occupied = num_occupied + 1
                break
            if seats[adj_row][adj_col] == EMPTY:
                break
            adj_row = adj_row + direction[0]
            adj_col = adj_col + direction[1]

    return num_occupied


def iterate(seats, visible_threshold, occupiend_count_fn):
    next_seats = [[s for s in row] for row in seats]
    for row in range(len(seats)):
        for col in range(len(seats[row])):
            if seats[row][col] == FLOOR:
                continue
            num_occupied = occupiend_count_fn(seats, row, col)
            if seats[row][col] == EMPTY and num_occupied == 0:
                next_seats[row][col] = OCCUPIED
            elif seats[row][col] == OCCUPIED and num_occupied >= visible_threshold:
                next_seats[row][col] = EMPTY
    return next_seats


def count_occupied(seats):
    total = 0
    for row in range(len(seats)):
        for col in range(len(seats[row])):
            if seats[row][col] == OCCUPIED:
                total += 1
    return total


def print_seats(seats):
    print("\n".join(["".join(r) for r in seats]))


def print_ans(input, visible_threshold, occupiend_count_fn):
    seats = [[s for s in l.rstrip()] for l in input]
    iterations = 0
    prev_seats = None
    while True:
        seats = iterate(seats, visible_threshold, occupiend_count_fn)
        if seats == prev_seats:
            break
        iterations = iterations + 1
        prev_seats = seats

    print(count_occupied(seats))


print_ans(INPUT, 5, part2_occupied_count)
