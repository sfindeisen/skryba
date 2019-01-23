#!/usr/bin/python3

import functools
import os

import skryba
import collection
import utils.xml

from abc import abstractmethod

def listdir(dirname):
    return DirectoryContents(None, dirname)

class FileSet(skryba.Base):
    """A set of file names."""
    def __init__(self, parent):
        super().__init__(parent)
        self.current_file = None

    @abstractmethod
    def all(self):
        """Returns all the file names in this set."""
        raise NotImplementedError()

    def set_current_file(self, f):
        self.current_file = f

    def __map(self, f, x):
        self.set_current_file(x)
        return f(self, x)

    def map(self, f):
        return collection.Collection(self, list(map(functools.partial(self.__map, f), self.all())))

    def foreach(self, f):
        self.map(f)
        return self

    def filter(self, predicate):
        return FileFilter(self, predicate)

    def filter_xml(self):
        return XMLFileSet(self.filter(lambda x : x.endswith('.xml')))

class DirectoryContents(FileSet):

    def __init__(self, parent, dirname):
        super().__init__(parent)
        self.dirname = dirname

    def all(self):
        return list(map(lambda x : os.path.join(self.dirname, x), os.listdir(self.dirname)))

class FileFilter(FileSet):

    def __init__(self, parent, predicate):
        super().__init__(parent)
        self.filter = predicate

    def all(self):
        return filter(self.filter, self.parent.all())

class XMLFileSet(FileSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.xslt_proc   = None
        self.current_dom = None

    def get_current_dom(self):
        if (self.current_dom is None):
            self.current_dom = utils.xml.parse_xml_dom(self.current_file)
        return self.current_dom

    def set_current_file(self, f):
        super().set_current_file(f)
        self.current_dom = None

    def all(self):
        return self.parent.all()

    def with_xslt(self, xslt_path):
        self.xslt_proc = utils.xml.get_xslt_transformer(xslt_path)
        return self

    def xpath1(self, xpath):
        return utils.xml.get_xpath1(self.get_current_dom(), xpath)

    def xslt_transform(self):
        u = self.xslt_proc(self.get_current_dom())
        for e in self.xslt_proc.error_log:
            warning(e)
        return u
