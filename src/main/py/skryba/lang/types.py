import abc

class Type(abc.ABC):

    # Returns true if this type can be assigned from (substituted by) the other type.
    @abc.abstractmethod
    def is_assignable_from(self, another):
        raise NotImplementedError()

# Unknown type denoted with a type variable, for example: 'a' or 'b'.
class AnyType(Type):

    def __init__(self, typevar):
        self.typevar = typevar

    def is_assignable_from(self, another):
        return (isinstance(another, AnyType) and (self.typevar == another.typevar))

class ListType(Type):

    def __init__(self, itemtype):
        self.itemtype = itemtype

    def is_assignable_from(self, another):
        return (isinstance(another, ListType) and (self.itemtype.is_assignable_from(another.itemtype)))

class ArrowType(Type):

    def __init__(self, ltype, rtype):
        self.ltype = ltype
        self.rtype = rtype

    # Given the types of arguments, returns the type of the result
    # None if error
    def result_type(self, arg_types):
        if (arg_types):
            if (self.ltype.is_assignable_from(arg_types[0])):
                rest = arg_types[1:]
                if isinstance(self.rtype, ArrowType):
                    return self.rtype.result_type(rest)
                elif (rest):
                    return None     # more arguments, but rtype is not a function type!
                else:
                    return self.rtype
        return None

    def is_assignable_from(self, another):
        return (
            isinstance(another, ArrowType) and
            (another.ltype.is_assignable_from(self.ltype)) and
            (self.rtype.is_assignable_from(another.rtype))
        )

class TupleType(Type):

    def __init__(self, item_types):
        self.item_types = item_types

class BooleanType(Type):

    def is_assignable_from(self, another):
        return isinstance(another, BooleanType);

class FileType(Type):

    def is_assignable_from(self, another):
        return isinstance(another, FileType);

class StringType(Type):

    def is_assignable_from(self, another):
        return isinstance(another, StringType);

class XMLDocumentType(Type):

    def is_assignable_from(self, another):
        return isinstance(another, XMLDocumentType);

class XMLNodeType(Type):

    def is_assignable_from(self, another):
        return isinstance(another, XMLNodeType);

class VoidType(Type):

    def is_assignable_from(self, another):
        return isinstance(another, VoidType);

anytype_a   = AnyType('a')
string_type = StringType()
void_type   = VoidType()
