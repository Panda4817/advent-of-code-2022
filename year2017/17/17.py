def spinlock_part1(step_size: int) -> int:
    buffer = [0]
    pos = 0
    for i in range(1, 2018):
        # Move forward 'step_size' steps within the current buffer
        pos = (pos + step_size) % len(buffer)
        # Insert the new value immediately after the current position
        buffer.insert(pos + 1, i)
        # The new element becomes the current position
        pos += 1

    # Find where 2017 ended up and return the value after it
    idx_2017 = buffer.index(2017)
    return buffer[(idx_2017 + 1) % len(buffer)]


def spinlock_part2(step_size: int) -> int:
    value_after_zero = -1
    pos = 0  # 'current' position in the virtual buffer
    length = 1  # initially, our buffer is just [0]

    # We insert from 1 up to 50,000,000
    for i in range(1, 50_000_000 + 1):
        # Move 'step_size' steps in a circle of size 'length'
        pos = (pos + step_size) % length

        # If we are about to insert right after 0 (i.e., pos == 0),
        # then the new value i goes immediately after 0
        if pos == 0:
            value_after_zero = i

        # Insert (virtually) at pos+1
        pos += 1
        length += 1

    return value_after_zero


def part1(data):
    step_size = int(data)
    return spinlock_part1(step_size)


def part2(data):
    step_size = int(data)
    return spinlock_part2(step_size)
