from collections import deque

INPUT = [l.rstrip() for l in open("day17_input.txt", "r").readlines()]


class Board(object):
    def __init__(self, hcubes):
        self.hcubes = hcubes

    @classmethod
    def from_input(cls, input):
        hcubes = deque()
        cubes = deque()
        layer = deque()
        for line in input:
            row = deque()
            for cube in line:
                row.append(1 if cube == "#" else 0)
            layer.append(row)
        cubes.append(layer)
        hcubes.append(cubes)
        return Board(hcubes)

    def active_cubes(self):
        count = 0
        for cubes in self.hcubes:
            for layer in cubes:
                for row in layer:
                    for cube in row:
                        count += cube
        return count

    def iterate(self):
        new_hcubes = deque()
        for w in range(-1, len(self.hcubes) + 1):
            new_cubes = deque()
            for z in range(-1, len(self.hcubes[0]) + 1):
                new_layer = deque()
                for y in range(-1, len(self.hcubes[0][0]) + 1):
                    new_row = deque()
                    for x in range(-1, len(self.hcubes[0][0][0]) + 1):
                        cube = 0
                        if (
                            0 <= w < len(self.hcubes)
                            and 0 <= z < len(self.hcubes[w])
                            and 0 <= y < len(self.hcubes[w][z])
                            and 0 <= x < len(self.hcubes[w][z][y])
                        ):
                            cube = self.hcubes[w][z][y][x]
                        active_neighbors = 0
                        for nw in range(max(0, w - 1), min(w + 2, len(self.hcubes))):
                            for nz in range(
                                max(0, z - 1), min(z + 2, len(self.hcubes[0]))
                            ):
                                for ny in range(
                                    max(0, y - 1), min(y + 2, len(self.hcubes[0][0]))
                                ):
                                    for nx in range(
                                        max(0, x - 1),
                                        min(x + 2, len(self.hcubes[0][0][0])),
                                    ):
                                        if w == nw and z == nz and y == ny and x == nx:
                                            continue
                                        else:
                                            active_neighbors += self.hcubes[nw][nz][ny][
                                                nx
                                            ]
                        if cube == 1 and active_neighbors in [2, 3]:
                            new_row.append(1)
                        elif cube == 0 and active_neighbors == 3:
                            new_row.append(1)
                        else:
                            new_row.append(0)
                    new_row.append(0)
                    new_layer.append(new_row)
                new_cubes.append(new_layer)
            new_hcubes.append(new_cubes)
        return Board(new_hcubes)


def print_part1_ans(input):
    board = Board.from_input(input)
    for _ in range(6):
        board = board.iterate()
    print(board.active_cubes())


print_part1_ans(INPUT)
