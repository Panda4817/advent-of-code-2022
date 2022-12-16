
import heapq
from itertools import product


class Tunnel:
    def __init__(self, name, valve_rate, tunnels):
        self.name = name
        self.valve_rate = valve_rate
        self.lead_to = tunnels

    def __str__(self):
        return f"{self.name}<rate={self.valve_rate}, leads_to={self.lead_to}>"


def process_data(data):
    lines = [line.split("; ") for line in data.split("\n")]
    tunnels = {}
    for line in lines:
        parts = line[0].split()
        name = parts[1]
        rate = int(parts[-1].split("=")[1])
        try:
            lead_to = line[1].split(" valves ")[1].split(", ")
        except IndexError:
            lead_to = line[1].split(" valve ")[1].split(", ")
        tunnels[name] = Tunnel(name, rate, lead_to)

    return tunnels


def get_heuristic(total_gas_vented, steps, max_flow, max_time):
    return -1 * (total_gas_vented + (max_flow * (max_time - steps)))


def get_heuristic_part2(total_gas_vented, steps, max_flow, max_time, flow_rate_opened_valves_new):
    # return total_gas_vented / steps
    return max_flow-flow_rate_opened_valves_new
    # return (total_gas_vented + (max_flow * (max_time - steps)))
    # return (total_gas_vented + (max_flow * (max_time - steps))) + extra_to_add
    # return -1 * ((total_gas_vented + extra_to_add) // steps)


def is_valid(open_valves, gas_vented, combo, visited, new_steps, max_flow_rate, max_time, max_vented,
             flow_rate_opened_valves_new, valves_to_open):
    valve_key_string = "".join(sorted(list(open_valves)))
    key1 = combo[0] + combo[1] + valve_key_string
    key2 = combo[1] + combo[0] + valve_key_string

    r = max_time - new_steps
    heuristic = (max_flow_rate-flow_rate_opened_valves_new) / (gas_vented + (max_flow_rate * r))
    # heuristic = (gas_vented + (max_flow_rate * (max_time - new_steps)))
    potential_flow_rate_left = heuristic + new_steps
    # valves_left_to_open = valves_to_open - len(open_valves)
    if (key1 in visited and visited[key1] > potential_flow_rate_left) \
            or (key2 in visited and visited[key2] > potential_flow_rate_left) \
            or (key1 not in visited and key2 not in visited):

        # if ((gas_vented + (max_flow_rate * (max_time - new_steps))) / max_time) > (max_vented / max_time):
        #     return True, potential_flow_rate_left, key1
        # if ((gas_vented + (max_flow_rate * (max_time - new_steps))) / max_time) > (max_vented / max_time):
        # if (gas_vented + (max_flow_rate * r)) > max_vented:

        return True, potential_flow_rate_left, key1

    return False, potential_flow_rate_left, key1


def part2(data):
    tunnels = process_data(data)
    flow_rates = [tunnels[v].valve_rate for v in tunnels if tunnels[v].valve_rate > 0]
    valves_to_open = len(flow_rates)
    max_flow_rate = sum(flow_rates)
    max_time = 26

    total_gas_vented = 0
    steps = 1
    open_valves = set()
    me = ellie = "AA"
    start = (max_flow_rate + 1, (me, ellie, steps, open_valves, total_gas_vented))
    q = [start]

    heapq.heapify(q)
    max_vented = 0

    valve_key_string = "".join(sorted(list(open_valves)))
    key = me + ellie + valve_key_string
    visited = {key: total_gas_vented}

    while q:
        h, (me, ellie, steps, open_valves, total_gas_vented) = heapq.heappop(q)
        # print(h, me, ellie, open_valves, total_gas_vented)
        if steps == max_time:
            if total_gas_vented > max_vented:
                max_vented = total_gas_vented
            continue

        if len(open_valves) == valves_to_open:
            total_gas_vented += (max_flow_rate * (max_time - steps))

            if total_gas_vented > max_vented:
                max_vented = total_gas_vented

            continue

        # print(len(q), steps)
        new_steps = steps + 1
        me_tunnel = tunnels[me]
        ellie_tunnel = tunnels[ellie]
        ellie_open = ellie_tunnel.valve_rate > 0 and ellie not in open_valves
        me_open = me_tunnel.valve_rate > 0 and me not in open_valves
        me_tunnels = me_tunnel.lead_to + [me] if me_open else me_tunnel.lead_to
        same_tunnel = me == ellie
        ellie_tunnels = ellie_tunnel.lead_to + [ellie] if ellie_open and not same_tunnel else ellie_tunnel.lead_to
        combos = list(product(me_tunnels, ellie_tunnels))
        flow_rate_opened_valves = sum([tunnels[t].valve_rate for t in open_valves])
        new_total_gas_vented = flow_rate_opened_valves + total_gas_vented

        for combo in combos:
            new_open_valves = set(open_valves)
            combo_new_total_gas_vented = new_total_gas_vented
            flow_rate_opened_valves_new = flow_rate_opened_valves
            if combo[0] == me:
                new_open_valves.add(me)
                combo_new_total_gas_vented += me_tunnel.valve_rate
                flow_rate_opened_valves_new += me_tunnel.valve_rate

            if combo[1] == ellie:
                new_open_valves.add(ellie)
                combo_new_total_gas_vented += ellie_tunnel.valve_rate
                flow_rate_opened_valves_new += ellie_tunnel.valve_rate

            valid, potential_flow_rate_left, key = is_valid(new_open_valves, combo_new_total_gas_vented, combo, visited,
                                                            new_steps, max_flow_rate, max_time, max_vented,
                                                            flow_rate_opened_valves_new, valves_to_open)

            if valid:
                el = (potential_flow_rate_left,
                      (combo[0], combo[1], new_steps, new_open_valves, combo_new_total_gas_vented))
                heapq.heappush(q, el)
                visited[key] = potential_flow_rate_left

    return max_vented


def part1(data):
    tunnels = process_data(data)
    flow_rates = [tunnels[v].valve_rate for v in tunnels if tunnels[v].valve_rate > 0]
    valves_to_open = len(flow_rates)
    max_flow_rate = sum(flow_rates)
    max_time = 30

    total_gas_vented = 0
    steps = 1
    open_valves = set()
    start = (
        get_heuristic(total_gas_vented, steps, max_flow_rate, max_time), ("AA", steps, open_valves, total_gas_vented))
    q = [start]

    heapq.heapify(q)
    max_vented = 0

    visited = {}

    while q:
        h, (name, steps, open_valves, total_gas_vented) = heapq.heappop(q)
        key = name + str(steps) + "-".join(sorted(list(open_valves)))
        if key in visited and visited[key] >= total_gas_vented:
            continue

        visited[key] = total_gas_vented
        if steps == max_time:
            if total_gas_vented > max_vented:
                max_vented = total_gas_vented
            break

        if len(open_valves) == valves_to_open:
            total_gas_vented += (max_flow_rate * (max_time - steps))
            if total_gas_vented > max_vented:
                max_vented = total_gas_vented
            break

        new_steps = steps + 1
        tunnel = tunnels[name]
        new_total_gas_vented = sum([tunnels[t].valve_rate for t in open_valves]) + total_gas_vented
        heuristic = get_heuristic(new_total_gas_vented, new_steps, max_flow_rate, max_time)

        if tunnel.valve_rate > 0 and name not in open_valves:
            new_open_valves = set(open_valves)
            new_open_valves.add(name)
            new_total_gas_vented_open_valve = new_total_gas_vented + tunnel.valve_rate
            heuristic_open_valve = get_heuristic(new_total_gas_vented_open_valve, new_steps, max_flow_rate, max_time)
            if (-1 * heuristic_open_valve) > max_vented:
                el_open = (heuristic_open_valve, (name, new_steps, new_open_valves, new_total_gas_vented_open_valve))
                heapq.heappush(q, el_open)

        for next_tunnel in tunnel.lead_to:
            if (-1 * heuristic) > max_vented:
                el_move = (heuristic, (next_tunnel, new_steps, open_valves, new_total_gas_vented))
                heapq.heappush(q, el_move)

    return max_vented
