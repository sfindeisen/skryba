from utils.log import debug, warning

import abc

class Type(abc.ABC):

    # Returns true if this type can be assigned from (substituted by) the other type.
    @abc.abstractmethod
    def is_assignable_from(self, another):
        raise NotImplementedError()

    def __str__(self):
        return "T"

# Unknown type denoted with a type variable, for example: 'a' or 'b'.
class AnyType(Type):

    def __init__(self, typevar):
        self.typevar = typevar

    def is_assignable_from(self, another):
        return (isinstance(another, AnyType) and (self.typevar == another.typevar))

    def __str__(self):
        return self.typevar

class ListType(Type):

    def __init__(self, itemtype):
        self.itemtype = itemtype

    def is_assignable_from(self, another):
        return (isinstance(another, ListType) and (self.itemtype.is_assignable_from(another.itemtype)))

    def __str__(self):
        return "[{}]".format(self.itemtype)

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
                    warning("Type unification error: {} is not an arrow type. It cannot be applied to: {} .".format(self.rtype, ", ".join(map(str, rest))))
                    return None     # more arguments, but rtype is not a function type!
                else:
                    return self.rtype
            else:
                warning("Type unification error: {} in arrow type ({}) is not assignable from {}.".format(self.ltype, self, arg_types[0]))
                return None
        else:
            debug("Arrow type ({}), but no arguments.".format(self))
            return self

    def is_assignable_from(self, another):
        return (
            isinstance(another, ArrowType) and
            (another.ltype.is_assignable_from(self.ltype)) and
            (self.rtype.is_assignable_from(another.rtype))
        )

    def __str__(self):
        return "({} -> {})".format(self.ltype, self.rtype)

class TupleType(Type):

    def __init__(self, item_types):
        self.item_types = item_types

    def __str__(self):
        s = ", ".join(map(str, self.item_types))
        return "({})".format(s)

class BooleanType(Type):

    def is_assignable_from(self, another):
        return isinstance(another, BooleanType);

    def __str__(self):
        return "boolean"

class FileType(Type):

    def is_assignable_from(self, another):
        return isinstance(another, FileType);

    def __str__(self):
        return "file"

class StringType(Type):

    def is_assignable_from(self, another):
        return isinstance(another, StringType);

    def __str__(self):
        return "string"

class XMLDocumentType(Type):

    def is_assignable_from(self, another):
        return isinstance(another, XMLDocumentType);

    def __str__(self):
        return "xml_document"

class XMLNodeType(Type):

    def is_assignable_from(self, another):
        return isinstance(another, XMLNodeType);

    def __str__(self):
        return "xml_node"

class VoidType(Type):

    def is_assignable_from(self, another):
        return isinstance(another, VoidType);

    def __str__(self):
        return "void"

anytype_a   = AnyType('a')
anytype_b   = AnyType('b')
anytype_c   = AnyType('c')
boolean_type= BooleanType()
string_type = StringType()
void_type   = VoidType()
