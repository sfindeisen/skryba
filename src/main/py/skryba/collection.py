#!/usr/bin/python3

import base
import generator

from utils.log import warning

class Collection(base.Base):
    """A collection of items."""

    def __init__(self, parent, items):
        super().__init__(parent)
        self.items = items

    def all(self):
        """Returns all the items in this collection."""
        return self.items

    def reverse_dict(self, f):
        """
        Given a function f, which, for each item X, yields a list L of elements Y, returns
        a new DictionaryCollection (a child of this) wrapping a dictionary from Y to list
        of X.

        This can be used e.g. to generate a tag cloud from a list of blog posts.
        """
        rdic = {}
        for x in self.items:
            for y in f(x):
                rdic.setdefault(y, []).append(x)
        return DictionaryCollection(self, rdic)

    def with_rendering_engine(self, search_path):
        return generator.RenderingEngine(self, search_path)

class ListCollection(Collection):

    def __init__(self, parent, items):
        super().__init__(parent, items)

    def __getitem__(self, k):
        return self.items[k]

    def map(self, f):
        return ListCollection(self, list(map(f, self.items)))

class DictionaryCollection(Collection):
    """A collection of key-value pairs."""

    def __init__(self, parent, items):
        super().__init__(parent, items)

    def __getitem__(self, k):
        return self.items[k]

    def map_values(self, f):
        return DictionaryCollection(self, {k: f(v) for k, v in self.items.items()})

    def map_values_with_keys(self, f):
        return DictionaryCollection(self, {k: f(k,v) for k, v in self.items.items()})

    def map_values_as_list(self):
        return self.map_values(lambda x : [x])

    def map_keys_uq(self, f):
        y = self.items.items()
        z = {f(k): v for k, v in y}
        if (len(z) == len(y)):
            return DictionaryCollection(self, z)
        else:
            raise ValueError("unique constraint violation")

    def map_keys(self, f, merge, warn=False):
        y = {}
        for k, v in self.items.items():
            z = f(k)
            if z in y:
                if (warn):
                    warning("Duplicate key: {}".format(z))
                y[z] = merge(y[z], v)   # merge these 2 values
            else:
                y[z] = v
        return DictionaryCollection(self, y)

    def map_keys_with_values(self, f, merge, warn=False):
        """
        f(k,v) is taken to be the new key
        merge(v1,v2) is used to merge 2 values in case of key conflict
        """
        y = {}
        for k, v in self.items.items():
            z = f(k,v)
            if z in y:
                if (warn):
                    warning("Duplicate key: {}".format(z))
                y[z] = merge(y[z], v)   # merge these 2 values
            else:
                y[z] = v
        return DictionaryCollection(self, y)

    def values(self):
        return ListCollection(self, self.items.values())
