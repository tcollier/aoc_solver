import os
import re
import sys

from lib.executor import Executor

CWD = os.path.dirname(os.path.abspath(__file__))


def valid_part1(min, max, char, pwd):
    num_char = 0
    for c in pwd:
        if c == char:
            num_char += 1
            if num_char > max:
                return False
    return num_char >= min


def valid_part2(pos1, pos2, char, pwd):
    return (pwd[pos1 - 1] == char) != (pwd[pos2 - 1] == char)


def num_valid(input, valid_fn):
    num_correct = 0
    for line in input:
        match = re.match(r"^(\d+)-(\d+) (\w): (\w+)$", line)
        if valid_fn(int(match[1]), int(match[2]), match[3], match[4]):
            num_correct += 1
    return num_correct


def part1_solution(input):
    return num_valid(input, valid_part1)


def part2_solution(input):
    return num_valid(input, valid_part2)


executor = Executor(
    [l.rstrip() for l in open(f"{CWD}/input.txt", "r").readlines()],
    part1_solution,
    part2_solution,
)
executor(sys.argv)
