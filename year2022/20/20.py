
def process_data(data):
    lines = data.split("\n")
    return {i: {(int(line)): i} for line, i in zip(lines, range(0, len(lines)))}


def process_data_part2(data):
    lines = data.split("\n")
    return {i: {(int(line) * 811589153): i} for line, i in zip(lines, range(0, len(lines)))}


def mix(id, total_length, order):
    while id < total_length:
        index = None
        prev = None
        for k, v in order[id].items():
            if k == 0:
                break
            prev = v

            index = (k + v) % (total_length - 1)

            order[id][k] = index

        if index is not None:
            # print(k, prev, index)
            for i, n in order.items():
                if id == i:
                    continue
                for k, v in order[i].items():
                    if prev > index and index <= v <= prev:
                        order[i][k] = v + 1
                        continue
                    if prev < index and prev <= v <= index:
                        order[i][k] = v - 1

        id += 1

    return order


def add_up(order, total_length):
    numbers_only = []
    for id, n in order.items():

        for k, v in order[id].items():
            numbers_only.append((k, v))

    numbers_only.sort(key=lambda x: x[1])
    numbers_only = [n for n, i in numbers_only]
    index = 0
    for n in numbers_only:
        if n == 0:
            break
        index += 1
    add_up = []
    for i in range(0, 3001):
        if i == 1000 or i == 2000 or i == 3000:
            add_up.append(numbers_only[index])

        index += 1
        if index == total_length:
            index = 0

    return sum(add_up)


def part1(data):
    order = process_data(data)
    total_length = len(order)

    id = 0
    order = mix(id, total_length, order)

    return add_up(order, total_length)


def part2(data):
    order = process_data_part2(data)
    total_length = len(order)

    for round in range(0, 10):
        id = 0
        order = mix(id, total_length, order)

    return add_up(order, total_length)
