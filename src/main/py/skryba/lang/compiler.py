from lang.types import AnyType, ListType, ArrowType, BooleanType, FileType, StringType, XMLDocumentType, XMLNodeType


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
# endswith      : string -> string -> boolean
# split         : string -> string -> [string]
# strip         : string -> string
# normalize     : string -> string

class BuiltIns:

    def __init__(self):
        self.builtins = dict(
            filter = ArrowType(
                        ArrowType(AnyType('a'), BooleanType()),
                        ArrowType(ListType(AnyType('a')), ListType(AnyType('a'))))
        )

    def __getitem__(self, key):
        return self.builtins[key]

    def __setitem__(self, key, value):
        self.builtins[key] = value

    def __contains__(self, key):
        return key in self.builtins

class Environment:

    def __init__(self):
        self.identifiers = dict()

    def __getitem__(self, key):
        return self.identifiers[key]

    def __setitem__(self, key, value):
        self.identifiers[key] = value

    def __contains__(self, key):
        return key in self.identifiers

class Compiler:

    def __init__(self):
        self.env      = Environment()
        self.builtins = BuiltIns()
