import math
import os
import sys

from lib.executor import Executor


CWD = os.path.dirname(os.path.abspath(__file__))


def pair_with_sum(numbers, sum):
    others = set(numbers)
    for num in numbers:
        if (sum - num) in others:
            return (num, sum - num)
    raise Exception(f"Pair with sum {sum} not found")


def triple_with_sum(numbers, sum):
    numbers.sort()
    for i, val in enumerate(numbers):
        j = i + 1
        k = len(numbers) - 1
        while j < k:
            if val + numbers[j] + numbers[k] == sum:
                return (val, numbers[j], numbers[k])
            elif val + numbers[j] + numbers[k] < sum:
                j += 1
            else:
                k -= 1
    raise Exception(f"Triplet with sum {sum} not found")


def part1_solution(input):
    pair = pair_with_sum(input, 2020)
    return pair[0] * pair[1]


def part2_solution(input):
    trip = triple_with_sum(input, 2020)
    return trip[0] * trip[1] * trip[2]


executor = Executor(
    [int(l.rstrip()) for l in open(f"{CWD}/input.txt", "r").readlines()],
    part1_solution,
    part2_solution,
)
executor(sys.argv)
