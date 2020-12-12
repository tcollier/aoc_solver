INPUT = [int(l) for l in open("day1_input.txt", "r").readlines()]

def pair_with_sum(arr, sum):
    vals = set()
    for val in arr:
        vals.add(val)
    for val in arr:
        if (sum - val) in vals:
            return (val, sum - val)


def triple_with_sum(arr, sum):
    arr.sort()
    for val_index, val in enumerate(arr):
        diff = sum - val
        i = 0
        j = len(arr) - 1
        while i < j:
            if i == val_index:
                i = i + 1
            elif j == val_index:
                j = j - 1
            elif arr[i] + arr[j] + val == sum:
                return (val, arr[i], arr[j])
            elif arr[i] + arr[j] + val < sum:
                i = i + 1
            else:
                j = j - 1


def print_part1_ans():
    pair = pair_with_sum(INPUT, 2020)
    print("Pair:", pair)
    print("Product:", pair[0] * pair[1])


def print_part2_ans():
    trip = triple_with_sum(INPUT, 2020)
    print("Triplet:", trip)
    print("Product:", trip[0] * trip[1] * trip[2])


print_part2_ans()
