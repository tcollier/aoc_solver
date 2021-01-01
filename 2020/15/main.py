INPUT = [14, 3, 1, 0, 9, 5]


def print_ans(input, num_rounds):
    last_usage = [-1] * num_rounds
    for i in range(len(input) - 1):
        last_usage[input[i]] = i
    prev_num = input[-1]
    for i in range(len(input), num_rounds):
        if last_usage[prev_num] >= 0:
            curr_num = i - 1 - last_usage[prev_num]
        else:
            curr_num = 0
        last_usage[prev_num] = i - 1
        prev_num = curr_num
    print(curr_num)


print_ans(INPUT, 2020)
print_ans(INPUT, 30000000)
