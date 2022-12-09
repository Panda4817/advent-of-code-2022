
def process_data(data):
    return [line.split() for line in data.split("\n")]


def compare(index, k, ck, knots):
    if knots[ck][index] > knots[k][index]:
        return 1
    else:
        return -1


def move_knots(knots, to_add, index):
    for k, v in knots.items():
        if k == 0:
            knots[k][index] += to_add
            continue

        knot_in_front = k - 1
        if abs(knots[knot_in_front][1] - knots[k][1]) == 2 and knots[knot_in_front][0] == knots[k][0]:
            knots[k][1] += compare(1, k, knot_in_front, knots)
            continue

        if abs(knots[knot_in_front][0] - knots[k][0]) == 2 and knots[knot_in_front][1] == knots[k][1]:
            knots[k][0] += compare(0, k, knot_in_front, knots)
            continue

        if (abs(knots[knot_in_front][0] - knots[k][0]) == 2 and knots[knot_in_front][1] != knots[k][1]) \
                or (abs(knots[knot_in_front][1] - knots[k][1]) == 2 and knots[knot_in_front][0] != knots[k][0]):
            knots[k][0] += compare(0, k, knot_in_front, knots)
            knots[k][1] += compare(1, k, knot_in_front, knots)
            continue
    return knots


def get_all_coords_visited_by_tail(knots, visited_by_tail, moves, tail_number):
    for move in moves:
        direction = move[0]
        steps = int(move[1])
        if direction == "R":
            for i in range(1, steps + 1):
                knots = move_knots(knots, 1, 0)
                visited_by_tail[tuple(knots[tail_number])] = True

        if direction == "L":
            for i in range(1, steps + 1):
                knots = move_knots(knots, -1, 0)
                visited_by_tail[tuple(knots[tail_number])] = True

        if direction == "U":
            for i in range(1, steps + 1):
                knots = move_knots(knots, 1, 1)
                visited_by_tail[tuple(knots[tail_number])] = True

        if direction == "D":
            for i in range(1, steps + 1):
                knots = move_knots(knots, -1, 1)
                visited_by_tail[tuple(knots[tail_number])] = True

    return visited_by_tail


def get_knots(number_of_knots):
    knots = {}
    for i in range (0, number_of_knots):
        knots[i] = [0, 0]

    return knots


def part1(data):
    moves = process_data(data)
    knots = get_knots(2)
    visited_by_tail = get_all_coords_visited_by_tail(knots, {tuple([0, 0]): True}, moves, 1)
    return len(visited_by_tail)


def part2(data):
    moves = process_data(data)
    knots = get_knots(10)
    visited_by_tail = get_all_coords_visited_by_tail(knots, {tuple([0, 0]): True}, moves, 9)
    return len(visited_by_tail)
