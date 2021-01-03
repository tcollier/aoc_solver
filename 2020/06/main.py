import os
import sys

from lib.executor import Executor


CWD = os.path.dirname(os.path.abspath(__file__))


def part1_solution(input):
    group_answers = set()
    total_answered = 0
    for line in input:
        if line == "":
            total_answered += len(group_answers)
            group_answers = set()
            continue
        for question in line:
            group_answers.add(question)

    return total_answered + len(group_answers)


def part2_solution(input):
    total_answered = 0
    first_person = True
    for line in input:
        if line == "":
            total_answered += len(group_answers)
            first_person = True
            continue
        person_answers = set(line)
        if first_person:
            group_answers = person_answers
            first_person = False
        else:
            group_answers = group_answers.intersection(person_answers)

    return total_answered + len(group_answers)


executor = Executor(
    [l.rstrip() for l in open(f"{CWD}/input.txt", "r").readlines()],
    part1_solution,
    part2_solution,
)
executor(sys.argv)
