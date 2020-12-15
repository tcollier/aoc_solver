INPUT = [14, 3, 1, 0, 9, 5]


def print_ans(input, n):
    prev_last_usage = {}
    last_usage = {}
    for i, curr_num in enumerate(input):
        last_usage[curr_num] = i
    for i in range(len(input), n):
        if curr_num not in prev_last_usage:
            curr_num = 0
        else:
            curr_num = last_usage[curr_num] - prev_last_usage[curr_num]
        if curr_num in last_usage:
            prev_last_usage[curr_num] = last_usage[curr_num]
        last_usage[curr_num] = i
    print(curr_num)


print_ans(INPUT, 30000000)
