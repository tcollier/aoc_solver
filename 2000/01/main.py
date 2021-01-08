import sys

from lib.executor import Executor


def part1_solution(input):
    return input[0]


def part2_solution(input):
    return input[1]


executor = Executor(["Hello", "World!"], part1_solution, part2_solution)
executor(sys.argv)
