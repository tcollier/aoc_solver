import re

INPUT = [l.rstrip() for l in open("day16_input.txt", "r").readlines()]


def ticket_parts(input):
    parts = {}
    for line in input:
        if line == "":
            return parts
        else:
            match = re.match(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)", line)
            parts[match[1]] = [
                range(int(match[2]), int(match[3]) + 1),
                range(int(match[4]), int(match[5]) + 1),
            ]


def valid_numbers(input):
    max_val = 0
    range_max = 0
    for _, rngs in ticket_parts(input).items():
        for rng in rngs:
            range_max = max(i for i in rng)
            if range_max > max_val:
                max_val = range_max
    valid_nums = [False for _ in range(range_max + 1)]
    for _, rngs in ticket_parts(input).items():
        for rng in rngs:
            for i in rng:
                valid_nums[i] = True
    return valid_nums


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


def print_part1_ans(input):
    valid_nums = valid_numbers(input)
    invalid_sum = 0
    for ticket in nearby_tickets(input):
        for num in ticket:
            if num >= len(valid_nums) or not valid_nums[num]:
                invalid_sum += num
    print(invalid_sum)


def print_part2_ans(input):
    valid_nums = valid_numbers(input)
    valid_tickets = []
    for ticket in nearby_tickets(input):
        valid = True
        for num in ticket:
            if num >= len(valid_nums) or not valid_nums[num]:
                valid = False
                break
        if valid:
            valid_tickets.append(ticket)
    parts = ticket_parts(input)
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
    my_tick = my_ticket(input)
    for i, part in enumerate(part_order):
        if re.match(r"departure", part):
            product *= my_tick[i]
    print(product)


print_part2_ans(INPUT)
