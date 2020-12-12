INPUT = [int(l.rstrip()) for l in open("day9_input.txt", "r").readlines()]


def first_invalid_number(input, pool_size=25):
    number_pool = {n for n in input[0:pool_size]}
    for i in range(pool_size, len(input)):
        valid = False
        for j in range(pool_size):
            if (input[i] - input[i - pool_size + j]) in number_pool:
                valid = True
                break
        if not valid:
            return i, input[i]
        number_pool.remove(input[i - pool_size])
        number_pool.add(input[i])


def print_part1_ans(input, pool_size=25):
    print(first_invalid_number(input, pool_size)[1])


def print_part2_ans(input, pool_size=25):
    max_index, target_num = first_invalid_number(input, pool_size)
    for i in range(max_index):
        sum = input[i]
        for j in range(i + 1, max_index):
            sum = sum + input[j]
            if sum == target_num:
                elems = input[i:j + 1]
                elems.sort()
                print(elems[0] + elems[-1])
                return
            elif sum > target_num:
                break


print_part2_ans(INPUT)
