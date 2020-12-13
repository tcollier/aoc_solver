import math

INPUT = open("day13_input.txt", "r").readlines()


def print_part1_ans(input):
    timestamp = int(input[0].rstrip())
    bus_ids = [int(n) for n in input[1].rstrip().split(",") if n != "x"]
    min_wait = math.inf
    min_wait_id = None
    for bus_id in bus_ids:
        wait_time = bus_id - timestamp % bus_id
        if wait_time < min_wait:
            min_wait = wait_time
            min_wait_id = bus_id
    print(min_wait_id * min_wait)


print_part1_ans(INPUT)
