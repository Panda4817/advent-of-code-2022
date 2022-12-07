
def process_data(data):
    return [[int(i) for i in line.split("\n")] for line in data.split("\n\n")]


def get_sums(elves):
    sums = []
    for elf in elves:
        sums.append(sum(elf))

    return sums


def part1(data):
    elves = process_data(data)
    sums = get_sums(elves)

    return max(sums)


def part2(data):
    elves = process_data(data)
    sums = get_sums(elves)

    sorted_sums = sorted(sums, reverse=True)
    return sum(sorted_sums[0:3])
