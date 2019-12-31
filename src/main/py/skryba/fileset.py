#!/usr/bin/python3

import functools
import os

import base
import collection
import generator
import utils.log
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

    def __set_current_file(self, f):
        self.current_file = f

    def __map(self, f, x):
        self.__set_current_file(x)
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

    def print_xslt_error_log(self, error_log):
        for entry in error_log:
            utils.log.warning(entry)
            # utils.log.warning('message from line {}, col {}: {}'.format(entry.line, entry.column, entry.message))
            # utils.log.warning('domain: {} ({})'.format(entry.domain_name, entry.domain))
            # utils.log.warning('type: {} ({})'.format(entry.type_name, entry.type))
            # utils.log.warning('level: {} ({})'.format(entry.level_name, entry.level))
            # utils.log.warning('filename: {}'.format(entry.filename))

    def __get_current_dom(self):
        if (self.current_dom is None):
            self.current_dom = utils.xml.parse_xml_dom(self.current_file)
        return self.current_dom

    def __set_current_file(self, f):
        super().__set_current_file(f)
        self.current_dom = None

    def all(self):
        return self.parent.all()

    def __load_xslt(self, xslt_path):
        """Loads the XSLT processor for the given filepath."""
        if (xslt_path not in self.xslt_proc):
            self.xslt_proc[xslt_path] = utils.xml.get_xslt_transformer(xslt_path)
        return self.xslt_proc[xslt_path]

    def xpath0(self, xpath):
        return utils.xml.get_xpath0(self.__get_current_dom(), xpath)

    def xpath1(self, xpath):
        return utils.xml.get_xpath1(self.__get_current_dom(), xpath)

    def xslt_transform(self, xslt_path, **kwargs):
        t = self.__load_xslt(xslt_path)
        u = t(self.__get_current_dom(), **kwargs)
        self.print_xslt_error_log(t.error_log)
        # TODO errors get accumulated across transforms; XSLT reload?...
        return u
