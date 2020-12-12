INPUT = open("day6_input.txt", "r").readlines()


def print_part1_ans(input):
    group_answers = set()
    total_answered = 0
    for line in input:
        if line == "\n":
            total_answered = total_answered + len(group_answers)
            group_answers = set()
            continue
        for question in line.rstrip():
            group_answers.add(question)

    print(total_answered + len(group_answers))


print_part1_ans(INPUT)
