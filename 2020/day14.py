import re

INPUT = [l.rstrip() for l in open("day14_input.txt", "r").readlines()]

BIT_LEN = 36


def parse_mask_part1(raw):
    zeros_mask = ones_mask = 0
    for i in range(BIT_LEN):
        zeros_mask <<= 1  # Mask where zeros have an effect (NAND)
        ones_mask <<= 1  # Mask where ones have an effect (OR)
        if raw[i] != "0":
            zeros_mask += 1
        if raw[i] == "1":
            ones_mask += 1
    return zeros_mask, ones_mask


def print_part1_ans(input):
    zeros_mask = ones_mask = None
    values = {}
    for line in input:
        match = re.match(r"^(.+) = (.+)$", line)
        if match[1] == "mask":
            zeros_mask, ones_mask = parse_mask_part1(match[2])
        else:
            addr_match = re.match(r"^mem\[(\d+)\]$", match[1])
            addr = addr_match[1]
            raw_value = int(match[2])
            value = raw_value & zeros_mask
            value |= ones_mask
            values[addr] = value
    total = 0
    for value in values.values():
        total += value
    print(total)


def parse_mask_part2(raw):
    ones_mask = 0
    floating_bits = []
    for i in range(BIT_LEN):
        ones_mask <<= 1  # Mask where ones have an effect (OR)
        if raw[i] == "1":
            ones_mask += 1
        elif raw[i] == "X":
            floating_bits.append(BIT_LEN - i - 1)
    return ones_mask, floating_bits


def store_part_2(values, addr, floating_bits, value, index=0):
    if index == len(floating_bits):
        values[addr] = value
        return
    mask = 1 << floating_bits[index]
    store_part_2(values, addr | mask, floating_bits, value, index + 1)
    store_part_2(values, addr & ~mask, floating_bits, value, index + 1)


def print_part2_ans(input):
    ones_mask = None
    floating_bits = []
    values = {}
    for line in input:
        match = re.match(r"^(.+) = (.+)$", line)
        if match[1] == "mask":
            ones_mask, floating_bits = parse_mask_part2(match[2])
        else:
            addr_match = re.match(r"^mem\[(\d+)\]$", match[1])
            raw_addr = int(addr_match[1])
            addr = raw_addr | ones_mask
            store_part_2(values, addr, floating_bits, int(match[2]))
    total = 0
    for value in values.values():
        total += value
    print(total)


print_part2_ans(INPUT)
