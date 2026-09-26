#!/usr/bin/env python3
"""Builds every SVG in /assets, a dark and a light twin of each.

    python3 -m pip install fonttools
    python3 tools/build.py

Edit tools/content.py to change texts, quests and statuses, then run this again.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import panels  # noqa: E402
from kit import THEMES  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
LIMIT = 300 * 1024


def main():
    os.makedirs(OUT, exist_ok=True)
    wanted = set(sys.argv[1:])
    total = 0
    for theme in THEMES:
        for name, make in panels.all_panels(theme):
            if wanted and name not in wanted:
                continue
            svg = make().render()
            path = os.path.join(OUT, "%s-%s.svg" % (name, theme.name))
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(svg)
            size = len(svg.encode("utf-8"))
            total += size
            flag = "  TOO BIG" if size > LIMIT else ""
            print("%-28s %7.1f KB%s" % (os.path.basename(path), size / 1024.0, flag))
    print("total %.1f KB" % (total / 1024.0))


if __name__ == "__main__":
    main()
