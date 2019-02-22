#!/usr/bin/python3

import jinja2
import os
import tempfile

import base
from utils.file import copytree, write_file
from utils.log import debug

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

    def render_all(self, f_name, f_args):
        for x in self.all():
            self.render((f_name(x)), **(f_args(x)))
        return self

    def render_all_templates(self, **kwargs):
        """Render all items as templates."""
        for x in self.all():
            debug('render all templates: {}'.format(x))
            template = self.env.get_template(x)
            html = template.render(**kwargs)
            write_file(self.output_filename(x), html.encode(encoding='utf-8', errors='strict'))
        return self

    def render(self, output_file, **kwargs):
        template = self.env.get_template(self.template_file)
        html = template.render(**kwargs)
        write_file(self.output_filename(output_file), html.encode(encoding='utf-8', errors='strict'))
        return self
