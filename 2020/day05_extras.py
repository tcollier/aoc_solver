import random
import re
import timeit


def tcollier_solution(bp):
    id = 0
    for char in bp:
        id <<= 1
        if char in ["B", "R"]:
            id += 1
    return id


def angelman_solution(bp):
    return int(re.sub(r"[FL]", "0", re.sub(r"[BR]", "1", bp)), 2)


CHAR_MAP = {
    "F": 0,
    "B": 1,
    "R": 1,
    "L": 0,
}


def jasonzhao6_solution(bp):
    return int("".join([str(CHAR_MAP[c]) for c in bp]), 2)


# Benchmarking code
def random_bp():
    seat_id = random.randint(0, 2 ** 10 - 1)
    mask = 2 ** 9
    bp = ""
    while mask > 0:
        if mask > 2 ** 3:
            next_ch = "B" if mask & seat_id else "F"
        else:
            next_ch = "R" if mask & seat_id else "L"
        bp += next_ch
        mask >>= 1
    return bp


def parse_bps(fn, bps):
    for bp in bps:
        fn(bp)


def time_parsing(fn, bps):
    print(
        fn,
        timeit.timeit(
            "parse_bps(fn, bps)",
            globals=locals(),
            number=100,
            setup="from __main__ import parse_bps",
        ),
    )


if __name__ == "__main__":
    bps = [random_bp() for _ in range(100000)]
    time_parsing(tcollier_solution, bps)
    time_parsing(angelman_solution, bps)
    time_parsing(jasonzhao6_solution, bps)
