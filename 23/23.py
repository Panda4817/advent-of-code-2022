def process_data(data):
    lines = data.split("\n")
    elves = {}
    x = 0
    y = 0
    id = 1
    for line in lines:
        print(line)
        for char in line:
            if char == "#":
                elves[id] = {"c": (x, y), "n": None}
                id += 1
            x += 1
        y += 1
        x = 0
    return elves


def get_n(x, y):
    return {
        "e": (x + 1, y),
        "w": (x - 1, y),
        "s": (x, y + 1),
        "n": (x, y - 1),
        "nw": (x - 1, y - 1),
        "sw": (x - 1, y + 1),
        "ne": (x + 1, y - 1),
        "se": (x + 1, y + 1)
    }


def round(elves, index):
    cycle = [("n", "ne", "nw"), ("s", "se", "sw"), ("w", "nw", "sw"), ("e", "ne", "se")]
    new_cycle = cycle[index:4] + cycle[0:index]
    s = set([v["c"] for k, v in elves.items()])

    for k, e in elves.items():
        n = get_n(e["c"][0], e["c"][1])
        n_set = set((x, y) for (x, y) in n.values())
        r = s.intersection(n_set)
        if len(r) == 0:
            continue

        for i in range(0, 4):
            if n[new_cycle[i][0]] not in s and n[new_cycle[i][1]] not in s and n[new_cycle[i][2]] not in s:
                elves[k]["n"] = n[new_cycle[i][0]]
                break

    p = [v["n"] for v in elves.values()]
    for k, e, in elves.items():
        if p.count(e["n"]) > 1:
            elves[k]["n"] = None

    new_elves = {}
    moved = False
    for k, v in elves.items():
        if v["n"] != None:
            new_elves[k] = {"c": v["n"], "n": None}
            moved = True
        else:
            new_elves[k] = {"c": v["c"], "n": None}

    index += 1
    if index == 4:
        index = 0
    return new_elves, index, moved


def part1(data):
    elves = process_data(data)
    index = 0
    for i in range(0, 10):
        elves, index, moved = round(elves, index)

    s = {v["c"] for v in elves.values()}
    all_x = [x for (x, y) in s]
    all_y = [y for (x, y) in s]
    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)
    area = ((max_x + 1) - min_x) * ((max_y + 1) - min_y)
    return area - len(elves)


def part2(data):
    elves = process_data(data)
    index = 0
    round_n = 0
    while True:
        round_n += 1
        elves, index, moved = round(elves, index)
        if not moved:
            break

    return round_n
