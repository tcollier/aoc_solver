import os
import sys

from lib.executor import Executor


CWD = os.path.dirname(os.path.abspath(__file__))


def part1_solution(input):
    input = [n for n in input]
    input.append(0)
    input.sort()
    input.append(input[-1] + 3)
    num_1_diff = num_3_diff = 0
    for i in range(1, len(input)):
        diff = input[i] - input[i - 1]
        if diff == 1:
            num_1_diff += 1
        elif diff == 3:
            num_3_diff += 1
    return num_1_diff * num_3_diff


def part2_solution(input):
    input = [n for n in input]
    input.append(0)
    input.sort()
    counts = [0 for _ in input]
    counts[0] = counts[1] = 1
    for i in range(2, len(input)):
        for j in range(max(0, i - 3), i):
            if input[i] - input[j] <= 3:
                counts[i] += counts[j]
    return counts[-1]


executor = Executor(
    [int(l.rstrip()) for l in open(f"{CWD}/input.txt", "r").readlines()],
    part1_solution,
    part2_solution,
)
executor(sys.argv)
