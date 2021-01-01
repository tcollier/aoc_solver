from collections import deque

# Mine
INPUT = "198753462"

# Sample
# INPUT = "389125467"


class Cup(object):
    def __init__(self, label):
        self.label = label
        self.next = None


def cups_to_str(head, highlight_head=False, delim=" "):
    curr = head
    cups = []
    while curr:
        if curr == head and highlight_head:
            cups.append(f"({head.label})")
        else:
            cups.append(str(curr.label))
        curr = curr.next
        if curr == head:
            break
    return delim.join(cups)


def generate_circle(labels, num_cups):
    head = None
    tail = None
    indexes = [None] * num_cups
    for label in labels:
        cup = Cup(label)
        indexes[label - 1] = cup
        if not head:
            head = cup
        else:
            tail.next = cup
        tail = cup
    for label in range(len(labels) + 1, num_cups + 1):
        cup = Cup(label)
        indexes[label - 1] = cup
        tail.next = cup
        tail = cup
    tail.next = head
    return head, indexes


def skip_cups(head, num_cups):
    for _ in range(num_cups):
        head = head.next
    return head


def break_circle(head, num_cups):
    for _ in range(num_cups):
        head = head.next
    head.next = None


def insert_pickups(destination, pick_ups):
    curr_pickup = pick_ups
    while curr_pickup.next:
        curr_pickup = curr_pickup.next
    curr_pickup.next = destination.next
    destination.next = pick_ups


def move(head, indexes, num_cups, move_num):
    dest_label = head.label - 1
    pick_ups = head.next
    head.next = skip_cups(head.next, 3)
    break_circle(pick_ups, 2)

    picked = set()
    curr_picked = pick_ups
    while curr_picked:
        picked.add(curr_picked.label)
        curr_picked = curr_picked.next
    if dest_label == 0:
        dest_label = num_cups
    while dest_label in picked:
        dest_label -= 1
        if dest_label == 0:
            dest_label = num_cups

    insert_pickups(indexes[dest_label - 1], pick_ups)


def output_part1(head, _):
    while head.label != 1:
        head = head.next
    print(cups_to_str(head, False, "")[1:])


def output_part2(_, indexes):
    print(indexes[0].next.label * indexes[0].next.next.label)


def print_ans(labels, num_cups, num_moves, output_fn):
    head, indexes = generate_circle(labels, num_cups)
    for move_num in range(num_moves):
        move(head, indexes, num_cups, move_num + 1)
        head = head.next
    output_fn(head, indexes)


labels = [int(c) for c in INPUT]

print_ans(labels, num_cups=9, num_moves=100, output_fn=output_part1)
print_ans(labels, num_cups=1000000, num_moves=10000000, output_fn=output_part2)
