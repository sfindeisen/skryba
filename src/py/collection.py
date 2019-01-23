#!/usr/bin/python3

import generator
import skryba

class Collection(skryba.Base):
    """A collection of items."""
    def __init__(self, parent, items):
        super().__init__(parent)
        self.items = items

    def all(self):
        """Returns all the items in this collection."""
        return self.items

    def map(self, f):
        """Map this collection into another collection using the specified mapping function."""
        return Collection(self, list(map(f, self.all())))

    def with_rendering_engine(self, search_path):
        return generator.RenderingEngine(self, search_path)
