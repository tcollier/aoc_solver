INPUT = [l.rstrip() for l in open("day24_input.txt", "r").readlines()]


def initial_flip(input):
    points = set()
    for line in input:
        x, y = 0, 0
        modified_line = (
            line.replace(r"se", "a")
            .replace(r"sw", "b")
            .replace(r"ne", "c")
            .replace(r"nw", "d")
        )
        for c in modified_line:
            if c == "a":
                x += 0.5
                y -= 1
            elif c == "b":
                x -= 0.5
                y -= 1
            elif c == "c":
                x += 0.5
                y += 1
            elif c == "d":
                x -= 0.5
                y += 1
            elif c == "e":
                x += 1
            elif c == "w":
                x -= 1
        if (x, y) not in points:
            points.add((x, y))
        else:
            points.remove((x, y))
    return points


def print_part1_ans(input):
    print(len(initial_flip(input)))


def neighbors(point):
    return [
        (point[0] + 0.5, point[1] - 1),
        (point[0] - 0.5, point[1] - 1),
        (point[0] + 1, point[1]),
        (point[0] + 0.5, point[1] + 1),
        (point[0] - 0.5, point[1] + 1),
        (point[0] - 1, point[1]),
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


print_part2_ans(INPUT)
