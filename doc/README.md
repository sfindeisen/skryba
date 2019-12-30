# Skryba --- documentation

## Usage

```
$ gen-blog.py --help
usage: generate.py [-h] [--verbose] [--overwrite-all] --html DIR --post DIR
                   input-dir output-dir

Generates the complete blog by processing input post XML files and input
Jinja2 HTML template files. Each post will result in a corresponding output
HTML file generated in output-dir/post/ . Each tag will result in a
corresponding output HTML file generated in output-dir/tag/ . Jinja2 HTML
template files named post.html and tag.html must be present. Other HTML
template files will be processed in a generic way (see the documentation).
Contents of input-dir will be copied as is to the output-dir.

positional arguments:
  input-dir        Input directory with static files: images, CSS... This will
                   be copied as is to output-dir.
  output-dir       Output directory

optional arguments:
  -h, --help       show this help message and exit
  --verbose        Verbose processing
  --overwrite-all  Overwrite all files without prompting (batch mode)
  --html DIR       HTML template input directory
  --post DIR       XML post input directory

This program comes with ABSOLUTELY NO WARRANTY.
```

## Variables available in Jinja2 templates

### Python data types

```python
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

class Tag:
    """A single article tag."""
    def __init__(self, filename=None, value=None, posts=[]):
        self.filename = filename    # filename (base)
        self.value    = value       # Unicode (normalized)
        self.posts    = posts       # list of Post
```

### Variables available on the post page (`post.html`)

Variable name     | Type          | Related XPath in the input post XML file | Value
------------------|---------------|------------------------------------------|--------------------
`date_cmt`        | string        | `/post/@orig-date`                       | parsed date comment
`date_day`        | int           | `/post/@orig-date`                       | parsed day
`date_fmt`        | string        | `/post/@orig-date`                       | date in the following format: `%a, %d %b %Y` (see [datetime.date.strftime](https://docs.python.org/3/library/datetime.html#datetime.date.strftime))
`date_month`      | int           | `/post/@orig-date`                       | parsed month
`date_orig`       | string        | `/post/@orig-date`                       |
`date_year`       | int           | `/post/@orig-date`                       | parsed year
`lang`            | string        | `/post/@lang`                            |
`path_to_root`    | string        |                                          | relative path to the top-level output directory, e.g.: `..`
`post_body`       | string        | `/post/body`                             | post contents as HTML (rendered using [`post.xslt`](../src/main/xslt/post.xslt))
`post_title`      | string        | `/post/title`                            |
`posts_all`       | list of Post  |                                          | all posts
`tags_all`        | list of Tag   |                                          | all tags
`tags`            | list of Tag   | `/post/tags`                             | all tags for this post

### Variables available on the tag page (`tag.html`)

Variable name     | Type          | Related XPath in the input post XML file | Value
------------------|---------------|------------------------------------------|--------------------
`path_to_root`    | string        |                                          | relative path to the top-level output directory, e.g.: `..`
`post_list`       | list of Post  | `/post/tags`                             | all posts for this tag
`posts_all`       | list of Post  |                                          | all posts
`tag`             | string        | `/post/tags`                             | this tag
`tags_all`        | list of Tag   | `/post/tags`                             | all tags

### Variables available to HTML templates other than `post.html` and `tag.html`

Variable name     | Type          | Related XPath in the input post XML file | Value
------------------|---------------|------------------------------------------|--------------------
`path_to_root`    | string        |                                          | relative path to the top-level output directory, e.g.: `..`
`posts_all`       | list of Post  |                                          | all posts
`tags_all`        | list of Tag   | `/post/tags`                             | all tags
