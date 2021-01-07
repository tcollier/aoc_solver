import sys

from lib.executor import Executor

# My input
CARD_PUBLIC_KEY = 15113849
DOOR_PUBLIC_KEY = 4206373

# Sample
# CARD_PUBLIC_KEY = 5764801
# DOOR_PUBLIC_KEY = 17807724

SUBJECT_NUMBER = 7
DIVISOR = 20201227


def loop_size(pubkey):
    loop = 0
    value = 1
    while value != pubkey:
        value *= SUBJECT_NUMBER
        value %= DIVISOR
        loop += 1
    return loop


def encrypt(pubkey, loop_size):
    value = 1
    for _ in range(loop_size):
        value *= pubkey
        value %= DIVISOR
    return value


def part1_solution(_):
    return encrypt(CARD_PUBLIC_KEY, loop_size(DOOR_PUBLIC_KEY))


def part2_solution(_):
    return ""


executor = Executor([], part1_solution, part2_solution)
executor(sys.argv)
