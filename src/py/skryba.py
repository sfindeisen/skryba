#!/usr/bin/python3

import jinja2
import os
import tempfile

import utils.file
import utils.log
import utils.xml

from abc import ABC, abstractmethod
from functools import partial

from utils.file import write_file
from utils.log import debug, info
from utils.xml import parse_xml_dom, get_xpath1

# Export these functions to the top level
verbose = utils.log.set_verbose
info    = utils.log.info
debug   = utils.log.debug

class Base(ABC):
    """Abstract base class in Skryba chain."""
    def __init__(self, parent=None):
        self.parent = parent

    def listdir(self, dirname):
        return DirectoryContents(self, dirname)

    def with_rendering_engine(self, search_path):
        return RenderingEngine(self, search_path)

class Generator(Base):
    """Basic output file generator."""
    def __init__(self, parent):
        super().__init__(parent)
        self.output_dir = tempfile.TemporaryDirectory()
        debug('Using temp outdir: {}'.format(self.output_dir.name))

    def output_filename(self, basename):
        return os.path.join(self.output_dir.name, basename)

    def copy_to(self, dest_dir):
        utils.file.copytree(self.output_dir.name, dest_dir)
        return self
                                                   
class RenderingEngine(Generator):
    """jinja2 rendering interface."""

    def __init__(self, parent, search_path):
        super().__init__(parent)
        spath = os.path.abspath(search_path)
        debug('jinja2 template search path: {}'.format(spath))
        loader = jinja2.FileSystemLoader(searchpath=spath, encoding='utf-8', followlinks=True)
        self.env = jinja2.Environment(loader=loader)
        self.template_file = None

    def with_template(self, filename):
        self.template_file = filename
        return self

    def render(self, output_file, **kwargs):
        template = self.env.get_template(self.template_file)
        html = template.render(**kwargs)
        write_file(self.output_filename(output_file), html.encode(encoding='utf-8', errors='strict'))
        return self

class FileSet(Base):
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
        return list(map(partial(self.__map, f), self.all()))

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
        return self.xslt_proc(self.get_current_dom())
