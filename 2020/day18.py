import re

INPUT = [l.rstrip() for l in open("day18_input.txt", "r").readlines()]

OPERATORS = {
    "+": lambda a, b: a + b,
    "*": lambda a, b: a * b,
}


def part1_eval_line(line):
    chars = []
    for c in line:
        if c in ["(", "+", "*"]:
            chars.append(c)
        elif c == ")":
            val = chars.pop()
            chars.pop()
            if not len(chars) or chars[-1] == "(":
                chars.append(val)
            else:
                operator = chars.pop()
                operand = chars.pop()
                chars.append(OPERATORS[operator](operand, val))
        elif re.match(r"\d", c):
            if not len(chars) or chars[-1] == "(":
                chars.append(int(c))
            else:
                operator = chars.pop()
                operand = chars.pop()
                chars.append(OPERATORS[operator](operand, int(c)))
        elif c == " ":
            continue
    return chars[0]


def print_ans(input, eval_fn):
    total = 0
    for line in input:
        total += eval_fn(line)
    print(total)


print_ans(INPUT, part1_eval_line)
