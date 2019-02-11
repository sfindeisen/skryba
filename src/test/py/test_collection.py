#!/usr/bin/python3

import unittest

from collection import DictionaryCollection, ListCollection

class TestListCollection(unittest.TestCase):

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

class TestDictionaryCollection(unittest.TestCase):

    def test_empty(self):
        u = DictionaryCollection(None, {})
        self.assertEqual(u.all(), {})

    def test_singleton(self):
        u = DictionaryCollection(None, {"A": 5})
        self.assertEqual(u.all(), {"A": 5})

    def test_double(self):
        u = DictionaryCollection(None, {5: "Ala", 7: "Ela"})
        self.assertEqual(u.all(), {5: "Ala", 7: "Ela"})

    def test_getitem(self):
        u = DictionaryCollection(None, {5: "Ala", 7: "Ela"})
        self.assertEqual(u[5], "Ala")
        self.assertEqual(u[7], "Ela")

    def test_map_values(self):
        u = DictionaryCollection(None, {19: "Alice", 20: "Bob"}).map_values(lambda x : (len(x), x))
        self.assertEqual(u.all(), {19: (5, "Alice"), 20: (3, "Bob")})

    def test_map_keys_unique(self):
        u = DictionaryCollection(None, {19: "Alice", 20: "Bob"}).map_keys_unique(lambda x : 3*x)
        self.assertEqual(u.all(), {57: "Alice", 60: "Bob"})

    def test_map_keys_unique_fail(self):
        u = DictionaryCollection(None, {19: "Alice", 20: "Bob", 21: "Eve"}).map_values(lambda x : [x])
        with self.assertRaises(ValueError):
            u.map_keys_unique(lambda x : (x%2))

    def test_map_keys(self):
        u = DictionaryCollection(None, {19: "Alice", 20: "Bob", 21: "Eve"})        \
            .map_values(lambda x : [x])                                            \
            .map_keys(lambda x : (x%2), lambda y,z: (y+z))
        self.assertEqual(u.all(), {1: ["Alice", "Eve"], 0: ["Bob"]})

if __name__ == '__main__':
    unittest.main()
