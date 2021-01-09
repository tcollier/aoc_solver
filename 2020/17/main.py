import os
import sys

from collections import deque
from lib.executor import Executor


CWD = os.path.dirname(os.path.abspath(__file__))


class Board3D:
    def __init__(self, cubes):
        self.cubes = cubes

    @classmethod
    def from_input(cls, input):
        cubes = deque()
        layer = deque()
        for line in input:
            row = deque()
            for cube in line:
                row.append(1 if cube == "#" else 0)
            layer.append(row)
        cubes.append(layer)
        return Board3D(cubes)

    def active_cubes(self):
        count = 0
        for layer in self.cubes:
            for row in layer:
                for cube in row:
                    count += cube
        return count

    def iterate(self):
        def num_neighbors(z, y, x):
            count = 0
            for nz in range(max(0, z - 1), min(z + 2, len(self.cubes))):
                for ny in range(max(0, y - 1), min(y + 2, len(self.cubes[0]))):
                    for nx in range(max(0, x - 1), min(x + 2, len(self.cubes[0][0])),):
                        if z == nz and y == ny and x == nx:
                            continue
                        else:
                            count += self.cubes[nz][ny][nx]
            return count

        new_cubes = deque()
        for z in range(-1, len(self.cubes) + 1):
            new_layer = deque()
            for y in range(-1, len(self.cubes[0]) + 1):
                new_row = deque()
                for x in range(-1, len(self.cubes[0][0]) + 1):
                    cube = 0
                    if (
                        0 <= z < len(self.cubes)
                        and 0 <= y < len(self.cubes[z])
                        and 0 <= x < len(self.cubes[z][y])
                    ):
                        cube = self.cubes[z][y][x]
                    active_neighbors = num_neighbors(z, y, x)
                    if cube == 1 and active_neighbors in [2, 3]:
                        new_row.append(1)
                    elif cube == 0 and active_neighbors == 3:
                        new_row.append(1)
                    else:
                        new_row.append(0)
                new_row.append(0)
                new_layer.append(new_row)
            new_cubes.append(new_layer)
        return Board3D(new_cubes)


class Board4D:
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
        return Board4D(hcubes)

    def active_cubes(self):
        count = 0
        for cubes in self.hcubes:
            for layer in cubes:
                for row in layer:
                    for cube in row:
                        count += cube
        return count

    def iterate(self):
        def num_neighbors(w, z, y, x):
            count = 0
            for nw in range(max(0, w - 1), min(w + 2, len(self.hcubes))):
                for nz in range(max(0, z - 1), min(z + 2, len(self.hcubes[0]))):
                    for ny in range(max(0, y - 1), min(y + 2, len(self.hcubes[0][0]))):
                        for nx in range(
                            max(0, x - 1), min(x + 2, len(self.hcubes[0][0][0])),
                        ):
                            if w == nw and z == nz and y == ny and x == nx:
                                continue
                            else:
                                count += self.hcubes[nw][nz][ny][nx]
            return count

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
                        active_neighbors = num_neighbors(w, z, y, x)
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
        return Board4D(new_hcubes)


def part1_solution(input):
    board = Board3D.from_input(input)
    for _ in range(6):
        board = board.iterate()
    return board.active_cubes()


def part2_solution(input):
    board = Board4D.from_input(input)
    for _ in range(6):
        board = board.iterate()
    return board.active_cubes()


executor = Executor(
    [l.rstrip() for l in open(f"{CWD}/input.txt", "r").readlines()],
    part1_solution,
    part2_solution,
)
executor(sys.argv)
