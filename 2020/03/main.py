import functools
import os
import sys

from lib.executor import Executor


CWD = os.path.dirname(os.path.abspath(__file__))


def parse_input(input):
    def parse_line(line):
        return [1 if c == "#" else 0 for c in line]

    return [parse_line(l) for l in input]


def num_trees(grid, down_steps, right_steps):
    num_trees = 0
    for row in range(0, len(grid), down_steps):
        col = row // down_steps * right_steps % len(grid[0])
        num_trees += grid[row][col]
    return num_trees


def part1_solution(input):
    return num_trees(parse_input(input), 1, 3)


def part2_solution(input):
    slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
    grid = parse_input(input)
    num_trees_list = [num_trees(grid, s[0], s[1]) for s in slopes]
    product = functools.reduce(lambda a, b: a * b, num_trees_list)
    return product


executor = Executor(
    [l.rstrip() for l in open(f"{CWD}/input.txt", "r").readlines()],
    part1_solution,
    part2_solution,
)
executor(sys.argv)
