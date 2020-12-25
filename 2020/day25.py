# My input
CARD_PUBLIC_KEY = 15113849
DOOR_PUBLIC_KEY = 4206373

# Sample
# CARD_PUBLIC_KEY = 5764801
# DOOR_PUBLIC_KEY = 17807724

SUBJECT_NUMBER = 7
DIVISOR = 20201227


def loop_size(pubkey):
    loop = 0
    value = 1
    while value != pubkey:
        value *= SUBJECT_NUMBER
        value %= DIVISOR
        loop += 1
    return loop


def encrypt(pubkey, loop_size):
    value = 1
    for _ in range(loop_size):
        value *= pubkey
        value %= DIVISOR
    return value


def print_part1_ans(pubkey1, pubkey2):
    print(encrypt(pubkey2, loop_size(pubkey1)))


print_part1_ans(CARD_PUBLIC_KEY, DOOR_PUBLIC_KEY)
