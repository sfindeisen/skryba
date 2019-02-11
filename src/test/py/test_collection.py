#!/usr/bin/python3

import unittest

from collection import DictionaryCollection, ListCollection

class TestCollection(unittest.TestCase):

    def test_empty(self):
        u = ListCollection(None, [])
        self.assertEqual(u.all(), [])

    def test_singleton(self):
        u = ListCollection(None, [5])
        self.assertEqual(u.all(), [5])

    def test_double(self):
        u = ListCollection(None, [5,7])
        self.assertEqual(u.all(), [5,7])

    def test_getitem(self):
        u = ListCollection(None, [5,7])
        self.assertEqual(u[0], 5)
        self.assertEqual(u[1], 7)

    def test_map(self):
        u = ListCollection(None, [5,7]).map(lambda x : 3*x)
        self.assertEqual(u.all(), [15,21])

    def test_reverse_dict(self):
        u = ListCollection(None, [5,7,8]).reverse_dict(lambda x : ["odd"] if (x % 2) else ["even"])
        self.assertTrue(isinstance(u, DictionaryCollection))
        self.assertEqual(u.all(), {"even": [8], "odd": [5,7]})

if __name__ == '__main__':
    unittest.main()
