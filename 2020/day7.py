INPUT = open("day7_input.txt", "r").readlines()

import re


def parse_rule(line):
    match = re.match("(.+) bags contain (.+)\.", line)
    container = match[1]
    contents = {}
    if match[2] != "no other bags":
        for part in match[2].split(", "):
            match = re.match("(\d+) (.+) bags?", part)
            contents[match[2]] = int(match[1])
    return container, contents


def print_part1_ans(input):
    bags = {}
    for line in input:
        container, contents = parse_rule(line.rstrip())
        if container not in bags:
            bags[container] = set()
        for contained in contents:
            if contained not in bags:
                bags[contained] = set()
            bags[contained].add(container)
    options = set()
    bags_to_try = [b for b in bags["shiny gold"]]
    while bags_to_try:
        bag = bags_to_try.pop()
        options.add(bag)
        for next_bag in bags[bag]:
            if next_bag not in options:
                bags_to_try.append(next_bag)
    print(len(options))


print_part1_ans(INPUT)
