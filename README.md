# Skryba - static blog generator

Focus on your content: write your blog posts in a lightweight, HTML-friendly XML:

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

Use powerful [Jinja2](http://jinja.pocoo.org/) templates to define your page layout.

Use CSS to make it nice-looking.

Skryba will take care of the rest:

* tags
* internal links (cross-links)
* images
* multiple language support (i18n)
* output directory layout.

## Extra features

* Bible quotes

## Examples

01. [My personal blog](example/01-blog/)

## Requirements

On a Debian-like OS, try this:

```shell
apt-get install python3-jinja2 python3-lxml
```

## TODO

- [ ] Bible quote index
- [ ] highlight current post in the menu
- [ ] post tags: make them links
