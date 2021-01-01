import os

CWD = os.path.dirname(os.path.abspath(__file__))
INPUT = [l.rstrip() for l in open(f"{CWD}/input.txt", "r").readlines()]

SE = 1 - 1j
SW = -1 - 1j
NE = 1 + 1j
NW = -1 + 1j
E = 2
W = -2


def initial_flip(input):
    tiles = set()
    for line in input:
        modified_line = (
            line.replace(r"se", f"{SE} + ")
            .replace(r"sw", f"{SW} + ")
            .replace(r"ne", f"{NE} + ")
            .replace(r"nw", f"{NW} + ")
            .replace(r"e", f"{E} + ")
            .replace(r"w", f"{W} + ")
        )
        tile = eval(modified_line + "0")
        if tile in tiles:
            tiles.remove(tile)
        else:
            tiles.add(tile)
    return tiles


def print_part1_ans(input):
    print(len(initial_flip(input)))


def neighbors(tile):
    return [
        tile + SE,
        tile + SW,
        tile + NE,
        tile + NW,
        tile + E,
        tile + W,
    ]


def tick(tiles):
    next_tiles = set()
    for tile in tiles:
        num_neighbors = 0
        for neighbor in neighbors(tile):
            if neighbor in tiles:
                num_neighbors += 1
            else:
                grand_num_neighbors = 0
                for grand_neighbor in neighbors(neighbor):
                    if grand_neighbor in tiles:
                        grand_num_neighbors += 1
                if grand_num_neighbors == 2:
                    next_tiles.add(neighbor)
        if 0 < num_neighbors <= 2:
            next_tiles.add(tile)
    return next_tiles


def print_part2_ans(input):
    tiles = initial_flip(input)
    for _ in range(100):
        tiles = tick(tiles)
    print(len(tiles))


print_part1_ans(INPUT)
print_part2_ans(INPUT)
