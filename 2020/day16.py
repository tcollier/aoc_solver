import re

INPUT = [l.rstrip() for l in open("day16_input.txt", "r").readlines()]


def my_ticket(input):
    parse_state = "start"
    for line in input:
        if parse_state == "start":
            if line == "":
                parse_state = "mine"
        elif parse_state == "mine":
            if line != "your ticket:":
                return [int(i) for i in line.split(",")]


def nearby_tickets(input):
    parse_state = "start"
    tickets = []
    for line in input:
        if parse_state == "start":
            if line == "":
                parse_state = "mine"
        elif parse_state == "mine":
            if line == "":
                parse_state = "nearby"
        elif line != "nearby tickets:":
            tickets.append([int(i) for i in line.split(",")])
    return tickets


def valid_numbers(input):
    ranges = []
    for line in input:
        if line == "":
            max_val = 0
            for rng in ranges:
                range_max = max(i for i in rng)
                if range_max > max_val:
                    max_val = range_max
            valid_nums = [False for _ in range(range_max + 1)]
            for rng in ranges:
                for i in rng:
                    valid_nums[i] = True
            return valid_nums
        else:
            match = re.match(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)", line)
            ranges.append(range(int(match[2]), int(match[3]) + 1))
            ranges.append(range(int(match[4]), int(match[5]) + 1))


def print_part1_ans(input):
    valid_nums = valid_numbers(input)
    invalid_sum = 0
    for ticket in nearby_tickets(input):
        for num in ticket:
            if num >= len(valid_nums) or not valid_nums[num]:
                invalid_sum += num
    print(invalid_sum)


print_part1_ans(INPUT)
