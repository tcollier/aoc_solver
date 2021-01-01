from collections import deque

# Mine
INPUT = "198753462"

# Sample
# INPUT = "389125467"


def generate_circle(labels, num_cups):
    indexes = [l - 1 for l in labels]
    cups = [None] * num_cups
    if num_cups > len(labels):
        head = num_cups - 1
    else:
        head = indexes[-1]
    curr = head
    for index in indexes:
        cups[curr] = index
        curr = index
    for index in range(len(indexes), num_cups):
        cups[curr] = index
        curr = index
    return cups, head


def move(cups, head, move_num):
    cup1 = cups[head]
    cup2 = cups[cup1]
    cup3 = cups[cup2]
    cup4 = cups[cup3]
    pickups = set([cup2, cup3, cup4])
    cups[cup1] = cups[cup4]

    dest = cups[head] - 1
    if dest < 0:
        dest = len(cups) - 1
    while dest in pickups:
        dest -= 1
        if dest < 0:
            dest = len(cups) - 1

    tmp = cups[dest]
    cups[dest] = cup2
    cups[cup2] = cup3
    cups[cup3] = cup4
    cups[cup4] = tmp

    if dest == head:
        head = cup4
    return head


def output_part1(cups, _):
    labels = []
    curr = cups[0]
    while curr != 0:
        labels.append(str(curr + 1))
        curr = cups[curr]
    print("".join(labels))


def output_part2(cups, head):
    print((cups[0] + 1) * (cups[cups[0]] + 1))


def print_ans(labels, num_cups, num_moves, output_fn):
    cups, head = generate_circle(labels, num_cups)
    for move_num in range(num_moves):
        head = move(cups, head, move_num + 1)
        head = cups[head]
    output_fn(cups, head)


labels = [int(c) for c in INPUT]

print_ans(labels, num_cups=9, num_moves=100, output_fn=output_part1)
print_ans(labels, num_cups=1000000, num_moves=10000000, output_fn=output_part2)
