import unittest
import zsur.kmeans as kmeans


class TestClusterLevels(unittest.TestCase):

    def setUp(self):
        self.data = [(0, 1), (2, 1), (1, 3), (1, -1), (1, 5), (1, 9), (-1, 7), (3, 7)]

    def test_chainmap(self):
        result = kmeans.kmeans(self.data, 3)
        expect = {(1, 1): [(0, 1), (2, 1), (1, 3), (1, -1)], (1, 7): [(1, 5), (1, 9), (-1, 7), (3, 7)]}
        self.assertEqual(result, expect)


if __name__ == '__main__':
    unittest.main()
