import unittest
import zsur.cluster_levels as clusterlvls


class TestClusterLevels(unittest.TestCase):

    def setUp(self):
        self.data = [(-3, 1), (1, 1), (-2, 0), (3, -3), (1, 2), (-2, -1)]

    def test_chainmap(self):
        result = clusterlvls.cluster_levels(self.data, 1.9)
        self.assertEqual(result, 3)

    def test_distanc(self):
        result = clusterlvls.distanc((1, 3), (1, 4))
        self.assertEqual(result, 1)
        result = clusterlvls.distanc((20, -15), (20, -15))
        self.assertEqual(result, 0)
        self.assertRaises(Exception, clusterlvls.distanc, (0, 0), (1, 1, 1))  # vectors don't have same length
        self.assertRaises(Exception, clusterlvls.distanc, (1, 0))  # not enough input arguments
        self.assertRaises(Exception, clusterlvls.distanc, (1, 0), (2, 5), (-9, 18))  # too many input arguments


if __name__ == '__main__':
    unittest.main()
