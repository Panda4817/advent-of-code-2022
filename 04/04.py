
def process_data(data):
    lines = [j.split("-") for i in data.split("\n") for j in i.split(",")]
    return lines, len(lines)


def get_sections(i, elves):
    a_low = int(elves[i][0])
    a_high = int(elves[i][1])
    b_low = int(elves[i + 1][0])
    b_high = int(elves[i + 1][1])
    return a_low, a_high, b_low, b_high


def part1(data):
    elves, size = process_data(data)
    total = 0
    for i in range(0, size, 2):
        a_low, a_high, b_low, b_high = get_sections(i, elves)
        if (a_low <= b_low and a_high >= b_high) or (a_low >= b_low and a_high <= b_high):
            total += 1

    return total


def part2(data):
    elves, size = process_data(data)
    total = 0
    for i in range(0, size, 2):
        a_low, a_high, b_low, b_high = get_sections(i, elves)
        if (a_high >= b_low and a_low <= b_high) or (b_high >= a_low and b_low <= a_high):
            total += 1

    return total
