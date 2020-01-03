class Environment:

    def __init__(self):
        self.identifiers = dict()

    def __getitem__(self, key):
        return self.identifiers[key]

    def __setitem__(self, key, value):
        self.identifiers[key] = value

    def __contains__(self, key):
        return key in self.identifiers
