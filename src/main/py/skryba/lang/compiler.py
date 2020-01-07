from lang.ast import Identifier
from lang.types import boolean_type, string_type, void_type, xml_document_type, xml_node_type, AnyType, ArrowType, ListType

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

            compose = ArrowType(
                        ArrowType(AnyType('a'), AnyType('b')),
                        ArrowType(
                            ArrowType(AnyType('b'), AnyType('c')),
                            ArrowType(AnyType('a'), AnyType('c'))
                        )
            ),

            endswith = ArrowType(string_type, ArrowType(string_type, boolean_type)),

            filter = ArrowType(
                        ArrowType(AnyType('a'), boolean_type),
                        ArrowType(ListType(AnyType('a')), ListType(AnyType('a')))
            ),

            flip = ArrowType(
                       ArrowType(AnyType('a'), ArrowType(AnyType('b'), AnyType('c'))),
                       ArrowType(AnyType('b'), ArrowType(AnyType('a'), AnyType('c')))
            ),

            listdir = ArrowType(string_type, ListType(string_type)),

            map = ArrowType(
                ArrowType(AnyType('a'), AnyType('b')),
                ArrowType(ListType(AnyType('a')), ListType(AnyType('b')))
            ),

            normalize = ArrowType(string_type, string_type),
            parse_xml_dom = ArrowType(string_type, xml_document_type),
            strip = ArrowType(string_type, string_type),
            xpath1 = ArrowType(string_type, ArrowType(xml_document_type, xml_node_type)),
        )

# Name table.
# Mapping of: string -> type.
class Environment:

    def __init__(self, identifiers=dict()):
        self.identifiers = identifiers

    def __delitem__(self, key):
        del self.identifiers[key]

    def __getitem__(self, key):
        return self.identifiers.__getitem__(self.k2s(key))

    def __setitem__(self, key, value):
        self.identifiers.__setitem__(self.k2s(key), value)

    def __contains__(self, key):
        return self.identifiers.__contains__(self.k2s(key))

    def k2s(self, key):
        return (key.value if isinstance(key, Identifier) else key)

    def __str__(self):
        return " ".join("{}:{}".format(key, val) for key, val in sorted(self.identifiers.items()))

class Compiler:

    def __init__(self):
        self.env = Environment(BuiltIns().builtins)
