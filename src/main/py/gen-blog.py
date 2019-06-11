#!/usr/bin/python3

import argparse
import functools
import os
import os.path

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

def make_post(xpost, skryba, filename, **kwargs):
    """Parses post XML file. Returns Post instance."""
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
    pi.html = skryba.xslt_transform(xpost, **kwargs)

    return pi

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='generate.py',
        description='Generate the complete blog.',
        add_help=True, allow_abbrev=False, epilog="""This program comes with ABSOLUTELY NO WARRANTY.""")

    parser.add_argument("--verbose", required=False, action="store_true", help="verbose processing")
    parser.add_argument("--html", required=True, metavar="DIR", help="HTML template input directory")
    parser.add_argument("--post", required=True, metavar="DIR", help="post input directory")
    parser.add_argument(metavar="input-dir",  dest="indir",  help="static files input directory")
    parser.add_argument(metavar="output-dir", dest="outdir", help="output directory; all files will be overwritten!")
    args = parser.parse_args()

    if (args.verbose):
        verbose(True)

    # get the directory of this script
    this_dir = os.path.dirname(os.path.realpath(__file__))
    xslt_dir = os.path.join(this_dir, os.pardir, 'xslt')

    xpost = os.path.join(xslt_dir, 'post.xslt')
    posts = listdir(args.post)          \
                .filter_xml()           \
                .map(functools.partial(make_post, xpost))

    ########################################################
    # menu (post list)
    ########################################################

    post_list_header = '<ul class="skryba-post-list">'
    post_list_footer = '</ul>'

    # generate main menu (post page)
    menu_post  = post_list_header + '\n'.join(posts.map(lambda pi : '<li><a href="./{}">{}</a></li>'.format(pi.basename, pi.title)).all()) + post_list_footer
    # generate main menu (tag page)
    menu_tag   = post_list_header + '\n'.join(posts.map(lambda pi : '<li><a href="../post/{}">{}</a></li>'.format(pi.basename, pi.title)).all()) + post_list_footer
    # generate main menu (index page)
    menu_index = post_list_header + '\n'.join(posts.map(lambda pi : '<li><a href="./post/{}">{}</a></li>'.format(pi.basename, pi.title)).all()) + post_list_footer

    # generate the list of all tags
    #
    # tag -> [Post]
    # tag -> Tag
    # Tag.filename -> Tag (group Posts by Tag filename)
    # [Tag]
    tags = posts.reverse_dict(lambda pi : pi.tags)     \
                .map_values_with_keys(
                    lambda t, pis: Tag(filename=string2id(t)+'.html', value=t, posts=pis)) \
                .map_keys_with_values(                  \
                    lambda t, tag : tag.filename,       \
                    lambda y, z : Tag(filename=y.filename, value=y.value, posts=y.posts+z.posts)) \
                .values()

    ########################################################
    # tag cloud
    ########################################################

    tag_list_header = '<ul class="skryba-tag-list">'
    tag_list_footer = '</ul>'

    # generate tag cloud (post page)
    tag_cloud_post  = tag_list_header + '\n'.join(['<li><a href="../tag/{}">{}</a></li>'.format(t.filename, t.value) for t in tags.all()]) + tag_list_footer
    # generate tag cloud (tag page)
    tag_cloud_tag   = tag_list_header + '\n'.join(['<li><a href="./{}">{}</a></li>'.format(t.filename, t.value) for t in tags.all()]) + tag_list_footer
    # generate tag cloud (index page)
    tag_cloud_index = tag_list_header + '\n'.join(['<li><a href="./tag/{}">{}</a></li>'.format(t.filename, t.value) for t in tags.all()]) + tag_list_footer

    # copy the static files
    copytree(args.indir, args.outdir, exclude=[args.html, xslt_dir, args.post, args.outdir])

    # generate the actual post HTML files (post.html)
    posts.with_rendering_engine(args.html).with_template('post.html').render_all(
        lambda pi : 'post/{}'.format(pi.basename),
        lambda pi : {
            'menu': menu_post,
            'post': pi.html,
            'post_title': pi.title,
            'tag_cloud': tag_cloud_post}
    ).copy_to(args.outdir)

    # generate the actual tag HTML files (tag.html)
    tags.with_rendering_engine(args.html).with_template('tag.html').render_all(
        lambda t : 'tag/{}'.format(t.filename),
        lambda t : {'menu': menu_tag,
                    'tag': t.value,
                    'post_list': post_list_header + '\n'.join(['<li><a href="../post/{}">{}</a></li>'.format(p.basename, p.title) for p in t.posts]) + post_list_footer,
                    'tag_cloud': tag_cloud_tag}
    ).copy_to(args.outdir)

    # render index-level HTML templates
    other = listdir(args.html)                                           \
                .filter_html()                                           \
                .map(lambda x,y : os.path.basename(y))                   \
                .filter(lambda x : (x not in ['post.html', 'tag.html'])) \
                .with_rendering_engine(args.html)                        \
                .render_all_templates(                                   \
                    menu=menu_index,                                     \
                    tag_cloud=tag_cloud_index)                           \
                .copy_to(args.outdir)
