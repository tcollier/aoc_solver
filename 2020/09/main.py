import os
import sys

from lib.executor import Executor


CWD = os.path.dirname(os.path.abspath(__file__))


POOL_SIZE = 25


def first_invalid_number(input):
    number_pool = set(input[0:POOL_SIZE])
    for i in range(POOL_SIZE, len(input)):
        valid = False
        for j in range(POOL_SIZE):
            if (input[i] - input[i - POOL_SIZE + j]) in number_pool:
                valid = True
                break
        if not valid:
            return i, input[i]
        number_pool.remove(input[i - POOL_SIZE])
        number_pool.add(input[i])


def part1_solution(input,):
    return first_invalid_number(input)[1]


def part2_solution(input):
    max_index, target_num = first_invalid_number(input)
    for i in range(max_index):
        sum = input[i]
        for j in range(i + 1, max_index):
            sum += input[j]
            if sum == target_num:
                elems = input[i : j + 1]
                elems.sort()
                return elems[0] + elems[-1]
            elif sum > target_num:
                break


executor = Executor(
    [int(l.rstrip()) for l in open(f"{CWD}/input.txt", "r").readlines()],
    part1_solution,
    part2_solution,
)
executor(sys.argv)
