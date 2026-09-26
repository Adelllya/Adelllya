#!/usr/bin/env python3
"""Writes README.md from tools/content.py, so the page and the panels never drift apart.

    python3 tools/readme.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import content as C  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER = "Adelllya"

QUEST_LINKS = {
    "flavor-tree": "https://github.com/Adelllya/Efes-ccl-Flavor",
    "petcare": "https://github.com/Adelllya/Petcare-Web",
    "finance-bridge": "https://github.com/Adelllya/Finance_Bridge",
    "shade": "https://github.com/Adelllya/shade-web",
}

LINK_URLS = {
    "telegram": "https://t.me/ailachu_dev",
    "gmail": "mailto:ailachu.echo@gmail.com",
    "tiktok": "https://www.tiktok.com/@_ailachuchu_",
    "pinterest": "https://pin.it/75PPQTbym",
}

PROFILE = [
    "Computer Science and Information Systems at KBTU, Almaty.",
    "Mostly backend, Python first. Django and DRF.",
    "Browser automation with Selenium and Camoufox, Telegram bots.",
    "Also TypeScript with Angular and React, some C++, Java (OOP), a bit of Unity.",
    "I draw, and I build cosplay props by hand.",
    "Open to small freelance jobs, backend and automation.",
]

NOW = [
    ("Building", "Flavor Tree for OneIdea Championship 2026"),
    ("Studying", "3rd year at KBTU"),
    ("Learning", "browser automation with Selenium and Camoufox"),
    ("Based in", "Almaty, UTC+5"),
]

def picture(name, alt, width="100%", dark=None, light=None):
    dark = dark or "./assets/%s-dark.svg" % name
    light = light or "./assets/%s-light.svg" % name
    return ('<picture>'
            '<source media="(prefers-color-scheme: dark)" srcset="%s">'
            '<source media="(prefers-color-scheme: light)" srcset="%s">'
            '<img src="%s" width="%s" alt="%s">'
            '</picture>') % (dark.replace("&", "&amp;"), light.replace("&", "&amp;"), dark.replace("&", "&amp;"), width, alt)


def block(*items):
    return '<p align="center">\n  ' + "\n  ".join(items) + "\n</p>\n"


def chapter(key):
    for k, tab, title, twin, mark in C.CHAPTERS:
        if k == key:
            return block(picture("chapter-" + key, "%s %s, %s" % (tab, title.title(), twin)))
    raise KeyError(key)


def main():
    out = ["<!-- Panels are built by tools/build.py, this file by tools/readme.py. Texts live in tools/content.py. -->\n"]
    out.append(block(picture("hero", "ailachu, アイラ. %s" % C.TAGLINE)))
    out.append(block(
        picture("status", "Status: %s" % C.STATUS.title()),
        "<br>",
        '<img src="https://komarev.com/ghpvc/?username=%s&amp;style=flat-square&amp;color=7b4dff&amp;label=VISITORS" alt="Profile views">' % USER,
    ))

    out.append(chapter("profile"))
    if os.path.exists(os.path.join(ROOT, "assets", "portrait-dark.svg")):
        out.append(picture("portrait", "Aila", "250").replace(' alt="Aila">', ' alt="Aila" align="right">') + "\n")
    out.append("\n".join("- " + line for line in PROFILE) + "\n")
    out.append("<br>\n\n<b>NOW</b>\n")
    out.append("\n".join("- <b>%s</b> · %s" % pair for pair in NOW) + "\n")
    out.append('<br clear="right">\n')

    out.append(chapter("arsenal"))
    alt = "Inventory: " + "; ".join("%s: %s" % (label.title(), ", ".join(c[1].title() for c in cells)) for label, cells in C.ARSENAL)
    out.append(block(picture("arsenal", alt)))

    out.append(chapter("quests"))
    for i in range(0, len(C.QUESTS), 2):
        row = []
        for q in C.QUESTS[i:i + 2]:
            alt = "Quest %s, %s: %s Stack: %s. Status: %s." % (
                q["num"], q["title"].title(), q["pitch"], q["stack"].title(), q["status"].lower())
            pic = picture("quest-" + q["key"], alt, "49%")
            link = QUEST_LINKS.get(q["key"])
            row.append('<a href="%s">%s</a>' % (link, pic) if link else pic)
        out.append(block(*row))
    row = []
    for sc in C.SHOWCASE:
        if os.path.exists(os.path.join(ROOT, "assets", "site-%s-dark.svg" % sc["key"])):
            pic = picture("site-" + sc["key"], "%s, live site: %s" % (sc["title"].title(), sc["url"]), "49%")
            row.append('<a href="https://%s">%s</a>' % (sc["url"], pic))
    if row:
        out.append(block(*row))
    out.append(block(picture("archive", C.ARCHIVE.title())))
    out.append('<p align="center">\n  Labs: <a href="https://github.com/Adelllya/pp2_2025">pp2_2025</a>'
               ' · <a href="https://github.com/Adelllya/WebDev">WebDev</a>\n</p>\n')

    out.append(chapter("slate"))
    out.append(block(picture("slate", "Slate readout: quests complete, live sites, public repos and languages, refreshed weekly")))

    out.append(chapter("side"))
    out.append(block(picture(
        "side-quests", "Off duty: drawing original characters; cosplay props built by hand, foam, paint, "
                       "way too much hot glue; Kyoka, Thunder Cloud, my original character.")))
    out.append(block('<a href="%s">%s</a>' % (LINK_URLS["tiktok"], picture("badge-tiktok", "TikTok: @_ailachuchu_", "24%"))))

    out.append(chapter("requests"))
    alt = "Request board, open for commissions: " + "; ".join(
        "%s: %s" % (title.title(), ", ".join(lines)) for title, _, lines, _ in C.REQUESTS) + ". Send a request on Telegram @ailachu_dev."
    out.append(block('<a href="%s">%s</a>' % (LINK_URLS["telegram"], picture("requests", alt))))

    out.append(chapter("link"))
    out.append(block(picture("quote", C.QUOTE)))
    row = []
    for key, ico, label, handle in C.LINKS:
        row.append('<a href="%s">%s</a>' % (LINK_URLS[key], picture("badge-" + key, "%s: %s" % (label.title(), handle), "24%")))
    out.append(block(*row))
    out.append(block(picture("terminal", "ailachu@hyrule:~$ " + " / ".join(C.COMMANDS))))
    out.append(block(picture("footer", "A tower at dusk, signed アイラ")))

    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))
    print("README.md written")


if __name__ == "__main__":
    main()
