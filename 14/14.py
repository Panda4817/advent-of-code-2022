class Cave:
    def __init__(self, data) -> None:
        self.spring = (500, 0)
        self.map, \
            self.min_x, \
            self.max_x_part1, \
            self.max_x_part2, \
            self.max_y_part1, self.max_y_part2, \
            self.min_y = self.process_data(data)

    def __str__(self) -> str:
        ansi_grey = "\033[30m\033[40m"
        ansi_yellow = "\033[33m\033[43m"
        ansi_clear = "\033[0m"
        ansi_light_grey = "\033[37m\033[47m"
        string = ""
        for r in range(0, self.max_y_part2 + 1):
            for c in range(self.max_x_part1 - 250, self.max_x_part2 + 1):
                if self.map[r][c] in ('o', '+'):
                    string += ansi_yellow
                elif self.map[r][c] == '#':
                    string += ansi_grey
                elif self.map[r][c] == '.':
                    string += ansi_light_grey
                string += self.map[r][c] + ansi_clear
            string += "\n"
        return string

    def process_data(self, data):
        map = []
        lines = [line.split(" -> ") for line in data.split("\n")]
        x_numbers = set()
        y_numbers = set()
        rock = []

        for line in lines:
            prev_x, prev_y = -1, -1
            for val in line:
                parts = val.split(",")
                x = int(parts[0])
                y = int(parts[1])
                if prev_x == -1 and prev_y == -1:
                    prev_x = x
                    prev_y = y
                    x_numbers.add(x)
                    y_numbers.add(y)
                    rock.append((x, y))

                if x > prev_x:
                    for i in range(prev_x, x+1):
                        x_numbers.add(i)
                        y_numbers.add(y)
                        rock.append((i, y))

                if x < prev_x:
                    for i in range(prev_x, x-1, -1):
                        x_numbers.add(i)
                        y_numbers.add(y)
                        rock.append((i, y))

                if y > prev_y:
                    for i in range(prev_y, y + 1):
                        x_numbers.add(x)
                        y_numbers.add(i)
                        rock.append((x, i))

                if y < prev_y:
                    for i in range(prev_y, y - 1, -1):
                        x_numbers.add(x)
                        y_numbers.add(i)
                        rock.append((x, i))

                prev_x = x
                prev_y = y

        max_x_part1 = max(x_numbers)
        max_y_part1 = max(y_numbers)
        max_y_part2 = max_y_part1 + 2
        max_x_part2 = 750
        min_x = 0

        for r in range(0, max_y_part2 + 1):
            if r == max_y_part2:
                row = ["#" for c in range(min_x, max_x_part2 + 1)]
            else:
                row = ["." for c in range(min_x, max_x_part2 + 1)]
            map.append(row)

        map[self.spring[1]][self.spring[0]] = "+"
        for coord in rock:
            map[coord[1]][coord[0]] = "#"

        return map, min_x, max_x_part1, max_x_part2, max_y_part1, max_y_part2, min(y_numbers)

    def reached_end(self, y):
        if y >= self.max_y_part1:
            return True

        return False

    def start_spring(self):
        x, y = self.spring
        part1_units = 0
        part1_done = False
        part2_units = 0
        while True:
            part2_units += 1
            while True:
                if self.map[y + 1][x] == ".":
                    y += 1

                if self.reached_end(y):
                    part1_done = True

                try:
                    while self.map[y + 1][x] == "o" or self.map[y + 1][x] == "#":
                        if self.map[y + 1][x - 1] == ".":
                            y += 1
                            x -= 1
                        elif self.map[y + 1][x + 1] == ".":
                            y += 1
                            x += 1
                        else:
                            break

                except IndexError:
                    print("max_x_part2 not long enough")
                    break

                if (y + 1 == self.max_y_part2) or (self.map[y + 1][x] != "."
                                                   and self.map[y + 1][x-1] != "."
                                                   and self.map[y + 1][x + 1] != "."):
                    break

            if (x, y) == self.spring:
                break

            self.map[y][x] = "o"
            if not part1_done:
                part1_units += 1
            x, y = self.spring

        print(self)
        return part1_units, part2_units


def part1(data):
    cave = Cave(data)
    return cave.start_spring()
