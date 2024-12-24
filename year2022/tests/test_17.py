import importlib
import unittest

import runner


class Test17(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        day = "17"
        year = "2022"
        cls.day = day
        cls.data = runner.get_data(day, year, True)
        formatted_day = runner.format_filename(day)
        formatted_year = runner.format_year(year)
        cls.mod = importlib.import_module(f"{formatted_year}.{formatted_day}.{formatted_day}")

    def test_part1(self):
        self.assertEqual(runner.run_part("1", self.mod, self.data), 3068)

#     def test_part2(self):
#         self.assertEqual(runner.run_part("2", self.mod, self.data), 1514285714288)


if __name__ == '__main__':
    unittest.main()
