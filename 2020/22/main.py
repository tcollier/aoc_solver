import math
import os
import re
import sys

from collections import deque
from lib.executor import Executor

CWD = os.path.dirname(os.path.abspath(__file__))


def play_part1(hand1, hand2):
    while hand1 and hand2:
        card1, card2 = (hand1.popleft(), hand2.popleft())
        if card1 > card2:
            hand1.append(card1)
            hand1.append(card2)
        else:
            hand2.append(card2)
            hand2.append(card1)
    return len(hand1) > 0


def play_part2(hand1, hand2):
    seen_hands = set()
    while hand1 and hand2:
        hand_id = ".".join([str(c) for c in hand1 + deque(["x"]) + hand2])
        if hand_id in seen_hands:
            return True
        seen_hands.add(hand_id)
        card1, card2 = (hand1.popleft(), hand2.popleft())
        if len(hand1) >= card1 and len(hand2) >= card2:
            p1_win = play_part2(
                deque([hand1[i] for i in range(card1)]),
                deque([hand2[i] for i in range(card2)]),
            )
        else:
            p1_win = card1 > card2
        if p1_win:
            hand1.append(card1)
            hand1.append(card2)
        else:
            hand2.append(card2)
            hand2.append(card1)
    return len(hand1) > 0


def play(input, play_fn):
    hands = []
    curr_hand = deque()
    for line in input:
        if line == "":
            hands.append(curr_hand)
            curr_hand = deque()
        else:
            match = re.match(r"Player (\d):", line)
            if not match:
                curr_hand.append(int(line))
    hands.append(curr_hand)
    winning_hand = hands[0] if play_fn(hands[0], hands[1]) else hands[1]
    score = 0
    for i in range(len(winning_hand)):
        score += (i + 1) * winning_hand[len(winning_hand) - i - 1]
    return score


def part1_solution(input):
    return play(input, play_part1)


def part2_solution(input):
    return play(input, play_part2)


executor = Executor(
    [l.rstrip() for l in open(f"{CWD}/input.txt", "r").readlines()],
    part1_solution,
    part2_solution,
)
executor(sys.argv)
