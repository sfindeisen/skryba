#!/usr/bin/python3

import functools
import os

import base
import collection
import generator
import utils.xml

from abc import abstractmethod

def listdir(dirname):
    return DirectoryContents(None, dirname)

class FileSet(base.Base):
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
        return collection.ListCollection(self, list(map(functools.partial(self.__map, f), self.all())))

    def foreach(self, f):
        self.map(f)
        return self

    def filter(self, predicate):
        return FileFilter(self, predicate)

    def filter_html(self):
        return HTMLFileSet(self.filter(lambda x : x.endswith('.html')))

    def filter_xml(self):
        return XMLFileSet(self.filter(lambda x : x.endswith('.xml')))

    def with_rendering_engine(self, search_path):
        return generator.RenderingEngine(self, search_path)

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

class HTMLFileSet(FileSet):

    def __init__(self, parent):
        super().__init__(parent)

    def all(self):
        return self.parent.all()

class XMLFileSet(FileSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.xslt_proc   = {}       # XSLT filepath -> XSLT processor
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

    def __load_xslt(self, xslt_path):
        """Loads the XSLT processor for the given filepath."""
        if (xslt_path not in self.xslt_proc):
            self.xslt_proc[xslt_path] = utils.xml.get_xslt_transformer(xslt_path)
        return self.xslt_proc[xslt_path]

    def xpath1(self, xpath):
        return utils.xml.get_xpath1(self.get_current_dom(), xpath)

    def xslt_transform(self, xslt_path, **kwargs):
        t = self.__load_xslt(xslt_path)
        u = t(self.get_current_dom(), **kwargs)
        for e in t.error_log:
            warning(e)
        return u
