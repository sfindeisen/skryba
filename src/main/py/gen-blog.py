#!/usr/bin/python3

import argparse
import functools
import os

from skryba.index import verbose, info, debug, normalize_string, string2id, listdir

class Post:
    """A single blog post."""
    def __init__(self):
        self.basename = None    # input file base name
        self.title    = None
        self.origdate = None
        self.html     = None
        self.tags     = None

def make_post(xpost, skryba, filename):
    info("Process post: " + filename)
    basename = os.path.basename(filename)[:-4]    # basename without .xml

    pi = Post()
    pi.basename = basename
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
    parser.add_argument("--out",  required=True, metavar="DIR", help="output directory; all files will be overwritten!")
    args = parser.parse_args()

    if (args.verbose):
        verbose(True)

    xpost = os.path.join(os.path.dirname(args.xslt), 'post.xslt')
    posts = listdir(args.post)          \
                .filter_xml()           \
                .map(functools.partial(make_post, xpost))

    menu  = '\n'.join(posts.map(lambda pi : '<li><a href="{}">{}</a></li>'.format(pi.basename, pi.title)).all())

    tags  = posts.reverse_dict(lambda pi : pi.tags).map_keys_uq(lambda t : (t, string2id(t)))
    tag_cloud = '\n'.join(['<li><a href="./tag/{}">{}</a></li>'.format(k[1],k[0]) for k in tags.all().keys()])

    posts.with_rendering_engine(args.html).with_template('post.html').render_all(
        lambda pi : pi.basename + '.html',
        lambda pi : {'menu': menu, 'post': pi.html, 'tag_cloud': tag_cloud}
    ).copy_to(args.out)

    tags.with_rendering_engine(args.html).with_template('tag.html').render_all(
        lambda t : t[1] + '.html',
        lambda t : {'menu': menu,
                    'post_list': '\n'.join(['<a href="./{}">{}</a>'.format(p.basename, p.title) for p in tags[t]]),
                    'tag_cloud': tag_cloud}
    ).copy_to(args.out)
