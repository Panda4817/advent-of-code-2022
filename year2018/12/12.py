def get_state(data):
    lst = data.split("\n")
    # Parse initial state
    # e.g. "initial state: #..#." => we only need the part after the 3rd token
    state_str = lst[0].split()[2]
    state = [0 if c == "." else 1 for c in state_str]

    # Index set for positions in the initial state that have a plant (#)
    index = {i for i, val in enumerate(state) if val == 1}

    # We'll store rules in standard Python lists (instead of blist).
    rules_with_plant = []
    rules_without_plant = []

    # Parse the rules
    # e.g. "###.. => #" or "..#.# => ."
    for line in lst[2:]:
        parts = line.split(" => ")
        if len(parts) < 2:
            continue
        pattern, result = parts[0], parts[1]

        # If result is ".", skip building a rule—no new plant grows
        if result == ".":
            continue

        # Build a rule (list of offsets where '#' appears)
        # For pattern "##.#.", the offsets are [-2, -1, 1] if we use x = -2..+2
        rule = []
        x = -2
        for char in pattern:
            if char == "#":
                rule.append(x)
            x += 1

        # If the center (offset 0) is in that rule, it means
        # "If the pot itself had a plant, it remains planted under these conditions"
        if 0 in rule:
            rules_with_plant.append(rule)
        else:
            rules_without_plant.append(rule)

    return index, rules_with_plant, rules_without_plant


def print_gen(state, min_index, max_index, gen):
    print(gen, end=" ")
    for i in range(min_index - 2, max_index + 3):
        if i in state:
            print("#", end="")
        else:
            print(".", end="")
    print()


def part1(data):
    state, rules_with, rules_without = get_state(data)
    generation = 0

    # Part 1 threshold
    total_gens = 102  # after this, the pattern shifts in a predictable way

    # Part 2 target
    gens = 50000000000

    min_index = min(state)
    max_index = max(state)
    # print_gen(state, min_index, max_index, generation)

    while generation != total_gens:
        if generation == 20:
            print("part 1: " + str(sum(state)))  # part 1
        new_state = set()
        # Build a set of indexes that currently have no plant
        not_in_state = set(range(min_index - 2, max_index + 3)) - state

        # Check positions that currently have a plant
        for i in state:
            for rule in rules_with:
                # We check offsets [-2, -1, 0, 1, 2]
                for c in [-2, -1, 0, 1, 2]:
                    n = i + c
                    # If (c not in rule but n is in state) => mismatch
                    # or (c in rule but n not in state) => mismatch
                    if (c not in rule and n in state) or (c in rule and n not in state):
                        break
                else:
                    # If we didn't break, the pattern matched
                    new_state.add(i)
                    break

        # Check positions that currently have no plant
        for i in not_in_state:
            for rule in rules_without:
                # Notice we skip '0' offset because that would contradict
                # "rule with plant" logic. We only look at [-2, -1, 1, 2].
                for c in [-2, -1, 1, 2]:
                    n = i + c
                    if (c not in rule and n in state) or (c in rule and n not in state):
                        break
                else:
                    new_state.add(i)
                    # Update min/max indexes if needed
                    if i < min_index:
                        min_index = i
                    if i > max_index:
                        max_index = i
                    break

        state = new_state
        generation += 1
        # print_gen(state, min_index, max_index, generation)

    # After total_gens, the pattern "shifts" at a constant rate
    left_over = gens - total_gens
    final_state = set()
    for i in state:
        final_state.add(i + left_over)

    return sum(final_state)  # Part 2 result.
