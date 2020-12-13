import re

INPUT = open("day04_input.txt", "r").readlines()

REQUIRED_FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]


def year_between(val, min, max):
    if re.match(r"^\d{4}$", val):
        int_val = int(val)
        return min <= int_val <= max
    else:
        return False


def valid_height(val):
    match = re.match(r"^(\d+)(in|cm)$", val)
    if match and match[2] == "cm":
        int_val = int(match[1])
        return 150 <= int_val <= 193
    elif match and match[2] == "in":
        int_val = int(match[1])
        return 59 <= int_val <= 76
    else:
        return False


VALID_EYE_COLORS = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
PART2_VALIDATION = {
    "byr": lambda val: year_between(val, 1920, 2002),
    "iyr": lambda val: year_between(val, 2010, 2020),
    "eyr": lambda val: year_between(val, 2020, 2030),
    "hgt": valid_height,
    "hcl": lambda val: re.match(r"^#[\da-f]{6}$", val) is not None,
    "ecl": lambda val: val in VALID_EYE_COLORS,
    "pid": lambda val: re.match(r"^\d{9}$", val) is not None,
}


def part1_validation(field, val):
    return True


def part2_validation(field, val):
    return PART2_VALIDATION[field](val)


def print_ans(input, validation_fn):
    needed_fields = {f for f in REQUIRED_FIELDS}
    num_valid = 0
    for line in input:
        if line == "\n":
            if not needed_fields:
                num_valid += 1
            needed_fields = {f for f in REQUIRED_FIELDS}
            continue
        parts = line.rstrip().split(" ")
        for part in parts:
            field, val = part.split(":")
            if field != "cid" and validation_fn(field, val):
                needed_fields.remove(field)
    if not needed_fields:
        num_valid += 1
    print(num_valid)


print_ans(INPUT, part2_validation)
