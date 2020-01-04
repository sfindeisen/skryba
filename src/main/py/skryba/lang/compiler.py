from lang.ast import Identifier
from lang.types import anytype_a, anytype_b, anytype_c, boolean_type, string_type, void_type, ArrowType, ListType

# Built-in functions
#
# filter        : (a -> boolean) -> [a] -> [a]
# map           : (a -> b) -> [a] -> [b]
# compose       : (a -> b) -> (b -> c) -> (a -> c)
# compose       : (a -> b) -> (b -> c) -> (c -> d) -> (a -> d)
# flip          : (a -> b -> c) -> b -> a -> c
#
# listdir       : string -> [file]
# parse_xml_dom : file -> xml_document
# xpath         : string -> xml_document -> [xml_node]
# xpath1        : string -> xml_document -> xml_node
#
# basename      : string -> string
# endswith      : string -> string -> boolean
# split         : string -> string -> [string]
# strip         : string -> string
# normalize     : string -> string
class BuiltIns:
    def __init__(self):
        self.builtins = dict(
            basename = ArrowType(string_type, string_type),
            endswith = ArrowType(string_type, ArrowType(string_type, boolean_type)),

            filter = ArrowType(
                        ArrowType(anytype_a, boolean_type),
                        ArrowType(ListType(anytype_a), ListType(anytype_a))
            ),

            flip = ArrowType(
                       ArrowType(anytype_a, ArrowType(anytype_b, anytype_c)),
                       ArrowType(anytype_b, ArrowType(anytype_a, anytype_c))
            )
        )

# Name table.
# Mapping of: string -> type.
class Environment:

    def __init__(self, identifiers=dict()):
        self.identifiers = identifiers

    def __getitem__(self, key):
        return self.identifiers.__getitem__(self.k2s(key))

    def __setitem__(self, key, value):
        self.identifiers.__setitem__(self.k2s(key), value)

    def __contains__(self, key):
        return self.identifiers.__contains__(self.k2s(key))

    def k2s(self, key):
        return (key.value if isinstance(key, Identifier) else key)

class Compiler:

    def __init__(self):
        self.env = Environment(BuiltIns().builtins)
