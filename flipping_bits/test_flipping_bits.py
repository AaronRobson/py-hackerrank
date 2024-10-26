import unittest

from hypothesis import given
from hypothesis.strategies import integers

from flipping_bits import (
    flipping_bits,
    MIN_UINT_32,
    MAX_UINT_32,
)


class TestRange(unittest.TestCase):
    def test(self) -> None:
        self.assertEqual(
            MAX_UINT_32,
            4_294_967_295)


class TestFlippingBits(unittest.TestCase):
    def test_example_1(self) -> None:
        self.assertEqual(
            flipping_bits(9),
            4_294_967_286,
        )

    def test_min(self) -> None:
        self.assertEqual(
            flipping_bits(MIN_UINT_32),
            MAX_UINT_32,
        )

    def test_max(self) -> None:
        self.assertEqual(
            flipping_bits(MAX_UINT_32),
            MIN_UINT_32,
        )

    def test_under_min(self) -> None:
        with self.assertRaises(ValueError):
            flipping_bits(MIN_UINT_32 - 1)

    def test_over_max(self) -> None:
        with self.assertRaises(ValueError):
            flipping_bits(MAX_UINT_32 + 1)

    @given(n=integers(min_value=MIN_UINT_32, max_value=MAX_UINT_32))
    def test_flipping_bits_is_own_inverse(self, n: int) -> None:
        self.assertEqual(
            flipping_bits(flipping_bits(n)),
            n,
        )
