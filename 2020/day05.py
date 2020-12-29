INPUT = [l.rstrip() for l in open("day05_input.txt", "r").readlines()]


def string_to_id(str):
    id = 0
    for char in str:
        id <<= 1
        if char in ["B", "R"]:
            id += 1
    return id


def print_part1_ans(input):
    max_id = 0
    for line in input:
        id = string_to_id(line)
        if id > max_id:
            max_id = id
    print(max_id)


def print_part2_ans(input):
    ids = {string_to_id(l) for l in input}
    for id in ids:
        if id + 1 not in ids and id + 2 in ids:
            print(id + 1)


print_part2_ans(INPUT)
