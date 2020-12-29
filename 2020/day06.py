INPUT = [l.rstrip() for l in open("day06_input.txt", "r").readlines()]


def print_part1_ans(input):
    group_answers = set()
    total_answered = 0
    for line in input:
        if line == "":
            total_answered += len(group_answers)
            group_answers = set()
            continue
        for question in line:
            group_answers.add(question)

    print(total_answered + len(group_answers))


def print_part2_ans(input):
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

    print(total_answered + len(group_answers))


print_part2_ans(INPUT)
