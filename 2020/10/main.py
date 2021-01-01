import os

CWD = os.path.dirname(os.path.abspath(__file__))
INPUT = [int(l.rstrip()) for l in open(f"{CWD}/input.txt", "r").readlines()]


def print_part1_ans(input):
    input = [n for n in input]
    input.append(0)
    input.sort()
    input.append(input[-1] + 3)
    num_1_diff = num_3_diff = 0
    for i in range(1, len(input)):
        diff = input[i] - input[i - 1]
        if diff == 1:
            num_1_diff += 1
        elif diff == 3:
            num_3_diff += 1
    print(num_1_diff * num_3_diff)


def print_part2_ans(input):
    input = [n for n in input]
    input.append(0)
    input.sort()
    counts = [0 for _ in input]
    counts[0] = counts[1] = 1
    for i in range(2, len(input)):
        for j in range(max(0, i - 3), i):
            if input[i] - input[j] <= 3:
                counts[i] += counts[j]
    print(counts[-1])


print_part1_ans(INPUT)
print_part2_ans(INPUT)
