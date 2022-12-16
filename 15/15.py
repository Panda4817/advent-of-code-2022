import math


class Sensor:
    def __init__(self, x, y, beacon_x, beacon_y):
        self.x, self.y, self.beacon_x, self.beacon_y = x, y, beacon_x, beacon_y
        self.mh = self.manhattan_dist()
        self.zone_corners, self.lowest_x, self.lowest_y, \
        self.highest_x, self.highest_y = self.exclusion_zone()

    def __str__(self):
        return f"sensor: [x={self.x}, y={self.y}], beacon: [x={self.beacon_x}, y={self.beacon_y}]"

    def manhattan_dist(self):
        return sum([abs(self.x - self.beacon_x), abs(self.y - self.beacon_y)])

    def exclusion_zone(self):
        lowest_x = self.x - self.mh
        highest_x = self.x + self.mh
        lowest_y = self.y - self.mh
        highest_y = self.y + self.mh

        return ((lowest_x, self.y), (highest_x, self.y), (self.x, lowest_y), (self.x, highest_y)), \
               lowest_x, lowest_y, highest_x, highest_y


def get_coords_from_input(string):
    parts = string.split(", ")
    x = int(parts[0].split("=")[-1])
    y = int(parts[1].split("=")[-1])
    return x, y


def process_data(data):
    lines = [line.split(": ") for line in data.split("\n")]
    sensors = []
    for line in lines:
        sx, sy = get_coords_from_input(line[0])
        bx, by = get_coords_from_input(line[1])
        sensors.append(Sensor(sx, sy, bx, by))

    return sensors


def get_distress_beacon_info(row, sensors, do_part1=False, part2_max_x=None):
    no_distress_beacon_count = 0
    possible_distress_beacon_coord = None
    sections_not_distress_beacon = set()
    from_coord = None
    to_coord = None
    for s in sensors:
        reduce_by = abs(s.y - row)
        lowest_x = s.lowest_x + reduce_by
        highest_x = s.highest_x - reduce_by
        if lowest_x <= highest_x:
            sections_not_distress_beacon.add((lowest_x, highest_x))

        if do_part1:
            if from_coord is not None and to_coord is not None:
                extra_low = lowest_x - from_coord
                extra_high = highest_x - to_coord
                if extra_low < 0:
                    no_distress_beacon_count += abs(extra_low)
                    from_coord = lowest_x
                if extra_high > 0:
                    no_distress_beacon_count += extra_high
                    to_coord = highest_x
            else:
                from_coord = lowest_x
                to_coord = highest_x
                no_distress_beacon_count += (highest_x - lowest_x)

    if part2_max_x:
        coordinates_sorted = sorted(sections_not_distress_beacon, key=lambda c: c[0])
        possible_x_value = set()
        low_x = 0
        max_x = part2_max_x
        for c in coordinates_sorted:
            if c[0] < low_x and c[1] > max_x:
                break

            if (c[0] < low_x and c[1] < low_x) or (c[0] > max_x and c[1] > max_x):
                continue

            if c[0] <= low_x <= c[1]:
                low_x = c[1] + 1
                continue

            if c[1] >= max_x >= c[0]:
                max_x = c[0] - 1
                continue

            if c[0] > low_x and (c[0] - low_x) == 1:
                possible_x_value.add(low_x)

            if c[1] < max_x and (max_x - c[1]) == 1:
                possible_x_value.add(max_x)

            if len(possible_x_value) > 1:
                possible_x_value = set()
                break

        if possible_x_value:
            possible_distress_beacon_coord = (possible_x_value.pop(), row)

    return no_distress_beacon_count, possible_distress_beacon_coord


def do_part1_and_part2(row, high, data):
    sensors = process_data(data)
    no_distress_beacon_count, possible_distress_beacon_coord = get_distress_beacon_info(row, sensors, True)
    part1_answer = no_distress_beacon_count
    freq_factor = 4000000
    low = 0
    for y in range(low, high + 1):
        no_distress_beacon_count, possible_distress_beacon_coord = get_distress_beacon_info(y, sensors, False,
                                                                                            high)
        if possible_distress_beacon_coord:
            break

    part2_answer = (possible_distress_beacon_coord[0] * freq_factor) + possible_distress_beacon_coord[1]
    return part1_answer, part2_answer


def part1_and_2_test(data):
    return do_part1_and_part2(10, 20, data)


def part1(data):
    return do_part1_and_part2(2000000, 4000000, data)


def part2(data):
    pass
