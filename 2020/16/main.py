import os
import re

CWD = os.path.dirname(os.path.abspath(__file__))
INPUT = [l.rstrip() for l in open(f"{CWD}/input.txt", "r").readlines()]


def parse_input(input):
    parse_state = "start"
    parts = {}
    mine = None
    nearby = []
    for line in input:
        if parse_state == "start":
            if line == "":
                parse_state = "mine"
            else:
                match = re.match(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)", line)
                parts[match[1]] = [
                    range(int(match[2]), int(match[3]) + 1),
                    range(int(match[4]), int(match[5]) + 1),
                ]
        elif parse_state == "mine":
            if line == "":
                parse_state = "nearby"
            elif line != "your ticket:":
                mine = [int(i) for i in line.split(",")]
        elif line != "nearby tickets:":
            nearby.append([int(i) for i in line.split(",")])
    return {"parts": parts, "mine": mine, "nearby": nearby}


def valid_numbers(parts):
    max_val = 0
    range_max = 0
    for _, rngs in parts.items():
        for rng in rngs:
            range_max = max(i for i in rng)
            if range_max > max_val:
                max_val = range_max
    valid_nums = [False for _ in range(range_max + 1)]
    for _, rngs in parts.items():
        for rng in rngs:
            for i in rng:
                valid_nums[i] = True
    return valid_nums


def print_part1_ans(input):
    invalid_sum = 0
    data = parse_input(input)
    valid_nums = valid_numbers(data["parts"])
    for ticket in data["nearby"]:
        for num in ticket:
            if num >= len(valid_nums) or not valid_nums[num]:
                invalid_sum += num
    print(invalid_sum)


def print_part2_ans(input):
    valid_tickets = []
    data = parse_input(input)
    valid_nums = valid_numbers(data["parts"])
    for ticket in data["nearby"]:
        valid = True
        for num in ticket:
            if num >= len(valid_nums) or not valid_nums[num]:
                valid = False
                break
        if valid:
            valid_tickets.append(ticket)
    parts = data["parts"]
    possible_part_order = []
    for i in range(len(parts)):
        available_parts = set()
        for part in parts.keys():
            if part not in possible_part_order:
                available_parts.add(part)
        for ticket in valid_tickets:
            for part in available_parts:
                if ticket[i] not in parts[part][0] and ticket[i] not in parts[part][1]:
                    available_parts.remove(part)
                    break
        possible_part_order.append(available_parts)
    part_order = [None for _ in range(len(possible_part_order))]
    done = False
    while not done:
        for i in range(len(possible_part_order)):
            if len(possible_part_order[i]) == 1:
                part_order[i] = possible_part_order[i].pop()
            for j in range(len(possible_part_order)):
                if part_order[i] in possible_part_order[j]:
                    possible_part_order[j].remove(part_order[i])
        done = True
        for i in range(len(part_order)):
            if part_order[i] is None:
                done = False
                break
    product = 1
    my_ticket = data["mine"]
    for i, part in enumerate(part_order):
        if re.match(r"departure", part):
            product *= my_ticket[i]
    print(product)


print_part1_ans(INPUT)
print_part2_ans(INPUT)
