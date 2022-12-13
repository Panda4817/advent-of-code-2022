import math


class Monkey:
    def __init__(self, items, operation, test, true, false, inspected):
        self.items = items
        self.operation = operation
        self.test = test
        self.true = true
        self.false = false
        self.inspected = inspected

    def __str__(self):
        return f"""
            items=<{self.items}>
            operation=<{self.operation}>
            test=<divide by {self.test}>
            true=<monkey {self.true}>
            false=<monkey {self.false}>
            inspected=<{self.inspected}>
        """

    def copy(self):
        return Monkey(self.items, self.operation, self.test, self.true, self.false, self.inspected)


def process_data(data):
    monkeys_string = [[l.strip() for l in line.split("\n")] for line in data.split("\n\n")]
    monkeys_class = {}
    for m in monkeys_string:
        key = int(m[0].split()[1][0])
        items = [int(i) for i in m[1].split(": ")[1].split(", ")]
        operation = m[2].split(": ")[1].split(" = ")[1]
        test = int(m[3].split()[-1])
        true = int(m[4].split()[-1])
        false = int(m[5].split()[-1])
        monkeys_class[key] = Monkey(items, operation, test, true, false, 0)

    return monkeys_class


def get_monkey_business(monkeys):
    inspected_numbers = sorted([m.inspected for m in monkeys.values()], reverse=True)
    return inspected_numbers[0] * inspected_numbers[1]


def round_inspection(monkeys, func):
    for k, m in monkeys.items():
        while m.items:
            old = m.items.pop()
            new = eval(m.operation)
            new = func(new)
            if new % m.test == 0:
                monkeys[m.true].items.append(new)
            else:
                monkeys[m.false].items.append(new)
            m.inspected += 1
    return monkeys


def part1(data):
    monkeys = process_data(data)
    for r in range(0, 20):
        monkeys = round_inspection(monkeys, lambda x: x // 3)

    return get_monkey_business(monkeys)


def part2(data):
    monkeys = process_data(data)
    common_divider = math.prod(v.test for v in monkeys.values())
    for r in range(0, 10000):
        monkeys = round_inspection(monkeys, lambda x: x % common_divider)

    return get_monkey_business(monkeys)
