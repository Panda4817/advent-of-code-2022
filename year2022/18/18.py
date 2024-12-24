from collections import deque


def process_data(data):
    return {tuple([int(i) for i in line.split(",")]) for line in data.split("\n")}


def get_neighbors(x, y, z):
    return {(x + 1, y, z),
            (x - 1, y, z),
            (x, y + 1, z),
            (x, y - 1, z),
            (x, y, z + 1),
            (x, y, z - 1)}


def part1(data):
    coords = process_data(data)
    sides = 0
    for (x, y, z) in coords:
        neighbors = get_neighbors(x, y, z)
        for n in neighbors:
            if not n in coords:
                sides += 1

    return sides


def has_free_sides(n, max_x, min_x, max_y, min_y, max_z, min_z, coords, exposed_sides):
    if n in coords:
        return False

    x, y, z = n
    if x >= max_x or x <= min_x or y >= max_y or y <= min_y or z >= max_z or z <= min_z:
        return True

    blocked_sides = 0
    for a in get_neighbors(x, y, z):

        if a in coords:
            blocked_sides += 1
        elif has_free_sides(a, max_x, min_x, max_y, min_y, max_z, min_z, coords, exposed_sides):
            blocked_sides += 0
        else:
            blocked_sides += 1

    if blocked_sides < 6:
        return True

    return False


def part2(data):
    coords = process_data(data)
    sides = 0
    exposed_sides = []
    for (x, y, z) in coords:
        neighbors = get_neighbors(x, y, z)
        for n in neighbors:
            if not n in coords:
                exposed_sides.append(n)

    max_x = max(x for (x, y, z) in coords)
    max_y = max(y for (x, y, z) in coords)
    max_z = max(z for (x, y, z) in coords)
    min_x = min(x for (x, y, z) in coords)
    min_y = min(y for (x, y, z) in coords)
    min_z = min(z for (x, y, z) in coords)

    done = {}
    reduce_duplicates = set(exposed_sides)
    for (x, y, z) in reduce_duplicates:
        neighbors = get_neighbors(x, y, z)
        q = [n for n in neighbors]
        stack = deque(q)
        blocked = False
        visited = set()
        while stack:
            nx, ny, nz = stack.pop()
            if (nx, ny, nz) in coords:
                blocked += True
                continue

            if nx >= max_x or nx <= min_x or ny >= max_y or ny <= min_y or nz >= max_z or nz <= min_z:
                blocked = False
                break

            visited.add((nx, ny, nz))

            for a in get_neighbors(nx, ny, nz):
                if a in coords:
                    blocked += True
                    continue
                if a not in visited:
                    stack.append(a)

        if not blocked:
            done[(x, y, z)] = 1
        else:
            done[(x, y, z)] = 0

    for n in exposed_sides:
        sides += done[n]

    return sides
