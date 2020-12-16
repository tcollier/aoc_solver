import re

INPUT = [l.rstrip() for l in open("day16_input.txt", "r").readlines()]


def print_part1_ans(input):
    parse_state = "start"
    ranges = []
    valid_nums = []
    invalid_sum = 0
    for line in input:
        if parse_state == "start":
            if line == "":
                parse_state = "mine"
                max_val = 0
                for rng in ranges:
                    range_max = max(i for i in rng)
                    if range_max > max_val:
                        max_val = range_max
                valid_nums = [False for _ in range(range_max + 1)]
                for rng in ranges:
                    for i in rng:
                        valid_nums[i] = True
            else:
                match = re.match(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)", line)
                ranges.append(range(int(match[2]), int(match[3]) + 1))
                ranges.append(range(int(match[4]), int(match[5]) + 1))
        elif parse_state == "mine":
            if line == "":
                parse_state = "nearby"
        elif line != "nearby tickets:":
            for num in [int(i) for i in line.split(",")]:
                if num >= len(valid_nums) or not valid_nums[num]:
                    invalid_sum += num
    print(invalid_sum)


print_part1_ans(INPUT)
