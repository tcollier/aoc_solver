import math
import os
import sys

from lib.executor import Executor


CWD = os.path.dirname(os.path.abspath(__file__))


class BitVector(object):
    NUM_BITS = 64  # Must be a power of 2
    MASK = NUM_BITS - 1
    SHIFTER = math.floor(math.log(NUM_BITS, 2))

    def __init__(self, max_value):
        self.bits = [0] * ((max_value >> self.SHIFTER) + 1)

    def set(self, value):
        self.bits[value >> self.SHIFTER] |= 1 << (value & self.MASK)

    def test(self, value):
        return self.bits[value >> self.SHIFTER] & 1 << (value & self.MASK) > 0

    def sorted_values(self):
        values = []
        for i, bits in enumerate(self.bits):
            num = i * self.NUM_BITS
            while bits:
                if bits & 1:
                    values.append(num)
                num += 1
                bits >>= 1
        return values


def pair_with_sum(numbers, bit_vec, sum):
    for num in numbers:
        if bit_vec.test(sum - num):
            return (num, sum - num)
    raise Exception(f"Pair with sum {sum} not found")


def triple_with_sum(arr, sum):
    for val_index, val in enumerate(arr):
        i = val_index + 1
        j = len(arr) - 1
        while i < j:
            if arr[i] + arr[j] + val == sum:
                return (val, arr[i], arr[j])
            elif arr[i] + arr[j] + val < sum:
                i += 1
            else:
                j -= 1
    raise Exception(f"Triplet with sum {sum} not found")


def part1_solution(input):
    bit_vec = BitVector(2020)
    for num in input:
        bit_vec.set(num)
    numbers = bit_vec.sorted_values()
    pair = pair_with_sum(numbers, bit_vec, 2020)
    return pair[0] * pair[1]


def part2_solution(input):
    bit_vec = BitVector(2020)
    for num in input:
        bit_vec.set(num)
    numbers = bit_vec.sorted_values()
    trip = triple_with_sum(numbers, 2020)
    return trip[0] * trip[1] * trip[2]


executor = Executor(
    [int(l.rstrip()) for l in open(f"{CWD}/input.txt", "r").readlines()],
    part1_solution,
    part2_solution,
)
executor(sys.argv)
