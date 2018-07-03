import unittest
import zsur.kmeans as kmeans


class TestClusterLevels(unittest.TestCase):

    def setUp(self):
        self.data = [(0, 1), (2, 1), (1, 3), (1, -1), (1, 5), (1, 9), (-1, 7), (3, 7)]

    def test_kmeans(self):
        result = kmeans.kmeans(self.data, 3)
        expect = {(1, 1): [(0, 1), (2, 1), (1, 3), (1, -1)], (1, 7): [(1, 5), (1, 9), (-1, 7), (3, 7)]}
        self.assertEqual(result, expect)

    def test_a_criterion(self):
        result1 = kmeans.a_criterions((0, 0), (3, 0), 1, 2)
        self.assertEqual(result1, 4.5)
        result2 = kmeans.a_criterions((0, 0), (0, 2), 2, 1)
        self.assertEqual(result2, 8)


if __name__ == '__main__':
    unittest.main()
