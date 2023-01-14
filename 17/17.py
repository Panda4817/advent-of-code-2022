def process_data(data):
    return [1 if a == ">" else -1 for a in list(data)]


def move_down(max_height, shape_pos, rock_squares):
    new_coords = set()
    for (x, y) in shape_pos:
        new_pos = (x, y + 1)
        if new_pos in rock_squares or new_pos[1] == max_height:
            return False, shape_pos
        new_coords.add(new_pos)

    return True, new_coords


def move_with_jet(shape_pos, x_add, max_width, rock_squares, left, right):
    new_coords = set()
    for (x, y) in shape_pos:
        new_pos = (x + x_add, y)
        new_coords.add(new_pos)

    for new_pos in new_coords:
        if new_pos in rock_squares or new_pos[0] == max_width or new_pos[0] == -1:
            new_coords = shape_pos
            break

    max_x = max(x for (x, y) in new_coords)
    min_x = min(x for (x, y) in new_coords)
    if max_x < max_width - 1:
        right = True
    else:
        right = False
    if min_x > 0:
        left = True
    else:
        left = False

    return left, right, new_coords


def print_grid(shape_pos, rock_squares, max_height, max_width):
    ansi_grey = "\033[30m\033[40m"
    ansi_yellow = "\033[33m\033[43m"
    all_rocks = rock_squares | shape_pos
    min_y = min(y for (x, y) in all_rocks)
    s = True
    for y in range(min_y, min_y + 20):
        for x in range(0, max_width):
            if (x, y) in rock_squares:
                print("#", end="")
                # if s:
                #     print(ansi_yellow)
                #     s = False
                # else:
                #     print(ansi_grey)
                #     s = True
            elif (x, y) in shape_pos:
                print("@", end="")
            else:
                print(".", end="")
        print()
    print()


def part1(data):
    arrows = process_data(data)
    arrows = arrows * 1000
    # print(arrows)
    max_height = 7
    max_width = 7
    shapes = {
        # all starting coords
        "dash": {(2, 3), (3, 3), (4, 3), (5, 3)},
        "plus": {(3, 1), (2, 2), (3, 2), (4, 2), (3, 3)},
        "L": {(4, 1), (4, 2), (2, 3), (3, 3), (4, 3)},
        "line": {(2, 0), (2, 1), (2, 2), (2, 3)},
        "square": {(2, 2), (3, 2), (2, 3), (3, 3)}
    }
    rock_squares = set()
    keys = [key for key in shapes] * 1000
    jet_index = 0
    for r in range(0, 2022):
        k = keys[r]
        shape_pos = shapes[k]
        if rock_squares:
            min_y = min(y for (x, y) in rock_squares)
            adjust_y = min_y - max_height
            shape_pos = {(x, y + adjust_y) for (x, y) in shapes[k]}
        left = True
        right = True
        can_move_down = True
        while can_move_down:
            x_add = arrows[jet_index]
            if (x_add == 1 and right is True) or (x_add == -1 and left is True):
                left, right, shape_pos = move_with_jet(shape_pos, x_add, max_width, rock_squares, left, right)
            jet_index += 1

            can_move_down, shape_pos = move_down(max_height, shape_pos, rock_squares)

        rock_squares = rock_squares | shape_pos
    min_y = min(y for (x, y) in rock_squares)
    return max_height - min_y


def get_pattern(min_y, rock_squares, top):
    top_fifty_with_rocks = set()
    for y in range(min_y, min_y + top):
        for x in range(0, 7):
            if (x, y) in rock_squares:
                top_fifty_with_rocks.add((x, y))

    return top_fifty_with_rocks


def part2(data):
    arrows = process_data(data)
    max_height = 7
    max_width = 7
    shapes = {
        # all starting coords
        "dash": {(2, 3), (3, 3), (4, 3), (5, 3)},
        "plus": {(3, 1), (2, 2), (3, 2), (4, 2), (3, 3)},
        "L": {(4, 1), (4, 2), (2, 3), (3, 3), (4, 3)},
        "line": {(2, 0), (2, 1), (2, 2), (2, 3)},
        "square": {(2, 2), (3, 2), (2, 3), (3, 3)}
    }
    rock_squares = set()
    keys = [key for key in shapes]
    jet_index = 0
    shape_index = 0
    adjust_y = 0
    r = 1
    rocks = 1000000000000

    # 1705 2582 7  - these values are where the pattern repeats (specific for my data)
    h = (rocks // 1705) * 2582
    remain = rocks % 1705

    # This while loop run with rocks instead of remain to find values of where pattern repeats
    while r <= remain:

        k = keys[shape_index]
        shape_pos = {(x, y + adjust_y) for (x, y) in shapes[k]}
        left = True
        right = True
        can_move_down = True
        move_down_count = 0
        while can_move_down:
            move_down_count += 1
            x_add = arrows[jet_index]
            if (x_add == 1 and right is True) or (x_add == -1 and left is True):
                left, right, shape_pos = move_with_jet(shape_pos, x_add, max_width, rock_squares, left, right)
            jet_index += 1
            if jet_index == len(arrows):
                jet_index = 0
            can_move_down, shape_pos = move_down(max_height, shape_pos, rock_squares)

        rock_squares = rock_squares | shape_pos
        min_y = min(y for (x, y) in rock_squares)

        adjust_y = min_y - max_height
        shape_index += 1
        if shape_index == 5:
            shape_index = 0

        r += 1
    min_y = min(y for (x, y) in rock_squares)
    return (max_height - min_y) + h
