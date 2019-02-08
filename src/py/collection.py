#!/usr/bin/python3

import generator
import skryba

class Collection(skryba.Base):
    """A collection of items."""
    def __init__(self, parent, items):
        super().__init__(parent)
        self.items = items

    def __getitem__(self, k):
        """The subscript[k] method (might not work with all collection types)."""
        return self.items[k]

    def all(self):
        """Returns all the items in this collection."""
        return self.items

    def map(self, f):
        """Map this collection into another collection using the specified mapping function."""
        return Collection(self, list(map(f, self.all())))

    def reverse_dict(self, f):
        """Given a function f, which, for each item X, yields a list L of elements Y, returns
           a new Collection (a child of this) wrapping a dictionary from Y to list of X.

           This can be used e.g. to generate a tag cloud from a list of blog posts.
        """
        rdic = {}
        for x in self.items:
            for y in f(x):
                rdic.setdefault(y, []).append(x)
        return Collection(self, rdic)

    def with_rendering_engine(self, search_path):
        return generator.RenderingEngine(self, search_path)
