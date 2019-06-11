# Example 01: my personal blog

A simple static blog with articles, tags and i18n support.

Use this command to generate:

```shell
export PYTHONPATH=../../src/main/py/skryba/:$PYTHONPATH
../../src/main/py/gen-blog.py --html ./web-template/ --post ./post/ ./web ./out
```

Now, point your web browser to `out/index.html`:

```shell
iceweasel ./out/index.html
```
