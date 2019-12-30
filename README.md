# Skryba --- static blog generator

Focus on your content. Write your blog posts in a lightweight, HTML-friendly XML:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<post orig-date="1983-10-15; my birthday!" lang="en">
<title>My 1983 birthday</title>
<tags>birthday; presents</tags>
<body>
<p>Today is my birthday!</p>
<img alt="party" src="img/brueghel.png"/>
<p>I got <a href="ibm.xml">this</a>!</p>
</body>
</post>
```

Use powerful [Jinja2](http://jinja.pocoo.org/) templates to define your page layout. For example, here's how you could define your tag page:

```jinja2
{% extends "index.html" %}
{% block title %}Tag: {{ tag }}{% endblock %}
{% block main %}
<h2>Posts for tag: {{ tag }}</h2>

<table class="post-table">
<tr><th>Title</th><th>Date</th><th>Language</th><th>Tags</th></tr>
{% for post in post_list %}
<tr>
<td><a href="./{{ path_to_root }}/post/{{ post.basename }}">{{ post.title }}</a></td>
<td>{{ post.origdate }}</td>
<td>{{ post.lang }}</td>
<td>
{% for tag in post.tags %}
{{ tag }}
{% endfor %}
</td>
</tr>
{% endfor %}
</table>
{% endblock %}
```

In the example above, `tag` and `post_list` are variables exported to your template from Skryba.

Use CSS to make it nice-looking.

Skryba will take care of the rest:

1. tags
2. internal links
3. multiple language support (i18n)
4. images
5. output directory layout.

## Extra features

1. [Bible quotes](./docs/#bible-quote)

## Examples

01. [My personal blog](docs/example/01-blog/)

## [Documentation](./docs/)

## Requirements

1. [Python3](https://www.python.org/)
2. [Jinja2](http://jinja.pocoo.org/)
3. [lxml](https://lxml.de/)

On a Debian-like OS (e.g. Ubuntu), you can try this:

```shell
apt-get install python3-jinja2 python3-lxml
```

## TODO

- [x] batch mode aka overwrite all files without any questions
- [ ] multiple authors
- [ ] language index (list of languages, list of posts per language)
- [ ] Bible quote index
- [ ] highlight current post in the menu
- [ ] post tags: make them links
- [ ] disquss
- [ ] documentation
