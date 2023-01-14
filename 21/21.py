
def subtract(a, b):
    return a - b


def division(a, b):
    return a / b


def multiply(a, b):
    return a * b


def add(a, b):
    return a + b


def process_data(data):
    lines = [line for line in data.split("\n")]
    numbers = {}
    operations = {}
    for line in lines:
        parts = line.split(": ")
        try:
            number = int(parts[1])
            numbers[parts[0]] = number
        except:
            is_plus = parts[1].split(" + ")
            if len(is_plus) == 2:
                operation = add
                operations[parts[0]] = (is_plus[0], is_plus[1], operation)
                continue

            is_subtract = parts[1].split(" - ")
            if len(is_subtract) == 2:
                operation = subtract
                operations[parts[0]] = (is_subtract[0], is_subtract[1], operation)
                continue

            is_prod = parts[1].split(" * ")
            if len(is_prod) == 2:
                operation = multiply
                operations[parts[0]] = (is_prod[0], is_prod[1], operation)
                continue

            is_division = parts[1].split(" / ")
            if len(is_division) == 2:
                operation = division
                operations[parts[0]] = (is_division[0], is_division[1], operation)
                continue

    return numbers, operations


def recurse_part1(key, numbers, operations):
    if key in numbers:
        return numbers[key]

    num1, num2, func = operations[key]
    number1 = recurse_part1(num1, numbers, operations)
    number2 = recurse_part1(num2, numbers, operations)
    return func(number1, number2)


def part1(data):
    numbers, operations = process_data(data)
    return recurse_part1("root", numbers, operations)


def get_func(func, a, b, hdir):
    if func == add:
        return subtract(a, b)

    if func == subtract:
        if hdir == "l":
            return add(a, b)
        else:
            return subtract(b, a)

    if func == multiply:
        return division(a, b)

    if hdir == "l":
        return multiply(a, b)
    else:
        return division(b, a)


def find_path(numbers, operations, key, target):
    path = []
    if key == target:
        return path, True

    if key in operations:
        l = operations[key][0]
        r = operations[key][1]
        p, found = find_path(numbers, operations, l, target)
        if found:
            return ["l"] + p, True

        p, found = find_path(numbers, operations, r, target)
        if found:
            return ["r"] + p, True

    return path, False


def part2(data):
    numbers, operations = process_data(data)

    path, _ = find_path(numbers, operations, "root", "humn")

    k = "root"
    hdir = path[0]
    if hdir == "l":
        other_k = operations[k][1]
        humn_k = operations[k][0]
    else:
        other_k = operations[k][0]
        humn_k = operations[k][1]

    n = recurse_part1(other_k, numbers, operations)

    for i in range(1, len(path)):
        hdir = path[i]
        func = operations[humn_k][2]
        if hdir == "l":
            other_k = operations[humn_k][1]
            humn_k = operations[humn_k][0]
        else:
            other_k = operations[humn_k][0]
            humn_k = operations[humn_k][1]

        ok = recurse_part1(other_k, numbers, operations)
        n = get_func(func, n, ok, hdir)

    return n
