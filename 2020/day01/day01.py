INPUT = [int(l.rstrip()) for l in open("day01_input.txt", "r").readlines()]


def pair_with_sum(arr, sum):
    vals = set(arr)
    for val in arr:
        if (sum - val) in vals:
            return (val, sum - val)


def triple_with_sum(arr, sum):
    arr.sort()
    for val_index, val in enumerate(arr):
        i = val_index + 1
        j = len(arr) - 1
        while i < j:
            if arr[i] + arr[j] + val == sum:
                return (val, arr[i], arr[j])
            elif arr[i] + arr[j] + val < sum:
                i += 1
            else:
                j -= 1


def print_part1_ans(input):
    pair = pair_with_sum(input, 2020)
    print(pair[0] * pair[1])


def print_part2_ans(input):
    trip = triple_with_sum(input, 2020)
    print(trip[0] * trip[1] * trip[2])


print_part1_ans(INPUT)
print_part2_ans(INPUT)
