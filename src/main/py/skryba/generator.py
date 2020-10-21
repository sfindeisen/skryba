import collections.abc
import operator
import os
import tempfile

import jinja2
import lxml.etree as ET

import base
from utils.file import copytree, write_file
from utils.log import debug
import utils.text

class Generator(base.Base):
    """Basic output file generator."""
    def __init__(self, parent):
        super().__init__(parent)
        self.output_dir = tempfile.TemporaryDirectory()
        debug('Using temp outdir: {}'.format(self.output_dir.name))

    def all(self):
        """Returns all the items in this collection."""
        return self.parent.all()

    def output_filename(self, basename):
        return os.path.join(self.output_dir.name, basename)

    def copy_to(self, dest_dir):
        copytree(self.output_dir.name, dest_dir)
        return self

class XMLGenerator(Generator):
    """Generator of XML files"""
    def __init__(self, parent):
        super().__init__(parent)

    def generate_xml_all(self, f_name, f_gen_xml_dom):
        """
        Given a function f_name : item -> string and f_gen_xml_dom : item -> XML DOM, calls them for each item
        to compute the output file name, the XML DOM and to write out the output file.
        """
        for x in self.all():
            self._generate_xml((f_name(x)), (f_gen_xml_dom(x)))
        return self

    def _generate_xml(self, output_file, output_xml_dom):
        """Given a (basic) output file name and output XML DOM, writes the output file."""
        write_file(self.output_filename(output_file), ET.tostring(output_xml_dom, pretty_print=True, xml_declaration=True, encoding='utf-8', method='xml'))
        return self

class RenderingEngine(Generator):
    """jinja2 rendering interface."""

    def __init__(self, parent, search_path):
        super().__init__(parent)
        spath = os.path.abspath(search_path)
        debug('jinja2 template search path: {}'.format(spath))
        loader = jinja2.FileSystemLoader(searchpath=spath, encoding='utf-8', followlinks=True)
        self.env = RenderingEngine.make_env(loader)
        self.template_file = None

    @staticmethod
    def make_env(loader):
        env = jinja2.Environment(loader=loader)
        # These vars are always available, see: https://jinja.palletsprojects.com/en/2.11.x/api/#jinja2.Environment.globals
        env.globals['skryba_string2id'] = utils.text.string2id
        return env

    def with_template(self, filename):
        self.template_file = filename
        return self

    def render_all(self, f_name, f_args):
        """
        Given a function f_name : item -> string and f_args : item -> dict, calls them for each item
        to compute the output file name, actual template parameters and to render the output file
        contents. If the underlying collection is a dictionary, item will be a key value pair.
        """
        all_items = self.all()

        if isinstance(all_items, collections.abc.Mapping):
            # the underlying collection is a dictionary (Mapping)
            for k, v in all_items.items():
                self.render((f_name((k,v))), **(f_args((k,v))))
        else:
            for x in all_items:
                self.render((f_name(x)), **(f_args(x)))

        return self

    def render_all_templates(self, **kwargs):
        """Render all items as templates."""
        for x in self.all():
            debug('render all templates: {}'.format(x))
            template = self.env.get_template(x)
            # Here we pass 2 extra parameters to the template:
            #   - name     : the loading name of the template (e.g. base file name)
            #   - filename : the filepath of the template in the filesystem (if any)
            html = template.render(name=template.name, filename=template.filename, **kwargs)
            write_file(self.output_filename(x), html.encode(encoding='utf-8', errors='strict'))
        return self

    def render(self, output_file, **kwargs):
        template = self.env.get_template(self.template_file)
        html = template.render(**kwargs)
        write_file(self.output_filename(output_file), html.encode(encoding='utf-8', errors='strict'))
        return self
