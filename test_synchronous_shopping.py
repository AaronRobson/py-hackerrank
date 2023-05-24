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

    def test_case_6(self):
        '''
        50 100 7
        0
        1 3
        3 4 5 7
        0
        0
        0
        0
        0
        1 4
        2 3 5
        1 3
        0
        0
        0
        2 3 4
        0
        0
        0
        1 3
        0
        0
        0
        1 5
        1 3
        1 3
        0
        1 1
        1 5
        0
        1 3
        1 1
        2 2 6
        0
        1 5
        0
        0
        0
        0
        1 4
        1 7
        0
        1 5
        0
        0
        1 3
        0
        0
        0
        0
        1 4
        34 42 44
        20 15 1000
        44 31 375
        30 14 504
        13 6 734
        39 45 968
        9 20 497
        47 37 568
        17 41 916
        15 8 361
        44 25 535
        45 24 424
        36 26 396
        29 25 916
        24 32 156
        33 9 591
        39 37 779
        5 30 482
        36 7 198
        49 1 169
        21 6 452
        12 2 529
        1 14 31
        29 31 400
        12 22 435
        35 10 972
        39 9 883
        8 13 75
        14 13 346
        43 34 21
        3 2 262
        14 15 30
        23 9 239
        48 28 275
        31 34 867
        10 5 78
        37 46 553
        16 39 258
        15 25 410
        10 17 124
        31 45 429
        42 28 837
        2 1 349
        3 30 317
        2 24 688
        32 36 870
        14 38 270
        21 26 110
        27 15 668
        9 6 966
        45 20 316
        9 11 207
        27 10 268
        3 43 949
        26 8 550
        46 47 283
        26 40 874
        23 2 356
        43 18 365
        34 20 269
        4 19 590
        35 17 894
        32 21 314
        47 17 816
        45 11 176
        36 45 413
        16 10 963
        28 1 528
        7 4 687
        49 5 801
        15 24 121
        8 5 464
        18 2 713
        35 1 939
        5 4 755
        48 50 251
        33 14 517
        1 22 666
        12 11 97
        30 11 7
        31 43 904
        43 22 660
        31 17 976
        28 38 219
        4 2 972
        27 9 754
        6 5 351
        16 38 952
        36 46 225
        40 8 243
        35 32 502
        46 14 181
        1 4 723
        30 21 854
        26 32 802
        19 37 906
        46 26 902
        49 21 173
        7 28 819
        22 41 526

        Should result in:

        2868
        '''
        n = 50
        road_count = 100
        k = 7
        centers = [
            '0',
            '1 3',
            '3 4 5 7',
            '0',
            '0',
            '0',
            '0',
            '0',
            '1 4',
            '2 3 5',
            '1 3',
            '0',
            '0',
            '0',
            '2 3 4',
            '0',
            '0',
            '0',
            '1 3',
            '0',
            '0',
            '0',
            '1 5',
            '1 3',
            '1 3',
            '0',
            '1 1',
            '1 5',
            '0',
            '1 3',
            '1 1',
            '2 2 6',
            '0',
            '1 5',
            '0',
            '0',
            '0',
            '0',
            '1 4',
            '1 7',
            '0',
            '1 5',
            '0',
            '0',
            '1 3',
            '0',
            '0',
            '0',
            '0',
            '1 4',
        ]
        roads = [
            [34, 42, 44],
            [20, 15, 1000],
            [44, 31, 375],
            [30, 14, 504],
            [13, 6, 734],
            [39, 45, 968],
            [9, 20, 497],
            [47, 37, 568],
            [17, 41, 916],
            [15, 8, 361],
            [44, 25, 535],
            [45, 24, 424],
            [36, 26, 396],
            [29, 25, 916],
            [24, 32, 156],
            [33, 9, 591],
            [39, 37, 779],
            [5, 30, 482],
            [36, 7, 198],
            [49, 1, 169],
            [21, 6, 452],
            [12, 2, 529],
            [1, 14, 31],
            [29, 31, 400],
            [12, 22, 435],
            [35, 10, 972],
            [39, 9, 883],
            [8, 13, 75],
            [14, 13, 346],
            [43, 34, 21],
            [3, 2, 262],
            [14, 15, 30],
            [23, 9, 239],
            [48, 28, 275],
            [31, 34, 867],
            [10, 5, 78],
            [37, 46, 553],
            [16, 39, 258],
            [15, 25, 410],
            [10, 17, 124],
            [31, 45, 429],
            [42, 28, 837],
            [2, 1, 349],
            [3, 30, 317],
            [2, 24, 688],
            [32, 36, 870],
            [14, 38, 270],
            [21, 26, 110],
            [27, 15, 668],
            [9, 6, 966],
            [45, 20, 316],
            [9, 11, 207],
            [27, 10, 268],
            [3, 43, 949],
            [26, 8, 550],
            [46, 47, 283],
            [26, 40, 874],
            [23, 2, 356],
            [43, 18, 365],
            [34, 20, 269],
            [4, 19, 590],
            [35, 17, 894],
            [32, 21, 314],
            [47, 17, 816],
            [45, 11, 176],
            [36, 45, 413],
            [16, 10, 963],
            [28, 1, 528],
            [7, 4, 687],
            [49, 5, 801],
            [15, 24, 121],
            [8, 5, 464],
            [18, 2, 713],
            [35, 1, 939],
            [5, 4, 755],
            [48, 50, 251],
            [33, 14, 517],
            [1, 22, 666],
            [12, 11, 97],
            [30, 11, 7],
            [31, 43, 904],
            [43, 22, 660],
            [31, 17, 976],
            [28, 38, 219],
            [4, 2, 972],
            [27, 9, 754],
            [6, 5, 351],
            [16, 38, 952],
            [36, 46, 225],
            [40, 8, 243],
            [35, 32, 502],
            [46, 14, 181],
            [1, 4, 723],
            [30, 21, 854],
            [26, 32, 802],
            [19, 37, 906],
            [46, 26, 902],
            [49, 21, 173],
            [7, 28, 819],
            [22, 41, 526],
        ]
        self.assertEqual(
            len(centers),
            n)
        self.assertEqual(
            len(roads),
            road_count)
        self.assertEqual(
            shop(
                n=n,
                k=k,
                centers=centers,
                roads=roads),
            2868)


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
            list(stop_early_when_all_fish_are_found(
                centers_permutation=(
                    (2, {2}),
                    (3, {3}),
                    (4, {4}),
                ),
                fishes_we_need={2, 3, 4},
            )),
            [2, 3, 4])

    def test_sample_test_case_1(self):
        self.assertEqual(
            list(stop_early_when_all_fish_are_found(
                centers_permutation=(
                    (1, {1, 2}),
                    (2, {3}),
                    (3, set()),
                    (4, {1, 3}),
                    (5, {2}),
                    (6, {3}),
                ),
                fishes_we_need=set(),
            )),
            [])


class TestAllSplitsInTwo(unittest.TestCase):
    def test_sample_test_case_0(self):
        self.assertEqual(
            list(all_splits_in_two(centers=(2, 3, 4))),
            [
                (tuple(), (2, 3, 4)),
                ((2,), (3, 4)),
                ((2, 3), (4,)),
                ((2, 3, 4), tuple()),
            ])

    def test_empty(self):
        self.assertEqual(
            list(all_splits_in_two(centers=tuple())),
            [
                (tuple(), tuple()),
            ])

    def test_one(self):
        self.assertEqual(
            list(all_splits_in_two(centers=(42,))),
            [
                (tuple(), (42,)),
                ((42,), tuple()),
            ])

    def test_two(self):
        self.assertEqual(
            list(all_splits_in_two(centers=(42, 43))),
            [
                (tuple(), (42, 43)),
                ((42,), (43,)),
                ((42, 43), tuple()),
            ])


if __name__ == '__main__':
    unittest.main()
