import unittest

from coin_change import (
    get_ways,
)


class TestGetWays(unittest.TestCase):
    def test_find_zero_in_nothing(self) -> None:
        self.assertEqual(
            get_ways(0, []),
            1,
        )

    def test_find_zero_in_ones(self) -> None:
        self.assertEqual(
            get_ways(0, [1]),
            1,
        )

    def test_find_one_in_nothing(self) -> None:
        self.assertEqual(
            get_ways(1, []),
            0,
        )

    def test_one_in_ones(self) -> None:
        self.assertEqual(
            get_ways(1, [1]),
            1,
        )

    def test_find_two_in_ones(self) -> None:
        self.assertEqual(
            get_ways(2, [1]),
            1,
        )

    def test_find_one_in_twos(self) -> None:
        self.assertEqual(
            get_ways(1, [2]),
            0,
        )

    def test_example_1(self) -> None:
        self.assertEqual(
            get_ways(3, [8, 3, 1, 2]),
            3,
        )

    def test_case_0(self) -> None:
        self.assertEqual(
            get_ways(4, [1, 2, 3]),
            4,
        )

    def test_case_1(self) -> None:
        self.assertEqual(
            get_ways(10, [2, 5, 3, 6]),
            5,
        )

    def test_case_2(self) -> None:
        self.assertEqual(
            get_ways(166, [5, 37, 8, 39, 33, 17, 22, 32, 13, 7, 10, 35, 40, 2, 43, 49, 46, 19, 41, 1, 12, 11, 28]),
            96_190_959,
        )

    def test_case_3(self) -> None:
        self.assertEqual(
            get_ways(75, [25, 10, 11, 29, 49, 31, 33, 39, 12, 36, 40, 22, 21, 16, 37, 8, 18, 4, 27, 17, 26, 32, 6, 38, 2, 30, 34]),
            16_694,
        )

    def test_case_4(self) -> None:
        self.assertEqual(
            get_ways(219, [36, 10, 42, 7, 50, 1, 49, 24, 37, 12, 34, 13, 39, 18, 8, 29, 19, 43, 5, 44, 28, 23, 35, 26]),
            168_312_708,
        )

    def test_case_5(self) -> None:
        self.assertEqual(
            get_ways(69, [25, 27, 40, 38, 17, 2, 28, 23, 9, 43, 18, 49, 15, 24, 19, 11, 1, 39, 32, 16, 35, 30, 48, 34, 20, 3, 6, 13, 44]),
            101_768,
        )

    def test_case_6(self) -> None:
        self.assertEqual(
            get_ways(15, [49, 22, 45, 6, 11, 20, 30, 10, 46, 8, 32, 48, 2, 41, 43, 5, 39, 16, 28, 44, 14, 4, 27, 36]),
            10,
        )

    def test_case_7(self) -> None:
        self.assertEqual(
            get_ways(1, [48, 6, 34, 50, 49, 36, 30, 35, 40, 41, 17, 43, 39, 13, 4, 20, 19, 2, 46, 7, 38, 33, 28, 18, 21]),
            0,
        )

    def test_case_8(self) -> None:
        self.assertEqual(
            get_ways(2, [44, 5, 9, 39, 6, 25, 3, 28, 16, 19, 4, 49, 40, 22, 2, 12, 45, 33, 23, 42, 34, 15, 46, 26, 13, 31, 8]),
            1,
        )

    def test_case_9(self) -> None:
        self.assertEqual(
            get_ways(250, [41, 34, 46, 9, 37, 32, 42, 21, 7, 13, 1, 24, 3, 43, 2, 23, 8, 45, 19, 30, 29, 18, 35, 11]),
            15_685_693_751,
        )

    def test_case_10(self) -> None:
        self.assertEqual(
            get_ways(250, [8, 47, 13, 24, 25, 31, 32, 35, 3, 19, 40, 48, 1, 4, 17, 38, 22, 30, 33, 15, 44, 46, 36, 9, 20, 49]),
            3_542_323_427,
        )

    def test_case_11(self) -> None:
        self.assertEqual(
            get_ways(179, [24, 6, 48, 27, 36, 22, 35, 15, 41, 1, 26, 25, 4, 8, 14, 20, 9, 38, 34, 40, 45, 17, 33, 19, 5, 43, 2]),
            1_283_414_971,
        )

    def test_case_12(self) -> None:
        self.assertEqual(
            get_ways(18, [49, 9, 40, 17, 46, 24, 42, 26, 43, 41, 35, 1, 47, 28, 20, 38, 2, 44, 32, 22, 18, 45, 25]),
            18,
        )

    def test_case_13(self) -> None:
        self.assertEqual(
            get_ways(85, [50, 10, 17, 21, 8, 3, 12, 41, 9, 13, 43, 37, 49, 19, 23, 28, 45, 46, 29, 16, 34, 25, 2, 22, 1]),
            370_927,
        )

    def test_case_14(self) -> None:
        self.assertEqual(
            get_ways(245, [16, 30, 9, 17, 40, 13, 42, 5, 25, 49, 7, 23, 1, 44, 4, 11, 33, 12, 27, 2, 38, 24, 28, 32, 14, 50]),
            64_027_917_156,
        )

    def test_case_15(self) -> None:
        self.assertEqual(
            get_ways(240, [23, 20, 35, 42, 19, 3, 34, 9, 28, 38, 13, 41, 26, 14, 27, 39, 24, 37, 46, 29, 43, 1, 21]),
            127_101_770,
        )

    def test_case_16(self) -> None:
        self.assertEqual(
            get_ways(222, [3, 25, 34, 38, 26, 42, 16, 10, 15, 50, 39, 44, 36, 29, 22, 43, 20, 27, 9, 30, 47, 13, 40, 33]),
            5_621_927,
        )
