
def get_marker_end(marker_length, data):
    for i in range(0, len(data)):
        slice_end_index = i + marker_length
        if len(set(data[i: slice_end_index])) == marker_length:
            return slice_end_index


def part1(data):
    return get_marker_end(4, data)


def part2(data):
    return get_marker_end(14, data)
