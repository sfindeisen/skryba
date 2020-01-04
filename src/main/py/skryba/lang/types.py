from utils.log import debug, warning

import abc

class Type(abc.ABC):

    # Returns true if this type can be unified with the other type.
    #
    # tvmapL is a mapping from free type variables of this type into types (parts of the other type)
    # rvmapR is a mapping from free type variables of the other type into types (parts of this type)
    @abc.abstractmethod
    def _unify(self, another, tvmapL, tvmapR):
        raise NotImplementedError()

    def __str__(self):
        return "T"

# Unknown type denoted with a type variable, for example: 'a' or 'b'.
class AnyType(Type):

    def __init__(self, typevar):
        self.typevar = typevar

    def _unify(self, another, tvmapL, tvmapR):
        if (self.typevar in tvmapL):
            # debug("self.typevar = {}".format(self.typevar))
            # debug("another = {}".format(another))
            # debug("Type variable mapping (L): {}".format(tvmapL))
            # debug("Type variable mapping (R): {}".format(tvmapR))
            # debug("tvmapL[self.typevar] = {}".format(tvmapL[self.typevar]))
            # res = (tvmapL[self.typevar] == another)
            # debug("res = {}".format(res))
            return (tvmapL[self.typevar] == another)
        else:
            tvmapL[self.typevar] = another
            return True

    def __str__(self):
        return self.typevar

class ListType(Type):

    def __init__(self, itemtype):
        self.itemtype = itemtype

    def _unify(self, another, tvmapL, tvmapR):
        return (isinstance(another, ListType) and (self.itemtype._unify(another.itemtype, tvmapL, tvmapR)))

    def __str__(self):
        return "[{}]".format(self.itemtype)

class ArrowType(Type):

    def __init__(self, ltype, rtype):
        self.ltype = ltype
        self.rtype = rtype

    # Given the types of arguments, returns the type of the result.
    # None if error.
    #
    # tvmapL is a mapping from free type variables of this type into types (parts of the other type)
    # rvmapR is a mapping from free type variables of the other type into types (parts of this type)
    def result_type(self, arg_types, tvmapL=dict(), tvmapR=dict()):
        if (arg_types):
            if (self.ltype._unify(arg_types[0], tvmapL, tvmapR)):
                rest = arg_types[1:]
                if isinstance(self.rtype, ArrowType):
                    return self.rtype.result_type(rest, tvmapL, tvmapR)
                elif (rest):
                    warning("Type unification error: {} is not an arrow type. It cannot be applied to: {} .".format(self.rtype, ", ".join(map(str, rest))))
                    return None     # more arguments, but rtype is not a function type!
                else:
                    return self.rtype.map_type_variables(tvmapL)
            else:
                warning("Type unification error: {} in arrow type ({}) does not match {} .".format(self.ltype, self, arg_types[0]))
                debug("Type variable mapping (L): {}".format(tvmapL))
                debug("Type variable mapping (R): {}".format(tvmapR))
                return None
        else:
            debug("Arrow type ({}), but no arguments.".format(self))
            return self

    def _unify(self, another, tvmapL, tvmapR):
        if (isinstance(another, ArrowType)):
            return ((self.ltype._unify(another.ltype, tvmapL, tvmapR)) and (self.rtype._unify(another.rtype, tvmapL, tvmapR)))
        return False

    def __str__(self):
        return "({} -> {})".format(self.ltype, self.rtype)

class TupleType(Type):

    def __init__(self, item_types):
        self.item_types = item_types

    def __str__(self):
        s = ", ".join(map(str, self.item_types))
        return "({})".format(s)

class BooleanType(Type):

    def _unify(self, another, tvmapL, tvmapR):
        return isinstance(another, BooleanType);

    def __str__(self):
        return "boolean"

class FileType(Type):

    def _unify(self, another, tvmapL, tvmapR):
        return isinstance(another, FileType);

    def __str__(self):
        return "file"

class StringType(Type):

    def _unify(self, another, tvmapL, tvmapR):
        return isinstance(another, StringType);

    def __str__(self):
        return "string"

class XMLDocumentType(Type):

    def _unify(self, another, tvmapL, tvmapR):
        return isinstance(another, XMLDocumentType);

    def __str__(self):
        return "xml_document"

class XMLNodeType(Type):

    def _unify(self, another, tvmapL, tvmapR):
        return isinstance(another, XMLNodeType);

    def __str__(self):
        return "xml_node"

class VoidType(Type):

    def _unify(self, another, tvmapL, tvmapR):
        return isinstance(another, VoidType);

    def __str__(self):
        return "void"

anytype_a   = AnyType('a')
anytype_b   = AnyType('b')
anytype_c   = AnyType('c')
boolean_type= BooleanType()
string_type = StringType()
void_type   = VoidType()
