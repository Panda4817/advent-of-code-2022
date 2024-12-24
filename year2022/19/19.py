import concurrent.futures
import copy

max_vals = {i: {"max_geodes": 0, "max_geode_robots": 0, "max_geode_robot_per_time": {j: 0 for j in range(2, 24)}} for i in range(1, 31)}

class Node(object):

    def __init__(self, number, costs, max_robots, robots, resources, time):
        self.robots = robots
        self.resources = resources
        self.time = time
        self.number = number
        self.costs = costs
        self.max_robots = max_robots
        self.children = []
        self.make_children()
        # print(self)

    def __str__(self):
        return f"<blueprint={self.number}, robots={self.robots}, resources={self.resources}>"

    def make_children(self):
        global max_vals
        # print(self, max_quality, self.time)
        # print(self)
        if self.time == 24:
            q = self.resources[3] * self.number
            if self.resources[3] > max_vals[self.number]["max_geodes"]:
                max_vals[self.number]["max_geodes"] = self.resources[3]
            if self.robots[3] > max_vals[self.number]["max_geode_robots"]:
                max_vals[self.number]["max_geode_robots"] = self.robots[3]
            print(self, max_vals[self.number]["max_geodes"], self.time)
            return

        # total_robots = sum(self.robots)
        if max_vals[self.number]["max_geode_robot_per_time"][self.time] > self.robots[3]:
            return
        else:
            max_vals[self.number]["max_geode_robot_per_time"][self.time] = self.robots[3]

        new_time = self.time + 1
        remaining = 24 - new_time

        if remaining == 1 and self.robots[3] < max_vals[self.number]["max_geode_robots"]:
            return

        new_resources = [self.resources[i] + self.robots[i] for i in range(0, 4)]
        new_robots = copy.deepcopy(self.robots)

        if remaining > 1:
            # States where something is bought
            for resource in range(3, -1, -1):
                if resource < 3 and self.robots[resource] >= self.max_robots[resource]:
                    continue

                can_buy_it = can_buy(resource, self.costs, self.resources)

                if can_buy_it:
                    new_resources_after_buying = copy.deepcopy(new_resources)
                    new_robots_after_buying = copy.deepcopy(new_robots)
                    for k, a in self.costs[resource].items():
                        new_resources_after_buying[k] -= a
                    new_robots_after_buying[resource] += 1

                    upper_bound = (new_resources_after_buying[3] + sum(new_robots_after_buying[3] + i for i in range(0, remaining)))
                    if upper_bound > max_vals[self.number]["max_geodes"]:
                        child_node = Node(self.number, self.costs, self.max_robots, new_robots_after_buying, new_resources_after_buying, new_time)
                        self.children.append(child_node)

                    if resource == 3:
                        break

        # state where nothing is bought
        upper_bound = (new_resources[3] + sum(new_robots[3] + i for i in range(0, remaining)))
        if upper_bound > max_vals[self.number]["max_geodes"]:
            child_node = Node(self.number, self.costs, self.max_robots, new_robots, new_resources, new_time)
            self.children.append(child_node)


def get_currency(word):
    if word == "ore":
        currency = 0
    elif word == "clay":
        currency = 1
    elif word == "obsidian.":
        currency = 2
    else:
        currency = 3

    return currency


def process_data(data):
    lines = [line for line in data.split("\n")]
    blueprints = {}
    for line in lines:
        costs = {}
        parts = line.split(": ")
        number = int(parts[0].split()[1])
        cost_strings = parts[1].split(". ")
        buying = 0
        ore = []
        clay = []
        ob = []
        for s in cost_strings:
            p = s.split()
            amount_one = int(p[4])
            currency_word_one = p[5]
            currency_one = get_currency(currency_word_one)
            costs[buying] = {currency_one: amount_one}
            if currency_one == 0:
                ore.append(amount_one)
            if currency_one == 1:
                clay.append(amount_one)
            if currency_one == 2:
                ob.append(amount_one)
            if p[1] == "obsidian" or p[1] == "geode":
                amount_two = int(p[7])
                currency_word_two = p[8]
                currency_two = get_currency(currency_word_two)
                costs[buying][currency_two] = amount_two
                if currency_two == 0:
                    ore.append(amount_two)
                if currency_two == 1:
                    clay.append(amount_two)
                if currency_two == 2:
                    ob.append(amount_two)

            buying += 1

        blueprints[number] = {"costs": costs, "max_robots": [max(ore), max(clay), max(ob)]}

    return blueprints


def can_buy(i, costs, new_resources):
    can_buy = True
    if i == 0 or i == 1:
        if new_resources[0] < costs[i][0]:
            can_buy = False
    if i == 2:
        if new_resources[0] < costs[i][0] or new_resources[1] < costs[i][1]:
            can_buy = False

    if i == 3:
        if new_resources[0] < costs[i][0] or new_resources[2] < costs[i][2]:
            can_buy = False

    return can_buy


def do_work_part1(number, val):
    Node(number, val["costs"], val["max_robots"], [1, 0, 0, 0], [2, 0, 0, 0], 2)
    global max_vals
    q = max_vals[number]["max_geodes"] * number
    print(number, q)
    return q


# Same code for part1 and part2
def part1(data):
    # Time limit is 24
    blueprints = process_data(data)
    quality_levels = []

    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        futures = set()
        for number, val in blueprints.items():
            futures.add(executor.submit(do_work_part1, number=number, val=val))
        for future in concurrent.futures.as_completed(futures):
            quality_levels.append(future.result())

    return sum(quality_levels)


def part2(data):
    # Time limit is 32
    pass
