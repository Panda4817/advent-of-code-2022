
def process_data(data):
    return [i.split(" ") for i in data.split("\n")]


class Player:
    def __init__(self, shape, points, rock=False, paper=False, scissors=False):
        self.shape_letter = shape
        self.shape_points = points
        self.is_rock = rock
        self.is_paper = paper
        self.is_scissors = scissors
        self.to_win = 'B' if rock else 'C' if paper else 'A'
        self.to_lose = 'C' if rock else 'A' if paper else 'B'

    def play_rock_paper_scissors(self, other):
        if (self.is_rock and other.is_rock) \
                or (self.is_paper and other.is_paper) \
                or (self.is_scissors and other.is_scissors):
            return 3

        if self.is_rock and other.is_scissors:
            return 6

        if self.is_scissors and other.is_paper:
            return 6

        if self.is_paper and other.is_rock:
            return 6

        return 0

    def choose_strategy_based_shape(self, strategy):
        if strategy == 'X':
            return get_player(self.to_lose)

        if strategy == 'Y':
            return get_player(self.shape_letter)

        if strategy == 'Z':
            return get_player(self.to_win)


def get_player(letter):
    rock = ['A', 'X']
    paper = ['B', 'Y']
    scissors = ['C', 'Z']

    if letter in rock:
        return Player(letter, 1, rock=True)

    if letter in paper:
        return Player(letter, 2, paper=True)

    if letter in scissors:
        return Player(letter, 3, scissors=True)


def part1(data):
    games = process_data(data)

    total = 0
    for round in games:
        other = get_player(round[0])
        me = get_player(round[1])
        round_total = me.shape_points + me.play_rock_paper_scissors(other)
        total += round_total

    return total


def part2(data):
    games = process_data(data)

    total = 0
    for round in games:
        other = get_player(round[0])
        me = other.choose_strategy_based_shape(round[1])
        round_total = me.shape_points + me.play_rock_paper_scissors(other)
        total += round_total

    return total
