
def process_data(data):
    lines = [i.split() for i in data.split("\n")]
    all_dirs = {"dirs": {}, "files": {}, "size": 0}

    previous = []
    where = all_dirs
    for line in lines:
        if line[0] == "$" and line[1] == "cd":
            if line[2] == "/":
                where = all_dirs
                continue

            if line[2] != "/" and line[2] != "..":
                previous.append(where)
                where = where["dirs"][line[2]]
                continue

            if line[2] == "..":
                prev = previous.pop()
                prev["size"] += where["size"]
                where = prev
                continue

        if line[0] == "$" and line[1] == "ls":
            continue

        if line[0] == "dir":
            where["dirs"][line[1]] = {"dirs": {}, "files": {}, "size": 0}
            continue

        size = int(line[0])
        file_name = line[1]
        where["files"][file_name] = size
        where["size"] += size

    while previous:
        prev = previous.pop()
        prev["size"] += where["size"]
        where = prev

    return all_dirs


def part1(data):
    file_system = process_data(data)

    sum = 0
    q = [file_system]
    while q:
        current = q.pop(0)
        if current["size"] <= 100000:
            sum += current["size"]

        for dir in current["dirs"]:
            q.append(current["dirs"][dir])

    return sum


def part2(data):
    file_system = process_data(data)
    disk_space = 70000000
    unused_space = 30000000
    free_space = disk_space - file_system["size"]
    need_to_free = unused_space - free_space

    possible_to_delete = {}
    q = [["/", file_system]]
    while q:
        dir_name, current = q.pop(0)
        if current["size"] >= need_to_free:
            possible_to_delete[dir_name] = current["size"]

        for dir in current["dirs"]:
            q.append([dir, current["dirs"][dir]])

    return min(possible_to_delete.values())
