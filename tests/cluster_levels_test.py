import unittest
import zsur.cluster_levels as clusterlvls


class TestClusterLevels(unittest.TestCase):

    def setUp(self):
        self.data = [(-3, 1), (1, 1), (-2, 0), (3, -3), (1, 2), (-2, -1)]

    def test_chainmap(self):
        result = clusterlvls.cluster_levels(self.data, 1.9)
        self.assertEqual(result, 3)


if __name__ == '__main__':
    unittest.main()
