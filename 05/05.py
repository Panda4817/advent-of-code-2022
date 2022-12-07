
def process_data(data):
    parts = [i.split("\n") for i in data.split("\n\n")]
    crates = {}
    height_crates = len(parts[0])
    number_of_crates = len(parts[0][-1].split())
    for i in range(1, number_of_crates+1):
        crates[i] = []

    for row in parts[0][0:height_crates-1]:
        stacks = row.split(" ")
        size_of_stacks = len(stacks)
        if size_of_stacks == number_of_crates:
            for i in range(0, number_of_crates):
                stack_num = i + 1
                crates[stack_num].insert(0, stacks[i][1])
            continue

        crate_num = 0
        counter = 0
        for i in range(0, size_of_stacks):
            if counter == 4:
                crate_num += 1
                counter = 0

            if stacks[i] != "":
                if counter == 0:
                    crate_num += 1
                crates[crate_num].insert(0, stacks[i][1])
                counter = 0
                continue

            counter += 1

    moves = []
    for row in parts[1]:
        procedures = row.split()
        moves.append([int(procedures[1]), int(procedures[3]), int(procedures[5])])

    return crates, moves


def get_top_crates(crates):
    return "".join([crate[-1] for crate in crates.values()])


def part1(data):
    crates, moves = process_data(data)
    for move in moves:
        size = move[0]
        from_stack = move[1]
        to_stack = move[2]
        for i in range(0, size):
            crate = crates[from_stack].pop()
            crates[to_stack].append(crate)

    return get_top_crates(crates)


def part2(data):
    crates, moves = process_data(data)
    for move in moves:
        size = move[0]
        from_stack = move[1]
        to_stack = move[2]
        crates_to_move = []

        for i in range(0, size):
            crate = crates[from_stack].pop()
            crates_to_move.insert(0, crate)

        for c in crates_to_move:
            crates[to_stack].append(c)

    return get_top_crates(crates)
