import os
import re

CWD = os.path.dirname(os.path.abspath(__file__))
INPUT = [l.rstrip() for l in open(f"{CWD}/input.txt", "r").readlines()]


def build_regex(rules, rule_num, repeats=0):
    if repeats > 4:
        return ""
    outputs = []
    orred = False
    for input_rule in rules[rule_num]:
        if isinstance(input_rule, int):
            repeats += 1 if input_rule == rule_num else 0
            outputs.append(build_regex(rules, input_rule, repeats))
        elif input_rule == "|":
            orred = True
            outputs.append(input_rule)
        else:
            outputs.append(input_rule)
    if orred:
        return f"({''.join(outputs)})"
    else:
        return f"{''.join(outputs)}"


def print_ans(input, custom_rules={}):
    def parse_rule(r):
        if re.match("^[0-9]+$", r):
            return int(r)
        elif r == "|":
            return r
        else:
            return re.sub(r'"', "", r)

    in_rules = True
    num_valid_strings = 0
    rules = {}
    for line in input:
        if line == "":
            regex = f"^{build_regex(rules, 0)}$"
            in_rules = False
        elif in_rules:
            match = re.match(r"^(\d+): (.+)$", line)
            rule_num = int(match[1])
            rule_str = custom_rules[rule_num] if rule_num in custom_rules else match[2]
            parts = [parse_rule(r) for r in rule_str.split(" ")]
            rules[rule_num] = parts
        elif re.match(regex, line):
            num_valid_strings += 1
    print(num_valid_strings)


print_ans(INPUT)
print_ans(INPUT, {8: "42 | 42 8", 11: "42 31 | 42 11 31"})
