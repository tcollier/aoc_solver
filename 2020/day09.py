INPUT = [int(l.rstrip()) for l in open("day09_input.txt", "r").readlines()]

POOL_SIZE = 25


def first_invalid_number(input):
    number_pool = set(input[0:POOL_SIZE])
    for i in range(POOL_SIZE, len(input)):
        valid = False
        for j in range(POOL_SIZE):
            if (input[i] - input[i - POOL_SIZE + j]) in number_pool:
                valid = True
                break
        if not valid:
            return i, input[i]
        number_pool.remove(input[i - POOL_SIZE])
        number_pool.add(input[i])


def print_part1_ans(input,):
    print(first_invalid_number(input)[1])


def print_part2_ans(input):
    max_index, target_num = first_invalid_number(input)
    for i in range(max_index):
        sum = input[i]
        for j in range(i + 1, max_index):
            sum += input[j]
            if sum == target_num:
                elems = input[i : j + 1]
                elems.sort()
                print(elems[0] + elems[-1])
                return
            elif sum > target_num:
                break


print_part2_ans(INPUT)
