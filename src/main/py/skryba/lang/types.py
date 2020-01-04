import abc

class Type(abc.ABC):
    pass

# Unknown type denoted with a type variable, for example: 'a' or 'b'.
class AnyType(Type):

    def __init__(self, typevar):
        self.typevar = typevar

class ListType(Type):

    def __init__(self, itemtype):
        self.itemtype = itemtype

class ArrowType(Type):

    def __init__(self, ltype, rtype):
        self.ltype = ltype
        self.rtype = rtype

class BooleanType(Type):
    pass
class FileType(Type):
    pass
class StringType(Type):
    pass
class XMLDocumentType(Type):
    pass
class XMLNodeType(Type):
    pass
