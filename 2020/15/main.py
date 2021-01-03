import sys

from lib.executor import Executor


def play(input, num_rounds):
    last_usage = [-1] * num_rounds
    for i in range(len(input) - 1):
        last_usage[input[i]] = i
    prev_num = input[-1]
    for i in range(len(input), num_rounds):
        if last_usage[prev_num] >= 0:
            curr_num = i - 1 - last_usage[prev_num]
        else:
            curr_num = 0
        last_usage[prev_num] = i - 1
        prev_num = curr_num
    return curr_num


def part1_solution(input):
    return play(input, 2020)


def part2_solution(input):
    return play(input, 30000000)


executor = Executor([14, 3, 1, 0, 9, 5], part1_solution, part2_solution)
executor(sys.argv)
