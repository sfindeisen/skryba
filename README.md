# skryba

Static blog generator. Focus on your content: write your blog posts in lightweight, HTML-friendly XML:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<post orig-date="2019-02-14; St. Valentine's Day">
<tags>holiday; Greece</tags>
<title>Holiday in Greece</title>
<body>
<a href="https://en.wikipedia.org/wiki/Parthenon"><img alt="Parthenon in Athens" src="img/parthenon-in-athens.jpg"/></a>
<p>What a trip!</p>
</body>
</post>
```

Use powerful [Jinja2](http://jinja.pocoo.org/) templates to define your page layout, CSS to make it nice-looking. Skryba will take care of the rest: tags, cross-links, images, output directory layout and multiple language support (i18n).

## [Examples](example/01-blog/)
