from utils.log import debug, warning

import abc

class Type(abc.ABC):

    # Returns true if this type can be unified with the other type. Extends tvmapL and tvmapR with the
    # appropriate mappings.
    #
    # tvmapL is a mapping from free type variables of this type into types (parts of the other type)
    # rvmapR is a mapping from free type variables of the other type into types (parts of this type)
    @abc.abstractmethod
    def _unify(self, another, tvmapL, tvmapR):
        raise NotImplementedError("Type class does not implement _unify method!")

    def __str__(self):
        return "T"

# Unknown type denoted with a type variable, for example: 'a' or 'b'.
class AnyType(Type):

    def __init__(self, typevar):
        self.typevar = typevar
        self.inferred= None

    # Computes the final mapping for this typevar. This is a fully specified type (no typevars).
    @staticmethod
    def _final_type(tvmapL, tvmapR, current_type, visitedL=frozenset(), visitedR=frozenset()):
        if isinstance(current_type, ScalarType):
            return current_type
        elif isinstance(current_type, AnyType):
            if (current_type.typevar in tvmapL) and (current_type.typevar not in visitedL):
                return AnyType._final_type(tvmapR, tvmapL, tvmapL[current_type.typevar], visitedR, visitedL | frozenset([current_type.typevar]))
            else:
                return None
        elif isinstance(current_type, ArrowType):
            finalL = AnyType._final_type(tvmapL, tvmapR, current_type.ltype, visitedL, visitedR)
            finalR = AnyType._final_type(tvmapL, tvmapR, current_type.rtype, visitedL, visitedR)
            return (None if ((finalL is None) or (finalR is None)) else ArrowType(finalL, finalR))
        elif isinstance(current_type, ListType):
            raise NotImplementedError("_final_type: list")
        elif isinstance(current_type, TupleType):
            raise NotImplementedError("_final_type: tuple")
        else:
            raise NotImplementedError("Unknown type: {}".format(current_type))

    def _unify(self, another, tvmapL, tvmapR):
        # debug("_unify {} with {}".format(self, another))

        if (self.typevar in tvmapL):
            finalL = AnyType._final_type(tvmapL, tvmapR, self)
            debug("Mapping (L): {} ~> {}".format(self, finalL))
            self.inferred = self.inferred or finalL
            finalR = AnyType._final_type(tvmapR, tvmapL, another)
            debug("Mapping (R): {} ~> {}".format(another, finalR))

            if ((finalL is not None) and (finalL == finalR)):
                debug("{} (L) = {} (R) => true".format(finalL, finalR))
                return True
            else:
                if (isinstance(another, AnyType) and ((another.typevar) not in tvmapR)):
                    debug("Mapping type variable {} (R) to {} (L)".format(another.typevar, self))
                    tvmapR[another.typevar] = self
                    return True
                else:
                    warning("Type unification error: unable to re-map type variable {} (L) to {} (R), because it is already mapped to {} (R).".format(self.typevar, another, tvmapL[self.typevar]))

                    debug("AnyType _unify: self.typevar = {}".format(self.typevar))
                    debug("AnyType _unify: another = {}".format(another))
                    debug("AnyType _unify: Type variable mapping (L): {}".format(tvmapL))
                    debug("AnyType _unify: Type variable mapping (R): {}".format(tvmapR))
                    debug("AnyType _unify: tvmapL[{}] = {}".format(self.typevar, tvmapL[self.typevar]))

                    return False
        else:
            debug("Mapping type variable {} (L) to {} (R)".format(self.typevar, another))
            tvmapL[self.typevar] = another
            return True

    def __str__(self):
        return ((self.typevar) if (self.inferred is None) else str(self.inferred))

class ListType(Type):

    def __init__(self, itemtype):
        self.itemtype = itemtype

    def _unify(self, another, tvmapL, tvmapR):
        if (isinstance(another, ListType)):
            return (self.itemtype._unify(another.itemtype, tvmapL, tvmapR))
        elif (isinstance(another, AnyType)):
            return another._unify(self, tvmapR, tvmapL)
        else:
            warning("Failed to unify list type {} with {}".format(self, another))
            return False

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
                    return self.rtype
            else:
                warning("Type unification error: {} in arrow type: {} does not match argument type: {} .".format(self.ltype, self, arg_types[0]))
                debug("Type variable mapping (L): {}".format(tvmapL))
                debug("Type variable mapping (R): {}".format(tvmapR))
                return None
        else:
            debug("Arrow type: {}, but no arguments.".format(self))
            return self

    def _unify(self, another, tvmapL, tvmapR):
        if (isinstance(another, ArrowType)):
            return ((self.ltype._unify(another.ltype, tvmapL, tvmapR)) and (self.rtype._unify(another.rtype, tvmapL, tvmapR)))
        elif (isinstance(another, AnyType)):
            return another._unify(self, tvmapR, tvmapL)
        else:
            warning("Failed to unify arrow type {} with {}".format(self, another))
            return False

    def __str__(self):
        return "({} -> {})".format(self.ltype, self.rtype)

class TupleType(Type):

    def __init__(self, item_types):
        self.item_types = item_types

    # TODO implement _unify

    def __str__(self):
        s = ", ".join(map(str, self.item_types))
        return "({})".format(s)

class ScalarType(Type):

    def _unify(self, another, tvmapL, tvmapR):
        if (self == another):
            return True
        elif (isinstance(another, AnyType)):
            return another._unify(self, tvmapR, tvmapL)
        else:
            warning("Failed to unify scalar type {} with {}".format(self, another))
            return False

    def __str__(self):
        return "scalar"

class BooleanType(ScalarType):

    def __str__(self):
        return "boolean"

class FileType(ScalarType):

    def __str__(self):
        return "file"

class StringType(ScalarType):

    def __str__(self):
        return "string"

class XMLDocumentType(ScalarType):

    def __str__(self):
        return "xml_document"

class XMLNodeType(ScalarType):

    def __str__(self):
        return "xml_node"

class UnknownType(Type):

    def _unify(self, another, tvmapL, tvmapR):
        return (self == another)

    def __str__(self):
        return "unknown"

class VoidType(Type):

    def _unify(self, another, tvmapL, tvmapR):
        return (self == another)

    def __str__(self):
        return "void"

anytype_a         = AnyType('a')
anytype_b         = AnyType('b')
anytype_c         = AnyType('c')
boolean_type      = BooleanType()
file_type         = FileType()
string_type       = StringType()
unknown_type      = UnknownType()
void_type         = VoidType()
xml_document_type = XMLDocumentType()
xml_node_type     = XMLNodeType()
