from lang.env import Environment
from utils.log import warning

import abc

class ASTNode(abc.ABC):

    def compile(self, env):
        """Pre-run checks, including: identifiers, types."""
        pass    # nothing to check

class Program(ASTNode):

    def __init__(self, statement, program=None):
        self.statements = [statement] + ([] if (program is None) else program.statements)

    def compile(self, env):
        """Pre-run checks, including: identifiers, types."""
        for s in self.statements:
            s.compile(env)

class Statement(ASTNode):
    pass

class Expression(ASTNode):
    pass

class Bind(Statement):

    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def compile(self, env):
        self.expression.compile(env)

        if (self.identifier in env):
            warning("Re-bind not supported: {}".format(self.identifier))
        else:
            env[self.identifier] = self.expression

class FunCallStmt(Statement):

    def __init__(self, funcall):
        self.funcall = funcall

    def compile(self, env):
        self.funcall.compile(env)

class FunCallExpr(Expression):

    def __init__(self, identifier, arguments):
        self.identifier = identifier
        self.arguments  = arguments

    def compile(self, env):
        for a in self.arguments:
            a.compile(env)

        # TODO better
        if (self.identifier not in env):
            warning("Identifier not found: {}".format(self.identifier))

class Identifier(Expression):

    def __init__(self, value):
        self.value = value

class Lambda(Expression):

    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    # TODO free vars
    def compile(self, env):
        self.expression.compile(env)

class StringLiteral(Expression):

    def __init__(self, value):
        self.value = value

class Tuple(Expression):

    def __init__(self, values):
        self.values = values

    def compile(self, env):
        for v in self.values:
            v.compile(env)
