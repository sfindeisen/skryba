#!/usr/bin/python3

import argparse
import datetime
import functools
import os
import os.path
import re

from skryba.index import verbose, force_overwrite, warning, info, debug, normalize_string, string2id, listdir, copytree
from skryba.utils.collection import filter_dict_values_not_none

re_date = re.compile('^([0-9]{4})-([0-9]{2})-([0-9]{2})(?:;(.*))?$')
date_format_default = '%a, %d %b %Y'

class Post:
    """A single blog post."""
    def __init__(self):
        self.basename = None    # input file base name
        self.title    = None    # post/title

        self.origdate = None    # orig-date post attribute value
        self.year     = None
        self.month    = None
        self.day      = None
        self.date_cmt = None
        self.date_fmt = None    # formatted date (string)
        self.date     = None    # datetime.date object

        self.lang     = None    # language code: en, pl ...
        self.html     = None    # HTML of the post body
        self.tags     = None    # list of tags (string)
        self.xmldom   = None

class Tag:
    """A single article tag."""
    def __init__(self, filename=None, value=None, posts=[]):
        self.filename = filename    # filename (base)
        self.value    = value       # Unicode (normalized)
        self.posts    = posts       # list of Post

def parse_date(pi):
    m = re_date.match(pi.origdate)
    if (m):
        g        = m.groups()
        pi.year  = g[0]
        pi.month = g[1]
        pi.day   = g[2]
        if (4 <= len(g)):
            pi.date_cmt = g[3]
        pi.date = datetime.date(int(pi.year), int(pi.month), int(pi.day))
    else:
        warning("Invalid date format: {}".format(pi.origdate))

def make_post(xpost, skryba, filename, date_fmt=date_format_default, **kwargs):
    """Parses post XML file. Returns Post instance."""
    info("Process post: " + filename)
    basename = os.path.basename(filename)[:-4]    # basename without .xml

    pi = Post()
    pi.basename = '{}.html'.format(basename)
    pi.title = skryba.xpath1('/post/title/text()')
    debug("title: {}".format(pi.title))
    pi.lang = skryba.xpath0('/post/@lang')
    debug("lang: {}".format(pi.lang))
    pi.tags = list(filter(bool, map(lambda s : normalize_string(s.strip()), skryba.xpath1('/post/tags/text()').split(';'))))
    debug("tags: {}".format(pi.tags))

    pi.origdate = skryba.xpath1('/post/@orig-date')
    debug("orig date: {}".format(pi.origdate))
    parse_date(pi)
    if (pi.date):
        pi.date_fmt = pi.date.strftime(date_fmt)
        debug('date_fmt: {}'.format(pi.date_fmt))
    else:
        warning('unable to format post creation date; lang={} date={}'.format(pi.lang, pi.date))

    pi.html = skryba.xslt_transform(xpost, **kwargs)
    pi.xmldom = skryba.current_dom
    return pi

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='generate.py',
        description='''
Generates the complete blog by processing input post XML files and input Jinja2 HTML template files.
Each post will result in a corresponding output HTML file generated in output-dir/post/ .
Each tag will result in a corresponding output HTML file generated in output-dir/tag/ .
Jinja2 HTML template files named post.html and tag.html must be present. Other HTML template files will be
processed in a generic way (see the documentation).
Contents of input-dir will be copied as is to the output-dir.
''',
        add_help=True, allow_abbrev=False, epilog="""This program comes with ABSOLUTELY NO WARRANTY.""")

    parser.add_argument("--verbose", required=False, action="store_true", help="Verbose processing")
    parser.add_argument("--overwrite-all", required=False, action="store_true", help="Overwrite all files without prompting (batch mode)")
    parser.add_argument("--html", required=True, metavar="DIR", help="HTML template input directory")
    parser.add_argument("--post", required=True, metavar="DIR", help="XML post input directory")
    parser.add_argument(metavar="input-dir",  dest="indir",  help="Input directory with static files: images, CSS... This will be copied as is to output-dir.")
    parser.add_argument(metavar="output-dir", dest="outdir", help="Output directory")
    args = parser.parse_args()

    if (args.verbose):
        verbose(True)
    if (args.overwrite_all):
        force_overwrite()

    # get the directory of this script
    this_dir = os.path.dirname(os.path.realpath(__file__))
    xslt_dir = os.path.join(this_dir, os.pardir, 'xslt')

    xpost = os.path.join(xslt_dir, 'post.xslt')

    # parse all posts
    #
    # [Post]
    posts = listdir(args.post)          \
                .filter_xml()           \
                .map(functools.partial(make_post, xpost))

    # generate the list of all tags
    #
    # reverse_dict         :  tag               -> tag, [Post]
    # map_values_with_keys :  tag, [Post]       -> tag, Tag
    # map_keys_with_values :  tag, Tag          -> Tag.filename, Tag (group and merge Tags by Tag filename)
    # values               :  Tag.filename, Tag -> [Tag]
    tags = posts.reverse_dict(lambda pi : pi.tags)     \
                .map_values_with_keys(
                    lambda t, pis: Tag(filename=string2id(t)+'.html', value=t, posts=pis)) \
                .map_keys_with_values(                  \
                    lambda t, tag : tag.filename,       \
                    lambda y, z : Tag(filename=y.filename, value=y.value, posts=y.posts+z.posts)) \
                .values()

    # copy the static files
    copytree(args.indir, args.outdir, exclude=[args.html, xslt_dir, args.post, args.outdir])

    # generate the actual post HTML files (post.html)
    posts.with_rendering_engine(args.html).with_template('post.html').render_all(
        lambda pi : 'post/{}'.format(pi.basename),
        lambda pi : filter_dict_values_not_none({
            'xmldom'       : pi.xmldom,
            'lang'         : pi.lang,
            'date_orig'    : pi.origdate,
            'date_year'    : pi.year,
            'date_month'   : pi.month,
            'date_day'     : pi.day,
            'date_cmt'     : pi.date_cmt,
            'date_fmt'     : pi.date_fmt,
            'tags'         : pi.tags,
            'path_to_root' : '..',
            'post_body'    : pi.html,
            'post_title'   : pi.title,
            'posts_all'    : posts.all(),
            'tags_all'     : tags.all()
        })
    ).copy_to(args.outdir)

    # generate the actual tag HTML files (tag.html)
    tags.with_rendering_engine(args.html).with_template('tag.html').render_all(
        lambda t : 'tag/{}'.format(t.filename),
        lambda t : {
            'path_to_root' : '..',
            'post_list'    : t.posts,
            'posts_all'    : posts.all(),
            'tag'          : t.value,
            'tags_all'     : tags.all()
        }
    ).copy_to(args.outdir)

    # render index-level HTML templates
    other = listdir(args.html)                                           \
                .filter_html()                                           \
                .map(lambda x,y : os.path.basename(y))                   \
                .filter(lambda x : (x not in ['post.html', 'tag.html'])) \
                .with_rendering_engine(args.html)                        \
                .render_all_templates(                                   \
                    path_to_root = '.',                                  \
                    posts_all    = posts.all(),                          \
                    tags_all     = tags.all())                           \
                .copy_to(args.outdir)
