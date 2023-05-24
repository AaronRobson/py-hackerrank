import unittest
from sys import maxsize

from synchronous_shopping import (
    shop,
    parse_vertices,
    parse_centers,
    Road,
    parse_roads,
    Node,
    dijkstra,
    _find_direct_roads,
    _find_new_node_in_progress,
    find_centers_with_fishes_we_need,
    stop_early_when_all_fish_are_found,
    all_splits_in_two,
)


class TestShop(unittest.TestCase):
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
            30)

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


class TestParseVertices(unittest.TestCase):
    def test(self):
        self.assertEqual(
            parse_vertices(5),
            (1, 2, 3, 4, 5),
        )


class TestParseCenters(unittest.TestCase):
    def test_sample_test_case_0(self):
        self.assertEqual(
            parse_centers([
                '1 1',
                '1 2',
                '1 3',
                '1 4',
                '1 5',
            ]),
            {
                1: {1},
                2: {2},
                3: {3},
                4: {4},
                5: {5},
            })

    def test_sample_test_case_1(self):
        self.assertEqual(
            parse_centers([
                '2 1 2',
                '1 3',
                '0',
                '2 1 3',
                '1 2',
                '1 3'
            ]),
            {
                1: {1, 2},
                2: {3},
                3: set(),
                4: {1, 3},
                5: {2},
                6: {3},
            })


class TestParseRoads(unittest.TestCase):
    def test_sample_test_case_0(self):
        self.assertEqual(
            parse_roads([
                [1, 2, 10],
                [1, 3, 10],
                [2, 4, 10],
                [3, 5, 10],
                [4, 5, 10],
            ]),
            (
                Road(route={1, 2}, cost=10),
                Road(route={1, 3}, cost=10),
                Road(route={2, 4}, cost=10),
                Road(route={3, 5}, cost=10),
                Road(route={4, 5}, cost=10),
            ),
        )

    def test_sample_test_case_1(self):
        self.maxDiff = None
        self.assertEqual(
            parse_roads([
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
            ]),
            (
                Road(route={1, 2}, cost=572),
                Road(route={4, 2}, cost=913),
                Road(route={2, 6}, cost=220),
                Road(route={1, 3}, cost=579),
                Road(route={2, 3}, cost=808),
                Road(route={5, 3}, cost=298),
                Road(route={6, 1}, cost=927),
                Road(route={4, 5}, cost=171),
                Road(route={1, 5}, cost=671),
                Road(route={2, 5}, cost=463),
            ))


class TestDijkstra(unittest.TestCase):
    def test_sample_test_case_0(self):
        self.assertEqual(
            dijkstra(
                vertices=(1, 2, 3, 4, 5),
                edges=(
                    Road(route={1, 2}, cost=10),
                    Road(route={1, 3}, cost=10),
                    Road(route={2, 4}, cost=10),
                    Road(route={3, 5}, cost=10),
                    Road(route={4, 5}, cost=10),
                ),
                from_=1),
            {
                1: 0,
                2: 10,
                3: 10,
                4: 20,
                5: 20,
            })


class TestNode(unittest.TestCase):
    def test(self):
        a = Node()
        self.assertEqual(a.latest_cost, maxsize)
        self.assertEqual(a.explored, False)
        a.latest_cost = 5
        a.explored = True
        self.assertEqual(a.latest_cost, 5)
        self.assertEqual(a.explored, True)


class TestFindDirectRoads(unittest.TestCase):
    def test_sample_test_case_0(self):
        self.assertEqual(
            _find_direct_roads(
                edges=(
                    Road(route={1, 2}, cost=10),
                    Road(route={1, 3}, cost=10),
                    Road(route={2, 4}, cost=10),
                    Road(route={3, 5}, cost=10),
                    Road(route={4, 5}, cost=10),
                ),
                from_=1,
            ),
            {
                2: 10,
                3: 10,
            })


class TestFindNewNodeInProgress(unittest.TestCase):
    def test_initial(self):
        self.assertEqual(
            _find_new_node_in_progress(
                {
                    1: Node(latest_cost=0),
                    2: Node(),
                    3: Node(),
                }
            ),
            1,
        )

    def test_one_possible(self):
        self.assertEqual(
            _find_new_node_in_progress(
                {
                    1: Node(latest_cost=0, explored=True),
                    2: Node(latest_cost=10),
                    3: Node(),
                }
            ),
            2,
        )

    def test_two_possible(self):
        self.assertIn(
            _find_new_node_in_progress(
                {
                    1: Node(latest_cost=0, explored=True),
                    2: Node(latest_cost=10),
                    3: Node(latest_cost=10),
                }
            ),
            [2, 3],
        )


class TestFindCentersWithFishesWeNeed(unittest.TestCase):
    def test_sample_test_case_0(self):
        self.assertEqual(
            find_centers_with_fishes_we_need(
                centers={
                    1: {1},
                    2: {2},
                    3: {3},
                    4: {4},
                    5: {5},
                },
                fishes_we_need={2, 3, 4},
            ),
            {
                2: {2},
                3: {3},
                4: {4},
            },
        )

    def test_sample_test_case_1(self):
        self.maxDiff = None
        self.assertEqual(
            find_centers_with_fishes_we_need(
                centers={
                    1: {1, 2},
                    2: {3},
                    3: set(),
                    4: {1, 3},
                    5: {2},
                    6: {3},
                },
                fishes_we_need=set(),
            ),
            {})


class TestStopEarlyWhenAllFishAreFound(unittest.TestCase):
    def test_sample_test_case_0(self):
        self.assertEqual(
            stop_early_when_all_fish_are_found(
                centers_permutation=(
                    (2, {2}),
                    (3, {3}),
                    (4, {4}),
                ),
                fishes_we_need={2, 3, 4},
            ),
            (2, 3, 4))

    def test_sample_test_case_1(self):
        self.assertEqual(
            stop_early_when_all_fish_are_found(
                centers_permutation=(
                    (1, {1, 2}),
                    (2, {3}),
                    (3, set()),
                    (4, {1, 3}),
                    (5, {2}),
                    (6, {3}),
                ),
                fishes_we_need=set(),
            ),
            tuple())


class TestAllSplitsInTwo(unittest.TestCase):
    def test_sample_test_case_0(self):
        self.assertEqual(
            all_splits_in_two(centers=(2, 3, 4)),
            (
                (tuple(), (2, 3, 4)),
                ((2,), (3, 4)),
                ((2, 3), (4,)),
                ((2, 3, 4), tuple()),
            ))

    def test_empty(self):
        self.assertEqual(
            all_splits_in_two(centers=tuple()),
            (
                tuple([tuple(), tuple()]),
            ))

    def test_one(self):
        self.assertEqual(
            all_splits_in_two(centers=(42,)),
            (
                tuple([tuple(), (42,)]),
                tuple([(42,), tuple()]),
            ))

    def test_two(self):
        self.assertEqual(
            all_splits_in_two(centers=(42, 43)),
            (
                tuple([tuple(), (42, 43)]),
                tuple([(42,), (43,)]),
                tuple([(42, 43), tuple()]),
            ))
