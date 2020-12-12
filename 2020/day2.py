INPUT = open("day2_input.txt", "r").readlines()

def valid_part1(rule, pwd):
    range, char = rule.split(" ")
    min, max = [int(n) for n in range.split("-")]
    num_char = 0
    for c in pwd:
        if c == char:
            num_char = num_char + 1
            if num_char > max:
                return False
    if num_char >= min:
        return True


def valid_part2(rule, pwd):
    positiions, char = rule.split(" ")
    first, second = [int(n) for n in positiions.split("-")]
    char_in_first = pwd[first - 1] == char
    char_in_second = pwd[second - 1] == char
    return char_in_first != char_in_second


def print_ans(input, valid_fn):
    num_correct = 0
    for line in input:
        rule, pwd = line.split(": ")
        if valid_fn(rule, pwd):
            num_correct += 1
    print(num_correct)


print_ans(INPUT, valid_part2)
