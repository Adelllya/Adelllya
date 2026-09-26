#!/usr/bin/env python3
"""Builds a local page that shows README.md roughly the way GitHub does, in both themes.

    python3 tools/preview.py   ->  tools/.preview/preview-dark.html and preview-light.html
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tools", ".preview")

PAGE = """<!doctype html><meta charset="utf-8"><title>README preview, %(name)s</title>
<style>
body{margin:0;background:%(page)s;color:%(text)s;font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
main{width:846px;margin:24px auto;padding:24px;border:1px solid %(line)s;border-radius:6px}
p{margin:0 0 16px}img{max-width:100%%;vertical-align:middle;border:0}a{color:%(link)s;text-decoration:none}
ul{padding-left:2em;margin:0 0 16px}
</style><main>%(body)s</main>"""

THEMES = {
    "dark": dict(name="dark", page="#0d1117", text="#f0f6fc", line="#3d444d", link="#4493f8"),
    "light": dict(name="light", page="#ffffff", text="#1f2328", line="#d1d9e0", link="#0969da"),
}


def to_html(md, theme):
    other = "light" if theme == "dark" else "dark"
    md = re.sub(r'<source media="\(prefers-color-scheme: %s\)" srcset="[^"]*">' % other, "", md)
    md = re.sub(r'<source media="\(prefers-color-scheme: %s\)" srcset="([^"]*)"><img src="[^"]*"' % theme,
                r'<img src="\1"', md)
    md = md.replace('="./assets/', '="../../assets/')
    lines, out, in_list = md.split("\n"), [], False
    for line in lines:
        if line.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append("<li>%s</li>" % line[2:])
        else:
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(line)
    return "\n".join(out)


def main():
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
        md = fh.read()
    for name, theme in THEMES.items():
        page = PAGE % dict(theme, body=to_html(md, name))
        path = os.path.join(OUT, "preview-%s.html" % name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(page)
        print(path)


if __name__ == "__main__":
    main()
