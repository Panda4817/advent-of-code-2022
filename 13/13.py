import functools
import json


def process_data(data):
    packets = [l for line in data.split("\n\n") for l in line.split("\n")]
    res = []
    for packet in packets:
        res.append(json.loads(packet))
    return res


def is_in_order(left, right, l, r, prev):
    try:
        li = left[l]
        ri = right[r]
    except IndexError:
        if len(left) < len(right):
            return True

        if len(right) < len(left):
            return False

        old_left, old_right, old_l, old_r = prev.pop()
        return is_in_order(old_left, old_right, old_l + 1, old_r + 1, prev)

    if type(li) == int and type(ri) == int:
        if li < ri:
            return True

        if ri < li:
            return False

        return is_in_order(left, right, l + 1, r + 1, prev)

    new_l = 0
    new_r = 0
    prev.append((left, right, l, r))
    if type(li) == list and type(ri) == list:
        new_left = li
        new_right = ri
        return is_in_order(new_left, new_right, new_l, new_r, prev)

    if type(li) == list and type(ri) == int:
        new_left = li
        new_right = [ri]
        return is_in_order(new_left, new_right, new_l, new_r, prev)

    if type(li) == int and type(ri) == list:
        new_left = [li]
        new_right = ri
        return is_in_order(new_left, new_right, new_l, new_r, prev)


def part1(data):
    packets = process_data(data)
    sum_of_pair_indices = 0
    pair = 1
    for i in range(0, len(packets), 2):
        if is_in_order(packets[i], packets[i + 1], 0, 0, []):
            sum_of_pair_indices += pair
        pair += 1

    return sum_of_pair_indices


def compare(item1, item2):
    if is_in_order(item1, item2, 0, 0, []):
        return -1
    else:
        return 1


def part2(data):
    packets = process_data(data)
    d1 = [[2]]
    d2 = [[6]]
    packets.append(d1)
    packets.append(d2)
    d1_index = 0
    d2_index = 0
    packets.sort(key=functools.cmp_to_key(compare))
    for i in range(0, len(packets)):
        if packets[i] == d1:
            d1_index = i + 1

        if packets[i] == d2:
            d2_index = i + 1

    return d1_index * d2_index
