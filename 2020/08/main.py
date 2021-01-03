import os
import sys

from lib.executor import Executor


CWD = os.path.dirname(os.path.abspath(__file__))


def run(instructions, fail_on_loop):
    acc = 0
    curr_ptr = 0
    visited = set()
    while curr_ptr < len(instructions):
        if curr_ptr in visited:
            if fail_on_loop:
                raise Exception("Infinite loop detected")
            else:
                return acc
        visited.add(curr_ptr)
        instruction = instructions[curr_ptr]
        if instruction[0:3] == "acc":
            acc += int(instruction[4:])
            curr_ptr += 1
        elif instruction[0:3] == "jmp":
            curr_ptr += int(instruction[4:])
        elif instruction[0:3] == "nop":
            curr_ptr += 1
    return acc


def part1_solution(input):
    return run(input, False)


def part2_solution(input):
    for i in range(len(input)):
        orig = input[i]
        if orig[0:3] == "jmp":
            input[i] = f"nop {orig[4:]}"
        elif orig[0:3] == "nop":
            input[i] = f"jmp {orig[4:]}"
        else:
            continue

        try:
            return run(input, True)
        except:
            pass
        input[i] = orig


executor = Executor(
    [l.rstrip() for l in open(f"{CWD}/input.txt", "r").readlines()],
    part1_solution,
    part2_solution,
)
executor(sys.argv)
