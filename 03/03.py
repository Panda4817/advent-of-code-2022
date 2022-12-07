def process_data(data):
    return [list(i) for i in data.split("\n")]


def get_priority(item):
    priorities = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return priorities.index(item) + 1


def part1(data):
    rucksacks = process_data(data)
    total = 0
    for rucksack in rucksacks:
        size = len(rucksack)
        half = size // 2
        common = set(rucksack[0:half]) & set(rucksack[half:size])
        for item in common:
            total += get_priority(item)

    return total


def part2(data):
    rucksacks = process_data(data)
    total = 0
    for i in range(0, len(rucksacks), 3):
        common = (set(rucksacks[i]) & set(rucksacks[i + 1]) & set(rucksacks[i + 2]))
        for item in common:
            total += get_priority(item)

    return total
