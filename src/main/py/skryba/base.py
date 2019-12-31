import abc

class Base(abc.ABC):
    """Abstract base class of the toolchain."""
    def __init__(self, parent=None):
        self.parent = parent
