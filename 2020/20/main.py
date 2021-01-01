import math
import os
import re

CWD = os.path.dirname(os.path.abspath(__file__))
INPUT = [l.rstrip() for l in open(f"{CWD}/input.txt", "r").readlines()]


def rotate_matrix(matrix):
    return list(zip(*matrix[::-1]))


def flip_matrix(matrix):
    return [row[::-1] for row in matrix]


class Tile(object):
    def __init__(self, tile_num, pixels, flipped):
        self.tile_num = tile_num
        self.pixels = [[p for p in row] for row in pixels]
        self._lonely_edges = set()
        if flipped:
            self.pixels = flip_matrix(self.pixels)

    def rotate(self):
        self.pixels = rotate_matrix(self.pixels)

    def add_lonley_edge(self, edge_val):
        self._lonely_edges.add(edge_val)

    def lonely_edge_count(self):
        return len(self._lonely_edges)

    def top(self):
        return "".join(self.pixels[0])

    def right(self):
        return "".join([row[-1] for row in self.pixels])

    def bottom(self, rotate=False):
        step = -1 if rotate else 1
        return "".join(self.pixels[-1][::step])

    def left(self, rotate=False):
        step = -1 if rotate else 1
        return "".join([row[0] for row in self.pixels[::step]])

    def lonely_top(self):
        return self.top() in self._lonely_edges

    def lonely_left(self):
        return self.left(True) in self._lonely_edges


def parse_tiles(input):
    tiles = []
    curr_tile_num = None
    pixels = []
    for line in input:
        if line == "":
            tiles.append(Tile(curr_tile_num, pixels, False))
            tiles.append(Tile(curr_tile_num, pixels, True))
            pixels = []
        else:
            match = re.match(r"Tile (\d+):", line)
            if match:
                curr_tile_num = int(match[1])
            else:
                pixels.append([c for c in line])
    tiles.append(Tile(curr_tile_num, pixels, False))
    tiles.append(Tile(curr_tile_num, pixels, True))
    set_lonely_edges(tiles)
    return tiles


def set_lonely_edges(tiles):
    edges = {}
    for tile in tiles:
        for val in [tile.top(), tile.right(), tile.bottom(True), tile.left(True)]:
            if val not in edges:
                edges[val] = []
            edges[val].append(tile)
    for val, edge_tiles in edges.items():
        if len(edge_tiles) == 1:
            edge_tiles[0].add_lonley_edge(val)


def group_pieces(tiles):
    grouped = {"corners": {}, "edges": {}, "inner": {}}
    for tile in tiles:
        if tile.lonely_edge_count() == 2:
            group = "corners"
        elif tile.lonely_edge_count() == 1:
            group = "edges"
        else:
            group = "inner"
        if tile.tile_num not in grouped[group]:
            grouped[group][tile.tile_num] = []
        grouped[group][tile.tile_num].append(tile)
    return grouped


def print_part1_ans(input):
    tiles = parse_tiles(input)
    grouped = group_pieces(tiles)
    product = 1
    for tile_num in grouped["corners"].keys():
        product *= tile_num
    print(product)


def join_puzzle(puzzle):
    joined = []
    for row in puzzle:
        for tile_row in range(1, 9):
            tr = []
            for tile in row:
                if not tile:
                    continue
                tr += tile.pixels[tile_row][1:9]
            joined.append("".join(tr))
    return joined


def apply_piece(puzzle, pieces, used, row, col):
    found = False
    for tile_num, tile_pieces in pieces.items():
        if tile_num in used:
            continue
        for piece in tile_pieces:
            for _ in range(4):
                if row == 0 and not piece.lonely_top():
                    piece.rotate()
                elif row > 0 and piece.top() != puzzle[row - 1][col].bottom():
                    piece.rotate()
                elif col == 0 and not piece.lonely_left():
                    piece.rotate()
                elif col > 0 and piece.left() != puzzle[row][col - 1].right():
                    piece.rotate()
                else:
                    puzzle[row][col] = piece
                    used.add(tile_num)
                    found = True
                    break
            if found:
                break
        if found:
            break


MONSTER = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
]


def assemble_puzzle(pieces, side_length):
    used = set()
    puzzle = [[None for _ in range(side_length)] for _ in range(side_length)]

    apply_piece(puzzle, pieces["corners"], used, 0, 0)
    for col in range(1, side_length - 1):
        apply_piece(puzzle, pieces["edges"], used, 0, col)
    apply_piece(puzzle, pieces["corners"], used, 0, side_length - 1)

    for row in range(1, side_length - 1):
        apply_piece(puzzle, pieces["edges"], used, row, 0)
        for col in range(1, side_length - 1):
            apply_piece(puzzle, pieces["inner"], used, row, col)
        apply_piece(puzzle, pieces["edges"], used, row, side_length - 1)

    apply_piece(puzzle, pieces["corners"], used, side_length - 1, 0)
    for col in range(1, 11):
        apply_piece(puzzle, pieces["edges"], used, side_length - 1, col)
    apply_piece(puzzle, pieces["corners"], used, side_length - 1, side_length - 1)
    return puzzle


def count_monsters(image, monster):
    monsters = 0
    for start_row in range(len(image) - len(monster) + 1):
        for start_col in range(len(image[0]) - len(monster[0]) + 1):
            found = True
            for row_offset in range(len(monster)):
                for col_offset in range(len(monster[0])):
                    monster_pixel = monster[row_offset][col_offset]
                    image_pixel = image[start_row + row_offset][start_col + col_offset]
                    if monster_pixel == "#" and image_pixel != "#":
                        found = False
                        break
                if not found:
                    break
            if found:
                monsters += 1
    return monsters


def count_hashes(image):
    hashes = 0
    for row in image:
        for c in row:
            if c == "#":
                hashes += 1
    return hashes


def all_rotations(orig):
    images = []
    flipped = flip_matrix(orig)
    for _ in range(4):
        images.append(orig)
        images.append(flipped)
        orig = rotate_matrix(orig)
        flipped = rotate_matrix(flipped)
    return images


def print_part2_ans(input):
    tiles = parse_tiles(input)
    pieces = group_pieces(tiles)
    puzzle = assemble_puzzle(pieces, int(math.sqrt(len(tiles) / 2)))
    image = join_puzzle(puzzle)
    monsters = all_rotations(MONSTER)
    monster_count = 0
    for monster in monsters:
        monster_count = count_monsters(image, monster)
        if monster_count > 0:
            break
    print(count_hashes(image) - monster_count * count_hashes(MONSTER))


print_part1_ans(INPUT)
print_part2_ans(INPUT)
