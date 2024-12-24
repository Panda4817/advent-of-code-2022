
def process_data(data):
    return [line.split() for line in data.split("\n")]


def update_cycle(cycle):
    cycle += 1
    return cycle


def update_strength(cycle, strengths, x):
    strength = cycle * x
    cycles = [20, 60, 100, 140, 180, 220]
    if cycle in cycles:
        strengths.append(strength)

    return strengths


def part1(data):
    instructions = process_data(data)
    cycle = 0
    strengths = []
    x = 1
    for instruction in instructions:
        if instruction[0] == "noop":
            cycle = update_cycle(cycle)
            strengths = update_strength(cycle, strengths, x)

        if instruction[0] == "addx":
            for i in range(0, 2):
                cycle = update_cycle(cycle)
                strengths = update_strength(cycle, strengths, x)
            x += int(instruction[1])

    return sum(strengths)


def draw(cycle, x, counter):
    cycles = [41, 81, 121, 161, 201]
    if cycle in cycles:
        print()
        counter = 0

    if counter in [x-1, x, x+1]:
        print("#", end="")
    else:
        print(" ", end="")

    counter += 1
    return counter


def part2(data):
    instructions = process_data(data)
    cycle = 0
    x = 1
    counter = 0
    for instruction in instructions:
        if instruction[0] == "noop":
            cycle = update_cycle(cycle)
            counter = draw(cycle, x, counter)

        if instruction[0] == "addx":
            for i in range(0, 2):
                cycle = update_cycle(cycle)
                counter = draw(cycle, x, counter)
            x += int(instruction[1])

    print()
