#!/usr/bin/python3

import argparse
import functools
import os

from skryba.index import verbose, info, debug, normalize_string, string2id, listdir, copytree

class Post:
    """A single blog post."""
    def __init__(self):
        self.basename = None    # input file base name
        self.title    = None
        self.origdate = None
        self.html     = None
        self.tags     = None    # list of tags (string)

class Tag:
    """A single article tag."""
    def __init__(self, filename=None, value=None, posts=[]):
        self.filename = filename    # filename (base)
        self.value    = value       # Unicode (normalized)
        self.posts    = posts       # list of Post

def make_post(xpost, skryba, filename):
    info("Process post: " + filename)
    basename = os.path.basename(filename)[:-4]    # basename without .xml

    pi = Post()
    pi.basename = '{}.html'.format(basename)
    pi.title = skryba.xpath1('/post/title/text()')
    debug("title: {}".format(pi.title))
    pi.origdate = skryba.xpath1('/post/@orig-date')
    debug("orig date: {}".format(pi.origdate))
    pi.tags = list(filter(bool, map(lambda s : normalize_string(s.strip()), skryba.xpath1('/post/tags/text()').split(';'))))
    debug("tags: {}".format(pi.tags))
    pi.html = skryba.xslt_transform(xpost)

    return pi

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='generate.py',
        description='Generate the complete blog.',
        add_help=True, allow_abbrev=False, epilog="""This program comes with ABSOLUTELY NO WARRANTY.""")

    parser.add_argument("--verbose", required=False, action="store_true", help="verbose processing")
    parser.add_argument("--html", required=True, metavar="DIR", help="HTML template input directory")
    parser.add_argument("--xslt", required=True, metavar="DIR", help="XSLT template input directory")
    parser.add_argument("--post", required=True, metavar="DIR", help="post input directory")
    parser.add_argument(metavar="input-dir",  dest="indir",  help="static files input directory")
    parser.add_argument(metavar="output-dir", dest="outdir", help="output directory; all files will be overwritten!")
    args = parser.parse_args()

    if (args.verbose):
        verbose(True)

    xpost = os.path.join(os.path.dirname(args.xslt), 'post.xslt')
    posts = listdir(args.post)          \
                .filter_xml()           \
                .map(functools.partial(make_post, xpost))

    # main menu (post page)
    menu_post = '\n'.join(posts.map(lambda pi : '<li><a href="./{}">{}</a></li>'.format(pi.basename, pi.title)).all())

    # main menu (tag page)
    menu_tag  = '\n'.join(posts.map(lambda pi : '<li><a href="../{}">{}</a></li>'.format(pi.basename, pi.title)).all())

    # tag -> [Post]
    # tag -> Tag
    # Tag.filename -> Tag (group Posts by Tag filename)
    # [Tag]
    tags = posts.reverse_dict(lambda pi : pi.tags)     \
                .map_values_with_keys(
                    lambda t,
                    pis: Tag(filename=string2id(t)+'.html', value=t, posts=pis)) \
                .map_keys_with_values(                  \
                    lambda t, tag : tag.filename,       \
                    lambda y, z : Tag(filename=y.filename, value=y.value, posts=y.posts+z.posts)) \
                .values()

    # tag cloud (post page)
    tag_cloud_post = '\n'.join(['<li><a href="./tag/{}">{}</a></li>'.format(t.filename, t.value) for t in tags.all()])
    # tag cloud (tag page)
    tag_cloud_tag  = '\n'.join(['<li><a href="./{}">{}</a></li>'.format(t.filename, t.value) for t in tags.all()])

    # copy the static files
    copytree(args.indir, args.outdir, exclude=[args.html, args.xslt, args.post, args.outdir])

    posts.with_rendering_engine(args.html).with_template('post.html').render_all(
        lambda pi : pi.basename,
        lambda pi : {'menu': menu_post, 'post': pi.html, 'tag_cloud': tag_cloud_post}
    ).copy_to(args.outdir)

    tags.with_rendering_engine(args.html).with_template('tag.html').render_all(
        lambda t : 'tag/{}'.format(t.filename),
        lambda t : {'menu': menu_tag,
                    'post_list': '\n'.join(['<a href="../{}">{}</a>'.format(p.basename, p.title) for p in t.posts]),
                    'tag_cloud': tag_cloud_tag}
    ).copy_to(args.outdir)
