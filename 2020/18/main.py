import os
import re

CWD = os.path.dirname(os.path.abspath(__file__))
INPUT = [l.rstrip() for l in open(f"{CWD}/input.txt", "r").readlines()]

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


def eval_without_parens(chars):
    summed = add_without_parens(chars)
    return mult_without_parens(summed)[0]


def add_without_parens(chars):
    new_chars = []
    operator = None
    for c in chars:
        if c == "+":
            operator = c
        elif c == "*":
            new_chars.append(c)
        else:
            if operator:
                new_chars[-1] = OPERATORS[operator](new_chars[-1], c)
                operator = None
            else:
                new_chars.append(c)
    return new_chars


def mult_without_parens(chars):
    new_chars = []
    operator = None
    for c in chars:
        if c == "*":
            operator = c
        else:
            if operator:
                new_chars[-1] = OPERATORS[operator](new_chars[-1], c)
            else:
                new_chars.append(c)
                operator = None
    return new_chars


def part2_eval_line(line):
    chars = []
    for c in line:
        if c in ["(", "+", "*"]:
            chars.append(c)
        elif c == ")":
            within_parens = []
            val = c
            while val != "(":
                val = chars.pop()
                if val != "(":
                    within_parens.append(val)
            chars.append(eval_without_parens(within_parens))
        elif re.match(r"\d", c):
            chars.append(int(c))
        elif c == " ":
            continue
    return eval_without_parens(chars)


def print_ans(input, eval_fn):
    total = 0
    for line in input:
        total += eval_fn(line)
    print(total)


print_ans(INPUT, part1_eval_line)
print_ans(INPUT, part2_eval_line)
