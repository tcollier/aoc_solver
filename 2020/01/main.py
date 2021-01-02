import math
import os


CWD = os.path.dirname(os.path.abspath(__file__))
INPUT = [int(l.rstrip()) for l in open(f"{CWD}/input.txt", "r").readlines()]


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


INPUT.sort()

bit_vec = BitVector(2020)
for num in INPUT:
    bit_vec.set(num)

pair = pair_with_sum(INPUT, bit_vec, 2020)
print(pair[0] * pair[1])

trip = triple_with_sum(INPUT, 2020)
print(trip[0] * trip[1] * trip[2])
