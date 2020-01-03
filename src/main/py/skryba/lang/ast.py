import abc

class ASTNode(abc.ABC):
    pass

class Program(ASTNode):
    def __init__(self, statement, program=None):
        self.statements = [statement] + ([] if (program is None) else program.statements)

class Statement(ASTNode):
    pass

class Expression(ASTNode):
    pass

class Bind(Statement):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class FunCallStmt(Statement):
    def __init__(self, funcall):
        self.funcall = funcall

class FunCallExpr(Expression):
    def __init__(self, identifier, arguments):
        self.identifier = identifier
        self.arguments  = arguments

class Identifier(Expression):
    def __init__(self, value):
        self.value = value

class Lambda(Expression):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class StringLiteral(Expression):
    def __init__(self, value):
        self.value = value

class Tuple(Expression):
    def __init__(self, values):
        self.values = values
