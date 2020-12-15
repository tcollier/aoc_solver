INPUT = [14, 3, 1, 0, 9, 5]


def write_val(val, i, prev_last_usage, last_usage):
    if val in last_usage:
        prev_last_usage[val] = last_usage[val]
    last_usage[val] = i + 1


def print_ans(input, n):
    curr_num = None
    prev_last_usage = {}
    last_usage = {}
    for i in range(n):
        if i < len(input):
            curr_num = input[i]
            write_val(curr_num, i, prev_last_usage, last_usage)
        else:
            last_val = curr_num
            if last_val not in prev_last_usage:
                curr_num = 0
            else:
                curr_num = last_usage[curr_num] - prev_last_usage[curr_num]
            write_val(curr_num, i, prev_last_usage, last_usage)
        print(curr_num)


print_ans(INPUT, 30000000)
