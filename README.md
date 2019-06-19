# Skryba - static blog generator

Focus on your content: write your blog posts in lightweight, HTML-friendly XML:

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

Use powerful [Jinja2](http://jinja.pocoo.org/) templates to define your page layout, CSS to make it nice-looking. Skryba will take care of the rest: tags, cross-linking, images, output directory layout and multiple language support (i18n).

## [Examples](example/01-blog/)
