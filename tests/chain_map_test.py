import unittest
import zsur.chain_map


class TestChainMap(unittest.TestCase):

    def setUp(self):
        self.data = [(-3, 0), (3, 2), (-2, 0), (3, 3), (2, 2), (3, -2), (4, -2), (3, -3)]

    def test_chainmap(self):
        result = zsur.chain_map(self.data, 3.5)
        self.assertEqual(result[2], 3)


if __name__ == '__main__':
    unittest.main()
