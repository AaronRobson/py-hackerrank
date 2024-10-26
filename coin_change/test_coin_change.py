import unittest

from coin_change import (
    get_ways,
)


class TestGetWays(unittest.TestCase):
    def test_find_zero_in_nothing(self):
        self.assertEqual(
            get_ways(0, []),
            1,
        )

    def test_find_zero_in_ones(self):
        self.assertEqual(
            get_ways(0, [1]),
            1,
        )

    def test_find_one_in_nothing(self):
        self.assertEqual(
            get_ways(1, []),
            0,
        )

    def test_one_in_ones(self):
        self.assertEqual(
            get_ways(1, [1]),
            1,
        )

    def test_find_two_in_ones(self):
        self.assertEqual(
            get_ways(2, [1]),
            1,
        )

    def test_find_one_in_twos(self):
        self.assertEqual(
            get_ways(1, [2]),
            0,
        )

    def test_example_1(self) -> None:
        self.assertEqual(
            get_ways(3, [8, 3, 1, 2]),
            3,
        )

    def test_sample_test_case_0(self) -> None:
        self.assertEqual(
            get_ways(4, [1, 2, 3]),
            4,
        )

    def test_sample_test_case_1(self) -> None:
        self.assertEqual(
            get_ways(10, [2, 5, 3, 6]),
            5,
        )
