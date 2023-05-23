import unittest

from synchronous_shopping import (
    shop,
)


class TestShop(unittest.TestCase):
    @unittest.expectedFailure
    def test_sample_test_case_0(self):
        self.assertEqual(
            shop(
                n=5,
                k=5,
                centers=[
                    '1 1',
                    '1 2',
                    '1 3',
                    '1 4',
                    '1 5',
                ],
                roads=[
                    [1, 2, 10],
                    [1, 3, 10],
                    [2, 4, 10],
                    [3, 5, 10],
                    [4, 5, 10],
                ],
            ),
            31)

    @unittest.expectedFailure
    def test_sample_test_case_1(self):
        self.assertEqual(
            shop(
                n=6,
                k=3,
                centers=[
                    '2 1 2',
                    '1 3',
                    '0',
                    '2 1 3',
                    '1 2',
                    '1 3',
                ],
                roads=[
                    [1, 2, 572],
                    [4, 2, 913],
                    [2, 6, 220],
                    [1, 3, 579],
                    [2, 3, 808],
                    [5, 3, 298],
                    [6, 1, 927],
                    [4, 5, 171],
                    [1, 5, 671],
                    [2, 5, 463],
                ],
            ),
            792)


if __name__ == '__main__':
    unittest.main()
