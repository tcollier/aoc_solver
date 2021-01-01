import os
import re

CWD = os.path.dirname(os.path.abspath(__file__))
INPUT = [l.rstrip() for l in open(f"{CWD}/input.txt", "r").readlines()]

BIT_LEN = 36


def parse_mask_part1(raw):
    zeros_mask = ones_mask = 0
    for i in range(BIT_LEN):
        zeros_mask <<= 1  # Mask where zeros have an effect
        ones_mask <<= 1  # Mask where ones have an effect
        if raw[i] != "0":
            zeros_mask += 1
        if raw[i] == "1":
            ones_mask += 1
    return zeros_mask, ones_mask


def print_part1_ans(input):
    values = {}
    for line in input:
        match = re.match(r"^(.+) = (.+)$", line)
        if match[1] == "mask":
            zeros_mask, ones_mask = parse_mask_part1(match[2])
        else:
            addr_match = re.match(r"^mem\[(\d+)\]$", match[1])
            addr = addr_match[1]
            values[addr] = int(match[2]) & zeros_mask | ones_mask
    total = 0
    for value in values.values():
        total += value
    print(total)


def parse_mask_part2(raw):
    ones_mask = 0
    floating_masks = []
    floating_mask = 1 << BIT_LEN
    for i in range(BIT_LEN):
        floating_mask >>= 1
        ones_mask <<= 1  # Mask where ones have an effect
        if raw[i] == "1":
            ones_mask += 1
        elif raw[i] == "X":
            floating_masks.append(floating_mask)
    return ones_mask, floating_masks


def store_part_2(values, addr, floating_masks, value, index=0):
    if index == len(floating_masks):
        values[addr] = value
        return
    addr_with_0 = addr & ~floating_masks[index]
    addr_with_1 = addr | floating_masks[index]
    store_part_2(values, addr_with_0, floating_masks, value, index + 1)
    store_part_2(values, addr_with_1, floating_masks, value, index + 1)


def print_part2_ans(input):
    values = {}
    for line in input:
        match = re.match(r"^(.+) = (.+)$", line)
        if match[1] == "mask":
            ones_mask, floating_masks = parse_mask_part2(match[2])
        else:
            addr_match = re.match(r"^mem\[(\d+)\]$", match[1])
            base_addr = int(addr_match[1]) | ones_mask
            store_part_2(values, base_addr, floating_masks, int(match[2]))
    total = 0
    for value in values.values():
        total += value
    print(total)


print_part1_ans(INPUT)
print_part2_ans(INPUT)
