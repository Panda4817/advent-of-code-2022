import copy
import heapq


def process_data(data):
    lines = data.split("\n")
    x = 0
    y = 0
    walls = set()
    b = {}
    b_id = 1
    start = None
    end = None
    total_rows = len(lines)
    total_cols = len(lines[0])
    for line in lines:
        # print(line)
        for char in line:
            if char == "#":
                walls.add((x, y))

            elif y == 0 and char == ".":
                start = (x, y)

            elif y == (total_rows - 1) and char == ".":
                end = (x, y)

            elif char == ">":
                b[b_id] = {"pos": (x, y), "move": (1, 0)}
                b_id += 1

            elif char == "<":
                b[b_id] = {"pos": (x, y), "move": (-1, 0)}
                b_id += 1

            elif char == "^":
                b[b_id] = {"pos": (x, y), "move": (0, -1)}
                b_id += 1

            elif char == "v":
                b[b_id] = {"pos": (x, y), "move": (0, 1)}
                b_id += 1

            x += 1

        y += 1
        x = 0

    return start, b, 0, end, walls, total_rows, total_cols


def heuristic(current, end):
    mh = abs(end[0] - current[0]) + abs(end[1]-current[1])
    return mh


def f_star(h, s):
    return h + s


def get_visited_key(pos, blizzards):
    return f"state[current={pos}, blizzards={blizzards}]"


def move_blizzards(b, total_rows, total_cols):
    new_b = {}
    for k, v in b.items():
        (x, y) = (v["pos"][0] + v["move"][0], v["pos"][1] + v["move"][1])
        if x == 0:
            x = total_cols - 2

        elif x == total_cols - 1:
            x = 1

        elif y == 0:
            y = total_rows - 2

        elif y == total_rows - 1:
            y = 1

        new_b[k] = {"pos": (x, y), "move": v["move"]}

    return new_b


def get_new_pos(x, y):
    return {
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
        (x, y)
    }


def print_state(pos, b, walls, total_rows, total_cols):
    s = []
    winds = {}
    for k, v in b.items():
        curr = winds.get(v['pos'], {'move': v['move'], "count": 0})
        curr["count"] += 1
        winds[v['pos']] = curr

    for y in range(0, total_rows):
        for x in range(0, total_cols):
            p = (x, y)

            if p in walls:
                s.append("#")
            elif p in winds:
                v = winds[p]
                if v["count"] > 1:
                    s.append(str(v["count"]))
                else:
                    dir = v['move']
                    if dir == (1, 0):
                        s.append('>')
                    if dir == (-1, 0):
                        s.append('<')
                    if dir == (0, -1):
                        s.append('^')
                    if dir == (0, 1):
                        s.append('v')
            elif p == pos:
                s.append("E")
            else:
                s.append(".")
        s.append("\n")
    return "".join(s)


def make_key(x, y, steps, total_rows, total_cols):
    lcm = (total_rows-2) * (total_cols-2)
    return (x, y, steps % lcm)


def traverse(start, end, bb, total_rows, total_cols, walls):
    h = heuristic(start, end)
    start_steps = 0
    f = f_star(h, start_steps)
    el = (start, start_steps, copy.deepcopy(bb))
    q = [(f, el)]
    heapq.heapify(q)
    key = make_key(start[0], start[1], start_steps, total_rows, total_cols)
    visited = {key: start_steps}
    while q:
        old_f, (current, steps, b) = heapq.heappop(q)
        if current == end:
            return steps, b

        new_steps = steps + 1
        new_b = move_blizzards(b, total_rows, total_cols)
        b_pos_set = set([new_b[k]["pos"] for k in new_b])
        new_pos = get_new_pos(current[0], current[1])

        for pos in new_pos:
            if pos in walls or pos in b_pos_set:
                continue

            if pos[0] < 0 or pos[0] >= total_cols:
                continue

            if pos[1] < 0 or pos[1] >= total_rows:
                continue

            new_state = (pos, new_steps, new_b)
            new_h = heuristic(pos, end)
            new_f = f_star(new_h, new_steps)
            new_k = make_key(pos[0], pos[1], new_steps, total_rows, total_cols)
            if new_k not in visited or visited[new_k] > new_steps:
                heapq.heappush(q, (new_f, new_state))
                visited[new_k] = new_steps


# Prints both part1 and part2 answers
def part1(data):
    start, bb, start_steps, end, walls, total_rows, total_cols = process_data(data)
    total_steps = 0
    part1_steps, new_bb = traverse(start, end, bb, total_rows, total_cols, walls)
    print(part1_steps)
    total_steps += part1_steps
    go_back_steps, new_bb2 = traverse(end, start, new_bb, total_rows, total_cols, walls)
    print(go_back_steps)
    total_steps += go_back_steps
    back_again_steps, new_bb3 = traverse(start, end, new_bb2, total_rows, total_cols, walls)
    print(back_again_steps)
    total_steps += back_again_steps
    return part1_steps, total_steps

def part2(data):
    pass
