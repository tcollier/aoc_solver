INPUT = [14, 3, 1, 0, 9, 5]


def print_ans(input, n):
    last_usage = {}
    for i in range(len(input) - 1):
        last_usage[input[i]] = i
    prev_num = input[-1]
    for i in range(len(input), n):
        if prev_num not in last_usage:
            curr_num = 0
        else:
            curr_num = i - 1 - last_usage[prev_num]
        last_usage[prev_num] = i - 1
        prev_num = curr_num
    print(curr_num)


print_ans(INPUT, 30000000)
