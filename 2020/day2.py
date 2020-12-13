import re

INPUT = open("day2_input.txt", "r").readlines()


def valid_part1(min, max, char, pwd):
    num_char = 0
    for c in pwd:
        if c == char:
            num_char = num_char + 1
            if num_char > max:
                return False
    if num_char >= min:
        return True


def valid_part2(pos1, pos2, char, pwd):
    return (pwd[pos1 - 1] == char) != (pwd[pos2 - 1] == char)


def print_ans(input, valid_fn):
    num_correct = 0
    for line in input:
        match = re.match(r"^(\d+)-(\d+) (\w): (\w+)$", line.rstrip())
        if valid_fn(int(match[1]), int(match[2]), match[3], match[4]):
            num_correct += 1
    print(num_correct)


print_ans(INPUT, valid_part2)
