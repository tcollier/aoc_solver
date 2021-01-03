import os
import sys

from lib.executor import Executor


CWD = os.path.dirname(os.path.abspath(__file__))


def string_to_id(str):
    id = 0
    for char in str:
        id <<= 1
        if char in ["B", "R"]:
            id += 1
    return id


def part1_solution(input):
    max_id = 0
    for line in input:
        id = string_to_id(line)
        if id > max_id:
            max_id = id
    return max_id


def part2_solution(input):
    ids = {string_to_id(l) for l in input}
    for id in ids:
        if id + 1 not in ids and id + 2 in ids:
            return id + 1


executor = Executor(
    [l.rstrip() for l in open(f"{CWD}/input.txt", "r").readlines()],
    part1_solution,
    part2_solution,
)
executor(sys.argv)
