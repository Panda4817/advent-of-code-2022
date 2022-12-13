import math
import heapq


class Area:
    def __init__(self, height, r, c, start=False, end=False):
        self.height = height
        self.row = r
        self.col = c
        self.start = start
        self.end = end

    def __str__(self):
        return f"h={self.height}"


def process_data(data):
    grid = [[area for area in line] for line in data.split("\n")]
    area_grid = []
    start = None
    end = None
    possible_starts = []
    for r in range(0, len(grid)):
        row = []
        for c in range(0, len(grid[r])):
            letter = grid[r][c]
            if letter == "S":
                row.append(Area(ord("a"), r, c, start=True))
                start = (0, (r, c, 0))
                possible_starts.append(start)
                continue

            if letter == "E":
                row.append(Area(ord("z"), r, c, end=True))
                end = (r, c)
                continue

            if letter == "a":
                row.append(Area(ord("a"), r, c, start=True))
                s = (0, (r, c, 0))
                possible_starts.append(s)
                continue

            row.append(Area(ord(letter), r, c))
        area_grid.append(row)

    return area_grid, start, end, possible_starts


def get_neighbors(grid, r, c):
    total_rows = len(grid)
    total_cols = len(grid[0])
    up_level = grid[r][c].height + 1
    same = grid[r][c].height
    n = []
    up = (r - 1, c)
    if up[0] >= 0 and (grid[up[0]][c].height == up_level
                       or grid[up[0]][c].height <= same):
        n.append([up, math.dist(up, (r, c))])

    down = (r + 1, c)
    if down[0] < total_rows and (grid[down[0]][c].height == up_level
                                 or grid[down[0]][c].height <= same):
        n.append([down, math.dist(down, (r, c))])

    left = (r, c - 1)
    if left[1] >= 0 and (grid[r][left[1]].height == up_level
                         or grid[r][left[1]].height <= same):
        n.append([left, math.dist(left, (r, c))])

    right = (r, c + 1)
    if right[1] < total_cols and (grid[r][right[1]].height == up_level
                                  or grid[r][right[1]].height <= same):
        n.append([right, math.dist(right, (r, c))])

    return n


def get_steps(grid, start, end):
    q = [start]
    heapq.heapify(q)
    steps = len(grid) * len(grid[0])
    visited = set()
    while q:
        p, (r, c, s) = heapq.heappop(q)
        if (r, c) == end and s < steps:
            steps = s
            continue

        if s > steps:
            continue

        new_steps = s + 1
        neighbors = get_neighbors(grid, r, c)
        for n in neighbors:
            coord = (n[0][0], n[0][1])
            if coord in visited:
                continue
            visited.add(coord)
            el = (new_steps * n[1], (coord[0], coord[1], new_steps))
            heapq.heappush(q, el)

    return steps


def part1(data):
    grid, start, end, possible_starts = process_data(data)
    return get_steps(grid, start, end)


def part2(data):
    grid, start, end, possible_starts = process_data(data)
    steps = []
    for s in possible_starts:
        least_steps = get_steps(grid, s, end)
        steps.append(least_steps)

    return min(steps)
