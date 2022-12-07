import importlib
import pathlib
from typing import Any


def format_filename(day: str):
    return day.zfill(2)


def run_part(part: str, mod: Any, data: str):
    funcname = f'part{part}'
    f = getattr(mod, funcname, None)
    if callable(f):
        print(f"Running Part {part}")
        val = f(data)
        print(f"Output: {val}")
        return val
    else:
        print(f"No {funcname} function")
        return


def get_data(day, test=False):
    # Try to find the filename
    day_module = format_filename(day)
    fname = str(pathlib.Path(__file__).parent.absolute()) + \
        "/" + day_module + "/" + day_module

    if test:
        fname += ".test.txt"
    else:
        fname += ".txt"

    try:
        with open(fname, "r") as f:
            data = f.read()
    except Exception as e:
        raise ValueError(f"Unable to read file {fname}") from e

    print(f"Loaded puzzle input from {fname}")
    print()
    return data


def run(day, year=2022):
    print(f"AOC {year} Day {day}")

    formatted_day = format_filename(day)
    module = importlib.import_module(f"{formatted_day}.{formatted_day}")
    data = get_data(day)
    run_part("1", module, data)
    print()
    run_part("2", module, data)
    print()
