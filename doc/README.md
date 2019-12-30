# Documentation

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

### Variables available on the tag page (`tag.html`)

Variable name     | Type          | Related XPath in the input post XML file | Value
------------------|---------------|------------------------------------------|--------------------
`path_to_root`    | string        |                                          | relative path to the top-level output directory, e.g.: `..`
`post_list`       | list of Post  | `/post/tags`                             | posts for this tag
`posts_all`       | list of Post  |                                          | all posts
`tag`             | string        | `/post/tags`                             | this tag
`tags_all`        | list of Tag   | `/post/tags`                             | all tags

### Variables available on the post page (`post.html`)

Variable name     | Type          | Related XPath in the input post XML file | Value
------------------|---------------|------------------------------------------|--------------------
`lang`            | string        | `/post/@lang`                            |
`date_orig`       | string        | `/post/@orig-date`                       |
`date_year`       | int           | `/post/@orig-date`                       | parsed year
`date_month`      | int           | `/post/@orig-date`                       | parsed month
`date_day`        | int           | `/post/@orig-date`                       | parsed day
`date_cmt`        | string        | `/post/@orig-date`                       | parsed date comment
`date_fmt`        | string        | `/post/@orig-date`                       | date in the following format: `%a, %d %b %Y` (see [strftime](https://docs.python.org/3/library/datetime.html#datetime.date.strftime))
`path_to_root`    | string        |                                          | relative path to the top-level output directory, e.g.: `..`
`posts_all`       | list of Post  |                                          | all posts
`tags_all`        | list of Tag   |                                          | all tags
