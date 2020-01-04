from lang.env import Environment

class Compiler:

    def __init__(self):
        self.env = Environment()

    def __getitem__(self, key):
        return self.env[key]

    def __setitem__(self, key, value):
        self.env[key] = value

    def __contains__(self, key):
        return key in self.env
