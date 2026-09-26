"""Drawing kit for the profile README assets.

Everything here returns plain SVG strings. Text is converted to outlines with
fontTools, because a GitHub README cannot load web fonts.
"""
import math
import os
import re
import urllib.request

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, ".fonts")
ICON_DIR = os.path.join(HERE, "icons")

FONT_URLS = {
    "ChakraPetch-Bold.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/chakrapetch/ChakraPetch-Bold.ttf",
    "ChakraPetch-Medium.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/chakrapetch/ChakraPetch-Medium.ttf",
    "JetBrainsMono-Regular.ttf": "https://raw.githubusercontent.com/JetBrains/JetBrainsMono/master/fonts/ttf/JetBrainsMono-Regular.ttf",
    "JetBrainsMono-Bold.ttf": "https://raw.githubusercontent.com/JetBrains/JetBrainsMono/master/fonts/ttf/JetBrainsMono-Bold.ttf",
    "NotoSansJP-Black.otf": "https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/SubsetOTF/JP/NotoSansJP-Black.otf",
}

# short name -> file
FONT_FILES = {
    "display": "ChakraPetch-Bold.ttf",
    "text": "ChakraPetch-Medium.ttf",
    "mono": "JetBrainsMono-Regular.ttf",
    "monob": "JetBrainsMono-Bold.ttf",
    "jp": "NotoSansJP-Black.otf",
}


def mix(a, b, t):
    """Blend hex colour a towards b by t (0..1)."""
    pa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    pb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join("%02x" % round(x + (y - x) * t) for x, y in zip(pa, pb))


class Theme:
    def __init__(self, name, bg, text, accent, soft, rune, seal, on_accent):
        self.name = name
        self.bg = bg
        self.text = text
        self.accent = accent
        self.soft = soft
        self.rune = rune
        self.seal = seal
        self.on_accent = on_accent
        self.dark = name == "dark"
        # derived surfaces stay inside the palette: they are blends of two tokens
        self.panel = "#1b1233" if self.dark else mix(bg, text, 0.06)
        self.cell = mix(bg, "#1b1233", 0.55) if self.dark else mix(bg, text, 0.03)
        self.dim = mix(bg, soft, 0.55) if self.dark else mix(bg, text, 0.6)
        self.ghost = mix(bg, accent, 0.5) if self.dark else mix(bg, accent, 0.35)
        self.mark = 0.10 if self.dark else 0.08


DARK = Theme("dark", bg="#0a0812", text="#f1ecfa", accent="#7b4dff", soft="#c9b3ff",
             rune="#46e6ff", seal="#e0314f", on_accent="#f1ecfa")
LIGHT = Theme("light", bg="#f5f1ea", text="#3b2280", accent="#6a4bd6", soft="#6a4bd6",
              rune="#0e7c8c", seal="#e0314f", on_accent="#f5f1ea")
THEMES = (DARK, LIGHT)


def n(v):
    """Compact number formatting."""
    s = ("%.2f" % v).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class Font:
    def __init__(self, key):
        path = os.path.join(FONT_DIR, FONT_FILES[key])
        if not os.path.exists(path):
            os.makedirs(FONT_DIR, exist_ok=True)
            print("downloading", FONT_FILES[key])
            urllib.request.urlretrieve(FONT_URLS[FONT_FILES[key]], path)
        self.key = key
        self.tt = TTFont(path)
        self.glyphs = self.tt.getGlyphSet()
        self.cmap = self.tt.getBestCmap()
        self.upm = self.tt["head"].unitsPerEm
        self._paths = {}

    def has(self, ch):
        return ord(ch) in self.cmap

    def name(self, ch):
        return self.cmap[ord(ch)]

    def advance(self, ch):
        return self.glyphs[self.name(ch)].width

    def path(self, ch):
        if ch not in self._paths:
            pen = SVGPathPen(self.glyphs, ntos=lambda v: str(int(round(v))))
            self.glyphs[self.name(ch)].draw(pen)
            self._paths[ch] = pen.getCommands()
        return self._paths[ch]


_fonts = {}


def font(key):
    if key not in _fonts:
        _fonts[key] = Font(key)
    return _fonts[key]


class Doc:
    """One SVG file: collects glyph defs, css and body elements."""

    def __init__(self, w, h, theme, title, radius=14, frame=True, corners="all", fill=None):
        self.w, self.h, self.t = w, h, theme
        self.title = title
        self.radius = radius
        self.frame = frame
        self.corners = corners  # all, top or bottom
        self.fill = fill or theme.bg
        self.defs = []
        self.css = []
        self.body = []
        self._glyph_ids = {}

    # ---- text -----------------------------------------------------------
    def _glyph(self, fkey, ch):
        f = font(fkey)
        if not f.has(ch):
            for alt in ("jp", "mono", "display"):
                if font(alt).has(ch):
                    fkey, f = alt, font(alt)
                    break
            else:
                raise ValueError("no glyph for %r" % ch)
        k = (fkey, ch)
        if k not in self._glyph_ids:
            gid = "g%d" % len(self._glyph_ids)
            self._glyph_ids[k] = gid
            d = f.path(ch)
            if d:
                self.defs.append('<path id="%s" d="%s"/>' % (gid, d))
            else:
                self._glyph_ids[k] = None
        return self._glyph_ids[k], f

    def measure(self, s, fkey, size, track=0):
        total = 0
        for ch in s:
            _, f = self._glyph(fkey, ch)
            total += f.advance(ch) * size / f.upm + track
        return total - track if s else 0

    def text(self, x, y, s, fkey="display", size=24, fill=None, track=0,
             anchor="start", opacity=None, extra=""):
        """Outlined text run. x, y is the baseline origin."""
        fill = fill or self.t.text
        width = self.measure(s, fkey, size, track)
        if anchor == "middle":
            x -= width / 2
        elif anchor == "end":
            x -= width
        k = size / 1000.0
        uses = []
        cx = 0.0
        for ch in s:
            gid, f = self._glyph(fkey, ch)
            if gid:
                uses.append('<use href="#%s" x="%s"/>' % (gid, n(cx / k)))
            cx += f.advance(ch) * size / f.upm + track
        op = ' opacity="%s"' % n(opacity) if opacity is not None else ""
        return '<g transform="translate(%s %s) scale(%s -%s)" fill="%s"%s%s>%s</g>' % (
            n(x), n(y), n4(k), n4(k), fill, op, extra, "".join(uses))

    def vtext(self, x, y, s, size=18, fill=None, gap=1.12, opacity=None):
        """Vertical (tategaki) run of CJK glyphs, x is the column centre, y the top."""
        fill = fill or self.t.soft
        k = size / 1000.0
        out = []
        for i, ch in enumerate(s):
            gid, f = self._glyph("jp", ch)
            gx = x - size / 2.0
            gy = y + size * 0.88 + i * size * gap
            if ch in "ー〜":
                out.append('<g transform="translate(%s %s) rotate(90) scale(%s -%s) translate(-500 -380)"><use href="#%s"/></g>' % (
                    n(x), n(gy - size * 0.38), n4(k), n4(k), gid))
            else:
                out.append('<use href="#%s" transform="translate(%s %s) scale(%s -%s)"/>' % (
                    gid, n(gx), n(gy), n4(k), n4(k)))
        op = ' opacity="%s"' % n(opacity) if opacity is not None else ""
        return '<g fill="%s"%s>%s</g>' % (fill, op, "".join(out))

    # ---- assembly -------------------------------------------------------
    def add(self, *parts):
        self.body.extend(parts)

    def style(self, css):
        if css not in self.css:
            self.css.append(css)

    def outline(self, inset):
        """Panel outline. Open sides run past the edge so the frame joins the next piece."""
        i, w, h = inset, self.w, self.h
        r = max(self.radius - inset, 0)
        top = self.corners in ("all", "top")
        bottom = self.corners in ("all", "bottom")
        y0 = i if top else -4
        y1 = h - i if bottom else h + 4
        rt = r if top else 0
        rb = r if bottom else 0
        return ("M%s %sh%sa%s %s 0 0 1 %s %sv%sa%s %s 0 0 1 -%s %sh-%sa%s %s 0 0 1 -%s -%sv-%sa%s %s 0 0 1 %s -%sz" % (
            n(i + rt), n(y0), n(w - 2 * i - 2 * rt), n(rt), n(rt), n(rt), n(rt),
            n(y1 - y0 - rt - rb), n(rb), n(rb), n(rb), n(rb),
            n(w - 2 * i - 2 * rb), n(rb), n(rb), n(rb), n(rb),
            n(y1 - y0 - rt - rb), n(rt), n(rt), n(rt), n(rt)))

    def render(self):
        t = self.t
        out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="%s">' % (
            self.w, self.h, self.w, self.h, esc(self.title))]
        out.append("<title>%s</title>" % esc(self.title))
        if self.css:
            out.append("<style>%s</style>" % "".join(self.css))
        clip = '<clipPath id="card"><path d="%s"/></clipPath>' % self.outline(0)
        out.append("<defs>%s%s</defs>" % (clip, "".join(self.defs)))
        out.append('<g clip-path="url(#card)">')
        out.append('<rect width="%d" height="%d" fill="%s"/>' % (self.w, self.h, self.fill))
        out.extend(self.body)
        out.append("</g>")
        if self.frame:
            out.append('<path d="%s" fill="none" stroke="%s" stroke-opacity=".28" stroke-width="2"/>' % (
                self.outline(1), t.soft))
        out.append("</svg>")
        return "\n".join(out)


def n4(v):
    s = ("%.4f" % v).rstrip("0").rstrip(".")
    return s


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ---- shared primitives ----------------------------------------------------

def scanlines(doc, opacity=0.04):
    doc.defs.append('<pattern id="sl" width="4" height="4" patternUnits="userSpaceOnUse">'
                    '<rect width="4" height="1" fill="%s"/></pattern>' % doc.t.text)
    return '<rect width="%d" height="%d" fill="url(#sl)" opacity="%s"/>' % (doc.w, doc.h, n(opacity))


def brackets(doc, x, y, w, h, size=22, stroke=None, width=2, opacity=1.0):
    """HUD corner brackets around a box."""
    s = size
    d = ("M%s %sv-%sh%s M%s %sh%sv%s M%s %sv%sh-%s M%s %sh-%sv-%s" % (
        n(x), n(y + s), n(s), n(s),
        n(x + w - s), n(y), n(s), n(s),
        n(x + w), n(y + h - s), n(s), n(s),
        n(x + s), n(y + h), n(s), n(s)))
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%s" opacity="%s"/>' % (
        d, stroke or doc.t.soft, n(width), n(opacity))


def rune_eye(doc, x, y, scale=1.0, color=None, blink=False):
    """Original rune eye glyph: almond, iris, three lashes, one tear."""
    c = color or doc.t.rune
    lid = ('<g%s><path d="M-52 0Q0 -40 52 0Q0 40 -52 0Z" fill="none" stroke="%s" stroke-width="6" stroke-linejoin="round"/>'
           '<circle r="14" fill="%s"/></g>') % (' class="blink"' if blink else "", c, c)
    lashes = ('<path d="M-7 -33L0 -60L7 -33Z M-34 -25L-38 -52L-22 -30Z M34 -25L38 -52L22 -30Z" fill="%s"/>' % c)
    tear = '<path d="M-5 31L5 31L8 58Q0 74 -8 58Z" fill="%s"/>' % c
    if blink:
        doc.style(".blink{transform-box:fill-box;transform-origin:center;animation:blink 8s ease-in-out infinite}"
                  "@keyframes blink{0%,90%,100%{transform:scaleY(1)}95%{transform:scaleY(.06)}}")
    return '<g transform="translate(%s %s) scale(%s)">%s%s%s</g>' % (n(x), n(y), n(scale), lashes, lid, tear)


def hanko(doc, x, y, size=76, char="愛", rotate=-5):
    """Crimson seal stamp."""
    t = doc.t
    paper = "#f1ecfa" if t.dark else "#f5f1ea"
    inner = size - 12
    g = ['<g transform="translate(%s %s) rotate(%s)">' % (n(x), n(y), n(rotate))]
    g.append('<rect x="%s" y="%s" width="%s" height="%s" rx="7" fill="%s"/>' % (
        n(-size / 2), n(-size / 2), n(size), n(size), t.seal))
    g.append('<rect x="%s" y="%s" width="%s" height="%s" rx="3" fill="none" stroke="%s" stroke-width="2"/>' % (
        n(-inner / 2), n(-inner / 2), n(inner), n(inner), paper))
    fs = size * 0.62
    g.append(doc.text(0, fs * 0.36, char, "jp", fs, fill=paper, anchor="middle"))
    g.append("</g>")
    return "".join(g)


def motes(doc, count, x0, x1, y_from, rise, seed=7, color=None):
    """Slow motes rising, like a tower waking up."""
    c = color or doc.t.rune
    doc.style("@keyframes rise{0%{transform:translateY(0);opacity:0}15%{opacity:.9}80%{opacity:.5}"
              "100%{transform:translateY(-" + n(rise) + "px);opacity:0}}"
              ".mote{animation:rise linear infinite}")
    out = []
    r = seed
    for i in range(count):
        r = (r * 1103515245 + 12345) % 2147483648
        fx = x0 + (r % 1000) / 1000.0 * (x1 - x0)
        r = (r * 1103515245 + 12345) % 2147483648
        rad = 1.4 + (r % 100) / 100.0 * 2.0
        r = (r * 1103515245 + 12345) % 2147483648
        dur = 9 + (r % 80) / 10.0
        r = (r * 1103515245 + 12345) % 2147483648
        delay = -((r % 1000) / 1000.0) * dur
        out.append('<circle class="mote" cx="%s" cy="%s" r="%s" fill="%s" style="animation-duration:%ss;animation-delay:%ss"/>' % (
            n(fx), n(y_from), n(rad), c, n(dur), n(delay)))
    return "".join(out)


def trace(doc, d, color=None, width=2, delay=0.0, dur=2.4, opacity=0.9):
    """A circuit line that draws itself once."""
    doc.style(".tr{stroke-dasharray:1;stroke-dashoffset:1;animation:tr 2.4s ease-out forwards}"
              "@keyframes tr{to{stroke-dashoffset:0}}")
    return ('<path class="tr" pathLength="1" d="%s" fill="none" stroke="%s" stroke-width="%s" opacity="%s" '
            'stroke-linecap="round" stroke-linejoin="round" style="animation-delay:%ss;animation-duration:%ss"/>') % (
        d, color or doc.t.rune, n(width), n(opacity), n(delay), n(dur))


def node(x, y, color, r=4, filled=False):
    if filled:
        return '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (n(x), n(y), n(r), color)
    return '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="2"/>' % (n(x), n(y), n(r), color)


def icon_path(name):
    """Path data of a 24x24 single-colour icon stored in tools/icons."""
    with open(os.path.join(ICON_DIR, name + ".svg"), encoding="utf-8") as fh:
        src = fh.read()
    return " ".join(re.findall(r'<path[^>]* d="([^"]+)"', src))


def icon(name, x, y, size, fill):
    return '<path transform="translate(%s %s) scale(%s)" fill="%s" d="%s"/>' % (
        n(x), n(y), n4(size / 24.0), fill, icon_path(name))


def slanted_tab(x, y, w, h, fill, slant=26):
    return '<path d="M%s %sH%sL%s %sH%sZ" fill="%s"/>' % (
        n(x), n(y), n(x + w), n(x + w - slant), n(y + h), n(x), fill)


def heart(x, y, size, fill, stroke=None, width=2):
    """Heart container, 24-unit box scaled to size, centred on x, y."""
    d = "M12 21C5 15.5 2 12 2 8.2C2 5.3 4.2 3 7 3C9 3 10.9 4.1 12 6C13.1 4.1 15 3 17 3C19.8 3 22 5.3 22 8.2C22 12 19 15.5 12 21Z"
    st = ' stroke="%s" stroke-width="%s"' % (stroke, n(width)) if stroke else ""
    return '<path transform="translate(%s %s) scale(%s)" d="%s" fill="%s"%s stroke-linejoin="round"/>' % (
        n(x - size / 2.0), n(y - size / 2.0), n4(size / 24.0), d, fill, st)


def halftone(cx, cy, r_in, r_out, step, max_r, fill, clip=None, angle_from=None):
    """Dots shrinking with distance from a disc edge."""
    out = []
    row = 0
    y = cy - r_out
    while y <= cy + r_out:
        off = (step / 2.0) if row % 2 else 0
        x = cx - r_out + off
        while x <= cx + r_out:
            d = math.hypot(x - cx, y - cy)
            if r_in < d <= r_out and (clip is None or clip(x, y)):
                f = 1 - (d - r_in) / (r_out - r_in)
                rad = max_r * f
                if rad > 0.5:
                    out.append('<circle cx="%s" cy="%s" r="%s"/>' % (n(x), n(y), n(rad)))
            x += step
        y += step * 0.866
        row += 1
    return '<g fill="%s">%s</g>' % (fill, "".join(out))
