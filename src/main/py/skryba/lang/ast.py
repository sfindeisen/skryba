from lang.types import anytype_a, string_type, void_type, ArrowType, TupleType
from utils.log import warning

import abc

class ASTNode(abc.ABC):

    def __init__(self):
        self.ctype = None     # Compile-time type

    # Computes expression types (.ctype) and runs various checks.
    @abc.abstractmethod
    def compile(self, compiler):
        raise NotImplementedError()

class Program(ASTNode):

    def __init__(self, statement, program=None):
        self.statements = [statement] + ([] if (program is None) else program.statements)

    def compile(self, compiler):
        ct = void_type
        for s in self.statements:
            s.compile(compiler)
            if (s.ctype is None):
                ct = None
        self.ctype = ct

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

        if (self.identifier in compiler.env):
            warning("Re-bind not supported: {}".format(self.identifier))
            self.ctype = None
        else:
            compiler.env[self.identifier] = self.expression.ctype
            self.ctype = (None if (self.expression.ctype is None) else void_type)

class FunCallStmt(Statement):

    def __init__(self, funcallexpr):
        self.funcallexpr = funcallexpr

    def compile(self, compiler):
        self.funcallexpr.compile(compiler)
        self.ctype = (None if (self.funcallexpr.ctype is None) else void_type)

class FunCallExpr(Expression):

    def __init__(self, identifier, arguments):
        self.identifier = identifier
        self.arguments  = arguments

    def compile(self, compiler):
        err = False
        argtypes = []
        for arg in self.arguments:
            arg.compile(compiler)
            argtypes.append(arg.ctype)
            if (arg.ctype is None):
                err = True

        if (err):
            self.ctype = None
            warning("Unable to compute function argument types: {}".format(self.identifier))
            return

        if (self.identifier in compiler.env):
            fn_type = compiler.env[self.identifier]
            if isinstance(fn_type, ArrowType):
                res_type = fn_type.result_type(argtypes)
                if (res_type is None):
                    warning("Type error: {} . Actual parameter types ({}) do not match the function type ({}).".format(
                        self.identifier,
                        ", ".join(map(str, argtypes)),
                        fn_type))
                self.ctype = res_type
            else:
                warning("Type error: {} is not a function. Cannot be applied to {} arguments.".format(self.identifier, len(self.arguments)))
                self.ctype = None
        else:
            warning("Unknown function: {}".format(self.identifier))
            self.ctype = None

class Identifier(Expression):

    def __init__(self, value):
        self.value = value

    def compile(self, compiler):
        if (self.value in compiler.env):
            self.ctype = compiler.env[self.value]
        else:
            warning("Unknown identifier: {}".format(self.value))
            self.ctype = None

class Lambda(Expression):

    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    # TODO free vars, identifier shadowing ...
    def compile(self, compiler):
        self.expression.compile(compiler)
        self.ctype = (None if (self.expression.ctype is None) else (ArrowType(anytype_a, self.expression.ctype)))

class StringLiteral(Expression):

    def __init__(self, value):
        self.value = value

    def compile(self, compiler):
        self.ctype = string_type

class Tuple(Expression):

    def __init__(self, values):
        self.values = values

    def compile(self, compiler):
        err = False
        tt = []
        for v in self.values:
            v.compile(compiler)
            tt.append(v.ctype)
            if (v.ctype is None):
                err = True
        self.ctype = (None if err else TupleType(tt))
