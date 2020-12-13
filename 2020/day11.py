INPUT = open("day11_input.txt", "r").readlines()


def part1_occupied_count(seats, row, col):
    num_occupied = 0
    for adj_row in range(max(0, row - 1), min(row + 2, len(seats))):
        for adj_col in range(max(0, col - 1), min(col + 2, len(seats[adj_row]))):
            if row == adj_row and col == adj_col:
                continue
            if seats[adj_row][adj_col] == "#":
                num_occupied = num_occupied + 1
    return num_occupied


def iterate(seats, occupiend_count_fn):
    next_seats = [[s for s in row] for row in seats]
    for row in range(len(seats)):
        for col in range(len(seats[row])):
            if seats[row][col] == ".":
                continue
            num_occupied = occupiend_count_fn(seats, row, col)
            if seats[row][col] == "L" and num_occupied == 0:
                next_seats[row][col] = "#"
            elif seats[row][col] == "#" and num_occupied >= 4:
                next_seats[row][col] = "L"
    return next_seats


def count_occupied(seats):
    total = 0
    for row in range(len(seats)):
        for col in range(len(seats[row])):
            if seats[row][col] == "#":
                total += 1
    return total


def print_ans(input, occupiend_count_fn):
    seats = [[s for s in l.rstrip()] for l in input]
    iterations = 0
    prev_seats = None
    while True:
        seats = iterate(seats, occupiend_count_fn)
        if seats == prev_seats:
            break
        iterations = iterations + 1
        prev_seats = seats
    print(count_occupied(seats))


print_ans(INPUT, part1_occupied_count)
