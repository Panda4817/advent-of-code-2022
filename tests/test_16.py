import importlib
import unittest

import runner


class Test16(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        day = "16"
        cls.day = day
        cls.data = runner.get_data(day, True)
        formatted_day = runner.format_filename(day)
        cls.mod = importlib.import_module(f"{formatted_day}.{formatted_day}")

    def test_part1(self):
        self.assertEqual(runner.run_part("1", self.mod, self.data), 1651)

    def test_part2(self):
        self.assertEqual(runner.run_part("2", self.mod, self.data), 1707)


if __name__ == '__main__':
    unittest.main()
