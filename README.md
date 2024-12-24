# Advent of Code - Python 3

## Create solution
- If this is a new year, add a new module called `year<year_number` e.g. 'year2022'
- Add a file for the day you are completing named `<day_number>.py` under module `<day_number`, which should be under the year module
- For your input data, add a `<day_number>.txt` file (this will be ignored by git)
- Add tests in a submodule called `tests` under the year module
- In the `<day_number>.py` add and implement `part1` and `part2` methods that both take `data` (string value) as an argument

## Run
- ```python main.py -y <year_number> -d <day_number>```
- year_number corresponds to the specific year's puzzle you want to run
- day_number corresponds to the particular day in December that you want to run puzzles for
- Before running, make sure the `<day_number>.txt` file is in the right module

## Test
- ```python -m unittest``` run all tests
- ```python -m unittest year<year_number>/tests/tests_<day_number>.py``` run specific test class

## Requirements

- Python 3.12
- See `requirements.txt` for external libraries