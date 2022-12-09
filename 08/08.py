
def process_data(data):
    grid = [[int(tree) for tree in line] for line in data.split("\n")]
    return grid, len(grid)


def is_edge(r, c, total_rows, total_col):
    top = r - 1
    bottom = r + 1
    left = c - 1
    right = c + 1
    if top == -1 or bottom == total_rows or left == -1 or right == total_col:
        return True, top, bottom, left, right

    return False, top, bottom, left, right


def get_number_of_shorter_trees(number_of_trees, tree1_height, tree2_height):
    if tree1_height < tree2_height:
        number_of_trees += 1

    return number_of_trees


def part1(data):
    grid, total_rows = process_data(data)
    visible = 0
    for r in range(0, total_rows):
        total_col = len(grid[r])
        for c in range(0, total_col):
            edge, top, bottom, left, right = is_edge(r, c, total_rows, total_col)
            if edge:
                visible += 1
                continue

            h = grid[r][c]

            trees = 0
            for i in range(top, -1, -1):
                trees = get_number_of_shorter_trees(trees, grid[i][c], h)

            if trees == len(grid[0:r]):
                visible += 1
                continue

            trees = 0
            for i in range(bottom, total_rows):
                trees = get_number_of_shorter_trees(trees, grid[i][c], h)

            if trees == len(grid[bottom:total_rows]):
                visible += 1
                continue

            trees = 0
            for i in range(left, -1, -1):
                trees = get_number_of_shorter_trees(trees, grid[r][i], h)

            if trees == len(grid[r][0:c]):
                visible += 1
                continue

            trees = 0
            for i in range(right, total_col):
                trees = get_number_of_shorter_trees(trees, grid[r][i], h)

            if trees == len(grid[r][right:total_col]):
                visible += 1
                continue

    return visible


def part2(data):
    grid, total_rows = process_data(data)
    scenic_scores = []
    for r in range(0, total_rows):
        total_col = len(grid[r])
        for c in range(0, total_col):
            edge, top, bottom, left, right = is_edge(r, c, total_rows, total_col)
            if edge:
                continue

            h = grid[r][c]

            p_top = 0
            for i in range(top, -1, -1):
                p_top = get_number_of_shorter_trees(p_top, grid[i][c], h)

                if grid[i][c] >= h:
                    p_top += 1
                    break

            p_bottom = 0
            for i in range(bottom, total_rows):
                p_bottom = get_number_of_shorter_trees(p_bottom, grid[i][c], h)

                if grid[i][c] >= h:
                    p_bottom += 1
                    break

            p_left = 0
            for i in range(left, -1, -1):
                p_left = get_number_of_shorter_trees(p_left, grid[r][i], h)

                if grid[r][i] >= h:
                    p_left += 1
                    break

            p_right = 0
            for i in range(right, total_col):
                p_right = get_number_of_shorter_trees(p_right, grid[r][i], h)

                if grid[r][i] >= h:
                    p_right += 1
                    break

            score = p_right * p_left * p_top * p_bottom
            scenic_scores.append(score)

    return max(scenic_scores)
