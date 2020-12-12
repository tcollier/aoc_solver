INPUT = [int(l.rstrip()) for l in open("day9_input.txt", "r").readlines()]


def print_part1_ans(input, pool_size=25):
    number_pool = {n for n in input[0:pool_size]}
    for i in range(pool_size, len(input)):
        valid = False
        for j in range(pool_size):
            if (input[i] - input[i - pool_size + j]) in number_pool:
                valid = True
                break
        if not valid:
            print(input[i])
            break
        number_pool.remove(input[i - pool_size])
        number_pool.add(input[i])



print_part1_ans(INPUT)
