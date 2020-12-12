INPUT = [int(l.rstrip()) for l in open("day10_input.txt", "r").readlines()]


def print_part1_ans(input):
    input.append(0)
    input.append(input[-1] + 3)
    input.sort()
    num_1_diff = num_3_diff = 0
    for i in range(1, len(input)):
        diff = input[i] - input[i - 1]
        if diff == 1:
            num_1_diff = num_1_diff + 1
        elif diff == 3:
            num_3_diff = num_3_diff + 1
    print(num_1_diff * num_3_diff)


print_part1_ans(INPUT)
