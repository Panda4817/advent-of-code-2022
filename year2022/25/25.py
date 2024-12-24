import copy


def process_data(data):
    signs = {
        "=": -2,
        "-": -1
    }
    lines = data.split("\n")
    input_list = []
    max_length = 0
    for line in lines:
        row = []
        for char in line:
            try:
                number = int(char)
                row.append(number)
            except:
                number = signs[char]
                row.append(number)
        input_list.append(row)
        if len(row) > max_length:
            max_length = len(row)

    print(max_length)
    return input_list, max_length


def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


def part1(data):
    snafu_numbers, max_length = process_data(data)
    # print(snafu_numbers)

    powers = []
    for i in range(0, max_length + 1):
        powers.append(5 ** i)
    powers.reverse()
    print(powers)
    total = 0
    for num in snafu_numbers:
        n = copy.deepcopy(num)
        while len(n) < max_length + 1:
            n.insert(0, 0)
        # print(n)
        s = sum([n[i] * powers[i] for i in range(0, max_length + 1)])
        # print(s)
        total += s

    nb = numberToBase(total, 5)
    print(nb)
    for i in range(len(nb) - 1, -1, -1):
        if nb[i] == 3:
            nb[i] = -2
            nb[i - 1] += 1

        elif nb[i] == 4:
            nb[i] = -1
            nb[i - 1] += 1

        elif nb[i] == 5:
            nb[i] = 0
            nb[i - 1] += 1

    snafu = ""
    for n in nb:
        if n == -1:
            snafu += "-"
        elif n == -2:
            snafu += "="
        else:
            snafu += str(n)

    return snafu


def part2(data):
    pass
