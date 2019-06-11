# Example 01: my personal blog

A simple static blog demonstrating the use of: tags, images (`img`), links (`a`), i18n.

Use this command to generate:

```shell
export PYTHONPATH=../../src/main/py/skryba/:$PYTHONPATH
../../src/main/py/gen-blog.py --html ./web-template/ --post ./post/ ./web ./out
```

Now, point your web browser to `out/index.html`:

```shell
iceweasel ./out/index.html
```
