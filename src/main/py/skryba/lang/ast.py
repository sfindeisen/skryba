from utils.log import warning

import abc

class ASTNode(abc.ABC):

    def compile(self, compiler):
        """Pre-run checks, including: identifiers, types."""
        pass    # nothing to check

class Program(ASTNode):

    def __init__(self, statement, program=None):
        self.statements = [statement] + ([] if (program is None) else program.statements)

    def compile(self, compiler):
        """Pre-run checks, including: identifiers, types."""
        for s in self.statements:
            s.compile(compiler)

class Statement(ASTNode):
    pass

class Expression(ASTNode):
    pass

class Bind(Statement):

    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def compile(self, compiler):
        self.expression.compile(compiler)

        if (self.identifier in compiler):
            warning("Re-bind not supported: {}".format(self.identifier))
        else:
            compiler[self.identifier] = self.expression

class FunCallStmt(Statement):

    def __init__(self, funcall):
        self.funcall = funcall

    def compile(self, compiler):
        self.funcall.compile(compiler)

class FunCallExpr(Expression):

    def __init__(self, identifier, arguments):
        self.identifier = identifier
        self.arguments  = arguments

    def compile(self, compiler):
        for a in self.arguments:
            a.compile(compiler)

        # TODO better
        if (self.identifier not in compiler):
            warning("Identifier not found: {}".format(self.identifier))

class Identifier(Expression):

    def __init__(self, value):
        self.value = value

class Lambda(Expression):

    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    # TODO free vars
    def compile(self, compiler):
        self.expression.compile(compiler)

class StringLiteral(Expression):

    def __init__(self, value):
        self.value = value

class Tuple(Expression):

    def __init__(self, values):
        self.values = values

    def compile(self, compiler):
        for v in self.values:
            v.compile(compiler)
