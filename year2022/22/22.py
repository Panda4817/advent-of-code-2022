def process_data(data, grid_size):
    parts = data.split("\n\n")
    grid_lines = parts[0].split("\n")
    grid = []
    row_count = 0
    max_column = 0
    column_count = 0
    side_count = 0
    side = [1, 2, 3, 4, 5, 6]
    index = 0
    skip_by = 1
    for r in grid_lines:
        row_count += 1
        if row_count == grid_size + 1:
            index += skip_by
            skip_by = 1
        if row_count == grid_size + grid_size + 1:
            index += skip_by
            skip_by = 1
        if row_count == grid_size + grid_size + grid_size +  1:
            index += skip_by
            skip_by = 1
        row = []
        for c in r:
            column_count += 1
            if c == " ":
                row.append(-7)
            elif c == "#":
                side_count += 1
                s = side[index]
                if (grid_size + 1) <= side_count < (grid_size + grid_size + 1):
                    s = side[index + 1]
                    skip_by = 2
                if side_count >= grid_size + grid_size + 1:
                    s = side[index + 2]
                    skip_by = 3
                row.append(-s)
            else:
                side_count += 1
                s = side[index]
                if (grid_size + 1) <= side_count < (grid_size + grid_size + 1):
                    s = side[index + 1]
                    skip_by = 2
                if side_count >= grid_size + grid_size + 1:
                    s = side[index + 2]
                    skip_by = 3
                row.append(s)

        grid.append(row)
        side_count = 0
        if column_count > max_column:
            max_column = column_count
        column_count = 0

    for r in grid:
        while len(r) != max_column:
            r.append(-7)

    for r in grid:
        for c in r:
            print(c, end="  " if c > 0 else " ")
        print()
        prev_c = None

    x = 0
    start = (0, 0)
    for c in grid[0]:
        if c == 1:
            start = (0, x)
            break
        x += 1

    parts[1] = parts[1].replace("L", " L ")
    parts[1] = parts[1].replace("R", " R ")
    instructions = [i if i == "L" or i == "R" else int(i) for i in parts[1].split()]

    return grid, start, instructions, max_column


def move_right_left_part1(xs, ys, grid, facing, move, max_col):
    if wrap_time_part1(ys, xs, move, facing, max_col, grid, x=True):
        if facing == "r":
            nx = 0
        else:
            nx = max_col - 1
        wall_found = False
        while True:
            if grid[ys][nx] == -7:
                nx += move[facing]
                continue

            if grid[ys][nx] in (-1, -2, -3, -4, -5, -6):
                wall_found = True
                break

            if grid[ys][nx] in (1, 2, 3, 4, 5, 6):
                break

        if wall_found:
            return xs

        xs = nx
        return xs

    if grid[ys][xs + move[facing]] in (-1, -2, -3, -4, -5, -6):
        return xs

    if grid[ys][xs + move[facing]] in (1, 2, 3, 4, 5, 6):
        xs += move[facing]

    return xs


def wrap_time_part1(ys, xs, move, facing, max_n, grid, y=False, x=False):
    if y:
        if ys + move[facing] < 0 or ys + move[facing] == max_n:
            return True

        if grid[ys + move[facing]][xs] == -7:
            return True

    if x:
        if (xs + move[facing]) < 0 or (xs + move[facing]) == max_n:
            return True

        if grid[ys][xs + move[facing]] == -7:
            return True

    return False


def wrap_time_part2(ys, xs, move, facing, side, max_col, max_row, grid, y=False, x=False):
    if y:
        if ys + move[facing] < 0 or ys + move[facing] == max_row:
            return True

        if grid[ys + move[facing]][xs] == -7:
            return True

        if grid[ys + move[facing]][xs] != -side and grid[ys + move[facing]][xs] != side:
            return True

    if x:
        if (xs + move[facing]) < 0 or (xs + move[facing]) == max_col:
            return True

        if grid[ys][xs + move[facing]] == -7:
            return True

        if grid[ys][xs + move[facing]] != -side and grid[ys][xs + move[facing]] != side:
            return True

    return False


def move_up_down_part1(xs, ys, grid, facing, move, max_row):
    if wrap_time_part1(ys, xs, move, facing, max_row, grid, y=True):
        if facing == "d":
            ny = 0
        else:
            ny = max_row - 1
        wall_found = False
        while True:
            if grid[ny][xs] == -7:
                ny += move[facing]
                continue

            if grid[ny][xs] in (-1, -2, -3, -4, -5, -6):
                wall_found = True
                break

            if grid[ny][xs] in (1, 2, 3, 4, 5, 6):
                break

        if wall_found:
            return ys

        ys = ny
        return ys

    if grid[ys + move[facing]][xs] in (-1, -2, -3, -4, -5, -6):
        return ys

    if grid[ys + move[facing]][xs] in (1, 2, 3, 4, 5, 6):
        ys += move[facing]

    return ys


def do_part1(data, test=False):
    grid_size = 50
    if test:
        grid_size = 4
    grid, (ys, xs), commands, max_col = process_data(data, grid_size)
    max_row = len(grid)
    # print(commands)
    move = {"r": 1, "l": -1, "d": 1, "u": -1}
    turn = {"r": {"L": "u", "R": "d"}, "l": {"L": "d", "R": "u"}, "d": {"L": "r", "R": "l"}, "u": {"L": "l", "R": "r"}}
    facing_score = {"r": 0, "l": 2, "d": 1, "u": 3}
    facing = "r"
    for c in commands:
        # print(c, facing)
        if type(c) == int:
            # print(ys, xs)
            for i in range(0, c):

                if facing == "r" or facing == "l":
                    xs = move_right_left_part1(xs, ys, grid, facing, move, max_col)

                if facing == "u" or facing == "d":
                    ys = move_up_down_part1(xs, ys, grid, facing, move, max_row)
            # print(ys, xs)
            continue

        facing = turn[facing][c]
        # print(facing)

    return (1000 * (ys + 1)) + (4 * (xs + 1)) + facing_score[facing]


def part1_test(data):
    return do_part1(data, test=True)


def part1(data):
    return do_part1(data)


def move_it(xs, ys, grid, facing, move, max_col, max_row, side, wrap_to, grid_size):
    if wrap_time_part2(ys, xs, move, facing, side, max_col, max_row, grid,
                       x=(True if facing in ("l", "r") else False),
                       y=(True if facing in ("u", "d") else False)):
        n_side, n_facing, multiplier, mod_m = wrap_to[(side, facing)]
        print(n_facing)
        test_x = xs
        test_y = ys
        if facing == "l" or facing == "r":
            test_x += move[facing]
        else:
            test_y += move[facing]
        x_offset = test_x % grid_size
        y_offset = test_y % grid_size
        nx, ny = None, None
        print(f"BEFORE x={xs}, y={ys}, cube_side={side}, facing={facing}")
        if n_facing == "r":
            nx = 0
            if side == 4 and facing == "u":
                ny = x_offset + grid_size
            elif side == 4 and facing == "l":
                ny = (grid_size - 1) - y_offset
            elif side == 1 and facing == "l":
                ny = ((3 * grid_size) - 1) - y_offset
            elif side == 1 and facing == "u":
                ny = (3 * grid_size) + x_offset
            elif facing == "r":
                nx = xs + move[n_facing]
                ny = ys

        elif n_facing == "l":
            nx = max_col - 1
            if side == 5 and facing == "r":
                ny = (grid_size - 1) - y_offset
            elif side == 5 and facing == "d":
                ny = (3 * grid_size) + x_offset
            elif side == 2 and facing == "r":
                ny = ((3 * grid_size) - 1) - y_offset
            elif side == 2 and facing == "d":
                ny = grid_size + x_offset
            elif facing == "l":
                nx = xs + move[n_facing]
                ny = ys

        elif n_facing == "d":
            ny = 0
            if side == 3 and facing == "l":
                nx = y_offset
            elif side == 6 and facing == "l":
                nx = grid_size + y_offset
            elif side == 6 and facing == "d":
                nx = (2 * grid_size) + y_offset
            elif facing == "d":
                ny = ys + move[n_facing]
                nx = xs

        elif n_facing == "u":
            ny = max_row - 1
            if side == 2 and facing == "u":
                nx = x_offset
            elif side == 6 and facing == "r":
                nx = grid_size + y_offset
            elif side == 3 and facing == "r":
                nx = (2 * grid_size) + y_offset
            elif facing == "u":
                ny = ys + move[n_facing]
                nx = xs

        print(f"AFTER x={nx}, y={ny}, cube_side={n_side}, facing={n_facing}")
        wall_found = False
        while True:
            if grid[ny][nx] == -7:
                if n_facing == "r" or n_facing == "l":
                    nx += move[n_facing]
                else:
                    ny += move[n_facing]
                continue

            if grid[ny][nx] == -n_side:
                print("BLOCK")
                wall_found = True
                break

            if grid[ny][nx] == n_side:
                break

        if wall_found:
            return xs, ys, side, facing, True

        xs = nx
        ys = ny
        side = n_side
        facing = n_facing
        return xs, ys, side, facing, False

    if facing == "r" or facing == "l":
        if grid[ys][xs + move[facing]] == -side:
            return xs, ys, side, facing, True

        if grid[ys][xs + move[facing]] == side:
            xs += move[facing]
    else:
        if grid[ys + move[facing]][xs] == -side:
            return xs, ys, side, facing, True

        if grid[ys + move[facing]][xs] == side:
            ys += move[facing]

    return xs, ys, side, facing, False


def do_part2(data, test=False):
    grid_size = 50
    if test:
        grid_size = 4
    grid, (ys, xs), commands, max_col = process_data(data, grid_size)
    max_row = len(grid)
    move = {"r": 1, "l": -1, "d": 1, "u": -1}
    turn = {"r": {"L": "u", "R": "d"}, "l": {"L": "d", "R": "u"}, "d": {"L": "r", "R": "l"}, "u": {"L": "l", "R": "r"}}
    facing_score = {"r": 0, "l": 2, "d": 1, "u": 3}
    facing = "r"
    side = 1
    block = False
    wrap_to = {
        (1, "r"): (2, "r", 0, 0), (1, "l"): (4, "r", 2, -1), (1, "d"): (3, "d", 0, 0), (1, "u"): (6, "r", 3, 1),
        (2, "r"): (5, "l", 2, -1), (2, "l"): (1, "l", 0, 0), (2, "d"): (3, "l", 1, -1), (2, "u"): (6, "u", 2, 1),
        (3, "r"): (2, "u", 1, -1), (3, "l"): (4, "d", -1, 1), (3, "d"): (5, "d", 0, 0), (3, "u"): (1, "u", 0, 0),
        (4, "r"): (5, "r", 0, 0), (4, "l"): (1, "r", 1, -1), (4, "d"): (6, "d", 0, 0), (4, "u"): (3, "r", -1, 1),
        (5, "r"): (2, "l", 1, -1), (5, "l"): (4, "l", 0, 0), (5, "d"): (6, "l", 1, -1), (5, "u"): (3, "u", 0, 0),
        (6, "r"): (5, "u", 1, -1), (6, "l"): (1, "d", 1, 1), (6, "d"): (2, "d", 2, 0), (6, "u"): (4, "u", 0, 0),
    }

    if test:
        wrap_to = {
            (1, "r"): (6, "l", 2, 1), (1, "l"): (3, "d", -1, -1), (1, "d"): (4, "d", 0, 0), (1, "u"): (2, "d", -2, 1),
            (2, "r"): (3, "r", 0, 0), (2, "l"): (6, "u", 3, 1), (2, "d"): (5, "u", 2, -1), (2, "u"): (1, "d", 2, -1),
            (3, "r"): (4, "r", 0, 0), (3, "l"): (2, "l", 0, 0), (3, "d"): (5, "r", 1, -1), (3, "u"): (1, "r", -1, 1),
            (4, "r"): (6, "d", 1, -1), (4, "l"): (3, "l", 0, 0), (4, "d"): (5, "d", 0, 0), (4, "u"): (1, "u", 0, 0),
            (5, "r"): (6, "r", 0, 0), (5, "l"): (3, "u", -1, 1), (5, "d"): (2, "u", -2, -1), (5, "u"): (4, "u", 0, 0),
            (6, "r"): (1, "l", -2, 1), (6, "l"): (5, "l", 0, 0), (6, "d"): (2, "r", -1, -1), (6, "u"): (4, "l", -1, 1)
        }

    for c in commands:
        print(f"c={c}")
        if type(c) == int:
            # print(ys, xs)

            for i in range(0, c):
                xs, ys, side, facing, block = move_it(xs, ys, grid, facing, move, max_col, max_row, side, wrap_to, grid_size)
                if block:
                    print("BLOCK")
                    break
            print(f"FINAL x={xs}, y={ys}, cube_side={side}, facing={facing}")
            continue

        facing = turn[facing][c]
        # print(f"x={xs}, y={ys}, cube_side={side}, facing={facing}")
        # print(facing)

    return (1000 * (ys + 1)) + (4 * (xs + 1)) + facing_score[facing]


def part2_test(data):
    return do_part2(data, test=True)


def part2(data):
    return do_part2(data)
