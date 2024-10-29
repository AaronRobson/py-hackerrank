import unittest
from unittest.mock import patch

from kittys_calculations_on_a_tree import (
    Edge,
    Data,
    parse,
    calc,
    ordered_pairs,
    dist,
)

parsed_examples = {
    'example_0': Data(
        n=7,
        q=3,
        edges=[
            Edge(1, 2),
            Edge(1, 3),
            Edge(1, 4),
            Edge(3, 5),
            Edge(3, 6),
            Edge(3, 7),
        ],
        sets=[
            {2, 4},
            {5},
            {2, 4, 5},
        ],
    ),
}


@patch('builtins.input')
class TestParse(unittest.TestCase):
    def test_example_0(self, mock_input) -> None:
        mock_input.side_effect = [
            '7 3',
            '1 2',
            '1 3',
            '1 4',
            '3 5',
            '3 6',
            '3 7',
            '2',
            '2 4',
            '1',
            '5',
            '3',
            '2 4 5',
        ]
        self.assertEqual(
            parse(),
            parsed_examples['example_0'],
        )


class TestCalc(unittest.TestCase):
    def test_example_0(self) -> None:
        self.assertEqual(
            calc(parsed_examples['example_0']),
            [
                16,
                0,
                106,
            ],
        )


class TestOrderedPairs(unittest.TestCase):
    def test_example_0(self) -> None:
        self.assertEqual(
            list(map(ordered_pairs, parsed_examples['example_0'].sets)),
            [
                [
                    (2, 4),
                ],
                [],
                [
                    (2, 4),
                    (2, 5),
                    (4, 5),
                ],
            ],
        )


class TestDist(unittest.TestCase):
    def test_example_0(self) -> None:
        data = parsed_examples['example_0']
        self.assertEqual(
            dist(2, 4, data),
            2)
        self.assertEqual(
            dist(2, 5, data),
            3)
        self.assertEqual(
            dist(4, 5, data),
            3)
