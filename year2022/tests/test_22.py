import importlib
import unittest

import runner


class Test22(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        day = "22"
        year = "2022"
        cls.day = day
        cls.data = runner.get_data(day, year, True)
        formatted_day = runner.format_filename(day)
        formatted_year = runner.format_year(year)
        cls.mod = importlib.import_module(f"{formatted_year}.{formatted_day}.{formatted_day}")

    def test_part1(self):
        self.assertEqual(runner.run_part("1_test", self.mod, self.data), 6032)

#     def test_part2(self):
#         self.assertEqual(runner.run_part("2_test", self.mod, self.data), 5031)


if __name__ == '__main__':
    unittest.main()
