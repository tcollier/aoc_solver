import math

INPUT = open("day13_input.txt", "r").readlines()


def print_part1_ans(input):
    timestamp = int(input[0].rstrip())
    bus_ids = [int(n) for n in input[1].rstrip().split(",") if n != "x"]
    min_wait = math.inf
    min_wait_id = None
    for bus_id in bus_ids:
        wait_time = bus_id - timestamp % bus_id
        if wait_time < min_wait:
            min_wait = wait_time
            min_wait_id = bus_id
    print(min_wait_id * min_wait)


def merge_factors(f1, f2):
    factors = {}
    for fact in set([k for k in f1.keys()] + [k for k in f2.keys()]):
        count1 = f1.get(fact, 0)
        count2 = f2.get(fact, 0)
        factors[fact] = max(count1, count2)
    return factors


def factor(n):
    factors = {}
    while n > 1:
        for i in range(2, n + 1):
            if n % i == 0:
                if i not in factors:
                    factors[i] = 0
                factors[i] = factors[i] + 1
                n = n // i
                break
    return factors


def product(f):
    p = 1
    for fact, exp in f.items():
        p = p * (fact ** exp)
    return p


def lcm(vals):
    factors = {}
    for val in vals:
        factors = merge_factors(factors, factor(val))
    return product(factors)


def print_part2_ans(input):
    bus_ids = {
        i: int(n) for i, n in enumerate(input[1].rstrip().split(",")) if n != "x"
    }
    first_bus_id = bus_ids.pop(0)
    incrementer = timestamp = first_bus_id
    for offset, bus_id in bus_ids.items():
        while (timestamp + offset) % bus_id != 0:
            timestamp = timestamp + incrementer
        incrementer = lcm([incrementer, bus_id])
    print(timestamp)


print_part2_ans(INPUT)
