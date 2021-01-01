import math
import time

import day24

RIGHT_HALF = " █"
FULL = "██"
LEFT_HALF = "█ "
EMPTY = "  "


def draw_tiles(tiles, min_real, min_img, max_real, max_img):
    lines = []
    for img in range(min_img, max_img):
        offset = img & 1
        line = "" * offset
        for real in range(min_real + offset, max_real, 2):
            is_black = real + img * 1j in tiles
            if offset == 1:
                prev_is_black = real - 2 + img * 1j in tiles
                if prev_is_black and is_black:
                    line += FULL
                elif prev_is_black:
                    line += LEFT_HALF
                elif is_black:
                    line += RIGHT_HALF
                else:
                    line += EMPTY
            else:
                if is_black:
                    line += FULL
                else:
                    line += EMPTY
        lines.append(line)
    print("\033c")
    print()
    print()
    print()
    print()
    print("\n".join(lines))
    print()
    print()
    print()
    print()


def animate():
    min_real = -140
    min_img = -70
    max_real = 140
    max_img = 70
    tiles = day24.initial_flip(input)
    draw_tiles(tiles, min_real, min_img, max_real, max_img)
    for _ in range(100):
        time.sleep(0.03)
        tiles = day24.tick(tiles)
        draw_tiles(tiles, min_real, min_img, max_real, max_img)


ALL_DIRECTIONS = [day24.SE, day24.SW, day24.NE, day24.NW, day24.E, day24.W]


def expand_hex(num_steps, tile=0):
    yield tile
    if num_steps == 0:
        return
    if tile.imag == tile.real:
        if tile.imag >= 0:
            for t in expand_hex(num_steps - 1, tile + day24.NE):
                yield t
        if tile.imag <= 0:
            for t in expand_hex(num_steps - 1, tile + day24.SW):
                yield t
    if tile.imag >= abs(tile.real):
        for t in expand_hex(num_steps - 1, tile + day24.NW):
            yield t
    if tile.imag <= -abs(tile.real):
        for t in expand_hex(num_steps - 1, tile + day24.SE):
            yield t
    if tile.real >= abs(tile.imag):
        for t in expand_hex(num_steps - 1, tile + day24.E):
            yield t
    if tile.real <= -abs(tile.imag):
        for t in expand_hex(num_steps - 1, tile + day24.W):
            yield t


NUM_STEPS = 2
POSSILBE_TILES = [t for t in expand_hex(NUM_STEPS)]
POSSILBE_TILES_PLUS_NEIGBORS = [t for t in expand_hex(NUM_STEPS + 1)]


def count_black_tiles(tiles, num_steps):
    tile_count = 0
    for tile in expand_hex(num_steps):
        if tile in tiles:
            tile_count += 1
    return tile_count


def tile_configurations(all_tiles):
    for i in range(2 ** len(all_tiles)):
        tiles = set()
        index = 0
        while i > 0:
            if i & 1 == 1:
                tiles.add(all_tiles[index])
            index += 1
            i >>= 1
        yield tiles


def find_prev_to_all_black(num_steps):
    min_real = -2 * NUM_STEPS - 4
    min_img = -NUM_STEPS - 2
    max_real = 2 * NUM_STEPS + 4
    max_img = NUM_STEPS + 2
    found = False
    for i, prev_tiles in enumerate(tile_configurations(POSSILBE_TILES_PLUS_NEIGBORS)):
        tiles = day24.tick(prev_tiles)
        if count_black_tiles(tiles, NUM_STEPS) == len(POSSILBE_TILES):
            draw_tiles(prev_tiles, min_real, min_img, max_real, max_img)
            time.sleep(5)
            draw_tiles(tiles, min_real, min_img, max_real, max_img)
            time.sleep(5)
            found = True
    if not found:
        print("No configuration found that will tick to all black")


find_prev_to_all_black(1)
