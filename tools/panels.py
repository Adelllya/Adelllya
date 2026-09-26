"""Every panel of the README, one function each."""
import art
import content as C
import ghdata
import photo
from kit import (Doc, brackets, halftone, hanko, heart, icon, mix, motes, n, node,
                 rune_eye, scanlines, slanted_tab, trace)


def plaque(d, inset=16, cut=22, opacity=0.35):
    """Stone plaque outline with chamfered corners."""
    w, h, i, c = d.w, d.h, inset, cut
    path = "M%s %sH%sL%s %sV%sL%s %sH%sL%s %sV%sZ" % (
        n(i + c), n(i), n(w - i - c), n(w - i), n(i + c), n(h - i - c),
        n(w - i - c), n(h - i), n(i + c), n(i), n(h - i - c), n(i + c))
    return '<path d="%s" fill="none" stroke="%s" stroke-width="2" opacity="%s"/>' % (path, d.t.soft, n(opacity))


# ---- hero -------------------------------------------------------------------

def hero(t):
    d = Doc(1200, 420, t, "ailachu, アイラ. %s" % C.TAGLINE, frame=False)
    cx = 600
    d.add(d.text(38, 322, "雷", "jp", 300, fill=t.soft, opacity=t.mark))

    # storm moon, halftone falloff, lightning
    moon_op = 0.5 if t.dark else 0.3
    d.add('<g opacity="%s">%s</g>' % (n(0.55 if t.dark else 0.4),
                                     halftone(cx, 176, 140, 232, 15, 5.2, t.accent)))
    d.add('<circle cx="%d" cy="176" r="140" fill="%s" opacity="%s"/>' % (cx, t.accent, n(moon_op)))
    bolt = "M756 30L690 104L720 111L648 180L678 187L578 276L632 192L602 185L668 118L638 111L706 30Z"
    d.add('<path d="%s" fill="%s" opacity="%s"/>' % (bolt, t.soft, n(0.5 if t.dark else 0.4)))

    # rune circuitry, traced once
    r = t.rune
    lines = [
        ("M150 16V58L192 100H286", 286, 100, 0.0),
        ("M214 16V44L240 70H352", 352, 70, 0.3),
        ("M16 124H70L100 154V214", 100, 214, 0.5),
        ("M206 404V380L228 358H318", 318, 358, 0.8),
        ("M1184 118H1150L1128 96V58", 1128, 58, 0.2),
        ("M1184 306H1146L1114 338H1004L982 360H896", 896, 360, 0.6),
        ("M986 16V40L960 66H868", 868, 66, 0.9),
    ]
    for path, nx, ny, delay in lines:
        d.add(trace(d, path, r, 2, delay))
        d.add(node(nx, ny, r, 4))
    d.add(plaque(d))

    # name
    size = 150
    base = 236
    d.add('<g transform="translate(-5 -5)">%s</g>' % d.text(cx, base, C.NAME_KANA, "jp", size, fill=t.rune, anchor="middle"))
    d.add('<g transform="translate(5 5)">%s</g>' % d.text(cx, base, C.NAME_KANA, "jp", size, fill=t.accent, anchor="middle"))
    d.add(d.text(cx, base, C.NAME_KANA, "jp", size, fill=t.text, anchor="middle"))
    d.style(".flick{opacity:0;animation:flick 2.6s linear .5s 1}"
            "@keyframes flick{0%{opacity:0}12%{opacity:.85}30%{opacity:0}55%{opacity:0}67%{opacity:.7}100%{opacity:0}}")
    d.add('<g class="flick">%s</g>' % d.text(cx, base, C.NAME_KANA, "jp", size, fill=t.rune, anchor="middle"))

    d.add(d.text(cx + 10, 300, C.NAME_LATIN, "display", 40, fill=t.text, track=20, anchor="middle"))
    d.add(d.text(cx, 338, C.TAGLINE, "text", 22, fill=t.soft, track=0.6, anchor="middle"))
    d.add(d.text(cx, 376, C.READOUT, "mono", 16, fill=t.rune, track=2.4, anchor="middle"))

    # rune eye with a dotted ring
    d.add('<circle cx="1046" cy="196" r="98" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="2 11" opacity=".55"/>' % r)
    d.add('<path d="M1046 74A122 122 0 0 1 1168 196" fill="none" stroke="%s" stroke-width="2" opacity=".4"/>' % r)
    d.add('<path d="M1046 318A122 122 0 0 1 924 196" fill="none" stroke="%s" stroke-width="2" opacity=".4"/>' % r)
    d.add(rune_eye(d, 1046, 190, 1.15, blink=True))

    d.add(hanko(d, 96, 330, 78))
    d.add(d.text(150, 326, "AILA", "mono", 14, fill=t.soft, track=3, opacity=0.8))
    d.add(d.text(150, 346, "EST. 2024", "mono", 14, fill=t.soft, track=3, opacity=0.8))

    d.add(scanlines(d))
    d.style(".scan{animation:scan 14s linear infinite}@keyframes scan{from{transform:translateY(-10px)}to{transform:translateY(430px)}}")
    d.add('<rect class="scan" width="1200" height="2" fill="%s" opacity=".14"/>' % r)
    d.add(motes(d, 14, 60, 1140, 430, 470))
    d.add(brackets(d, 30, 30, 1140, 360, 20, t.rune, 2, 0.8))
    return d


# ---- status strip -------------------------------------------------------------

def status(t):
    d = Doc(1200, 58, t, "Status: %s" % C.STATUS, radius=10)
    d.add(d.text(34, 36, "STATUS", "monob", 17, fill=t.soft, track=4))
    d.style(".pulse{animation:pulse 2.4s ease-in-out infinite}@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}")
    d.add('<rect class="pulse" x="142" y="19" width="9" height="21" fill="%s"/>' % t.rune)
    end = 172 + d.measure(C.STATUS, "mono", 17, 3)
    d.add(d.text(172, 36, C.STATUS, "mono", 17, fill=t.text, track=3))
    d.style(".cur{animation:cur 1.2s steps(1) infinite}@keyframes cur{0%,100%{opacity:1}50%{opacity:0}}")
    d.add('<rect class="cur" x="%s" y="20" width="10" height="20" fill="%s"/>' % (n(end + 10), t.text))
    d.add('<path d="M%s 29H930" stroke="%s" stroke-width="2" opacity=".35"/>' % (n(end + 44), t.rune))
    d.add(node(938, 29, t.rune, 4))
    for i in range(3):
        d.add(heart(972 + i * 30, 29, 22, t.seal))
    d.add(d.text(1166, 36, "LV.03 KBTU", "monob", 16, fill=t.soft, track=2.4, anchor="end"))
    return d


# ---- chapter headers ----------------------------------------------------------

def chapter(t, key, tab, title, twin, mark):
    d = Doc(1200, 112, t, "%s %s, %s" % (tab, title, twin), radius=12)
    d.add(d.text(1012, 112, mark, "jp", 140, fill=t.soft, opacity=t.mark))
    d.style(".gl{animation:gl .9s steps(1) .3s 1 both}"
            "@keyframes gl{0%{transform:translate(-7px,0)}34%{transform:translate(6px,-2px)}67%{transform:translate(-2px,1px)}100%{transform:none}}")
    g = ['<g class="gl">']
    g.append(slanted_tab(24, 22, 246, 68, t.accent, 28))
    g.append('<path d="M274 22h10l-28 68h-10z" fill="%s"/>' % t.rune)
    g.append(d.text(44, 69, tab, "jp", 36, fill=t.on_accent, track=3))
    g.append(rune_eye(d, 212, 55, 0.27, color=t.on_accent))
    g.append("</g>")
    d.add("".join(g))
    d.add(d.text(318, 60, title, "display", 38, fill=t.text, track=11))
    d.add(d.text(320, 90, twin, "jp", 19, fill=t.soft, track=5))
    start = 318 + d.measure(title, "display", 38, 11) + 36
    d.add('<path d="M%s 47H952" stroke="%s" stroke-width="2" opacity=".4"/>' % (n(start), t.rune))
    d.add(node(start - 6, 47, t.rune, 4, filled=True))
    d.add(node(960, 47, t.rune, 4))
    d.add(brackets(d, 12, 12, 1176, 88, 14, t.soft, 2, 0.5))
    return d



# ---- helpers ------------------------------------------------------------------

def fit(d, s, fkey, size, track, maxw):
    """Shrink tracking, then size, until the run fits."""
    while d.measure(s, fkey, size, track) > maxw and size > 9:
        if track > 0.8:
            track -= 0.4
        else:
            size -= 0.5
    return size, track


def wrap(d, s, fkey, size, track, maxw):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if cur and d.measure(trial, fkey, size, track) > maxw:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def chip(d, right, y, label, color, filled=False, cls="", dashed=False):
    """Status chip, right aligned. Returns the svg and the chip's left edge."""
    t = d.t
    size, track = 12.5, 2
    w = d.measure(label, "monob", size, track) + 26
    x = right - w
    box = ('<rect x="%s" y="%s" width="%s" height="26" rx="5" fill="%s" stroke="%s" stroke-width="1.6"%s/>' % (
        n(x), n(y), n(w), color if filled else "none", color, ' stroke-dasharray="5 4"' if dashed else ""))
    txt = d.text(x + 13, y + 17.6, label, "monob", size, fill=t.panel if filled else color, track=track)
    return '<g%s>%s%s</g>' % (' class="%s"' % cls if cls else "", box, txt), x


def grid(d, opacity=0.09, step=28):
    d.defs.append('<pattern id="grid" width="%d" height="%d" patternUnits="userSpaceOnUse">'
                  '<path d="M%d 0H0V%d" fill="none" stroke="%s" stroke-width="1"/></pattern>' % (step, step, step, step, d.t.soft))
    return '<rect width="%d" height="%d" fill="url(#grid)" opacity="%s"/>' % (d.w, d.h, n(opacity))


def num_tab(d, x, y, label, w=86, h=38):
    return slanted_tab(x, y, w, h, d.t.rune, 20) + d.text(x + 20, y + h - 12, label, "monob", 18, fill=d.t.bg, track=2)


# ---- arsenal ------------------------------------------------------------------

def builtin_icon(d, name, x, y, size, fill):
    k = size / 24.0
    if name == "@sql":
        parts = []
        for y0 in (1.5, 8.5, 15.5):
            parts.append("M3 %sc0-1.6 4-2.7 9-2.7s9 1.1 9 2.7v1.6c0 1.6-4 2.7-9 2.7s-9-1.1-9-2.7z" % n(y0 + 2.2))
        return '<path transform="translate(%s %s) scale(%s)" fill="%s" d="%s"/>' % (n(x), n(y), n(k), fill, "".join(parts))
    if name == "@rest":
        return d.text(x + size / 2.0, y + size * 0.8, "{/}", "monob", size * 0.86, fill=fill, anchor="middle")
    raise ValueError(name)


def arsenal(t):
    cw, ch, gap = 188, 116, 12
    x0, top = 200, 36
    rows = len(C.ARSENAL)
    h = top * 2 + rows * ch + (rows - 1) * gap + 34
    d = Doc(1200, h, t, "Arsenal: " + "; ".join(
        "%s: %s" % (label.title(), ", ".join(c[1].title() for c in cells)) for label, cells in C.ARSENAL))
    d.add(grid(d, 0.06))
    d.add(d.text(880, 470, "装", "jp", 440, fill=t.soft, opacity=t.mark * 0.7))
    cells_xy = []
    for r, (label, cells) in enumerate(C.ARSENAL):
        y = top + r * (ch + gap)
        d.add(num_tab(d, 30, y + 16, "%02d" % (r + 1), 74, 32))
        d.add(d.text(32, y + 78, label, "monob", 15, fill=t.soft, track=3))
        d.add('<path d="M32 %sH168" stroke="%s" stroke-width="2" opacity=".35"/>' % (n(y + 92), t.rune))
        for c, (ico, name) in enumerate(cells):
            x = x0 + c * (cw + gap)
            cells_xy.append((x, y))
            equipped = name in C.EQUIPPED
            d.add('<rect x="%s" y="%s" width="%d" height="%d" rx="6" fill="%s" stroke="%s" stroke-width="%s" stroke-opacity="%s"/>' % (
                n(x), n(y), cw, ch, mix(t.cell, t.accent, 0.16) if equipped else t.cell, t.rune,
                2 if equipped else 1, 1 if equipped else 0.5))
            if equipped:
                d.add('<path d="M%s %sh30l-30 30z" fill="%s"/>' % (n(x), n(y), t.rune))
                d.add('<path d="M%s %sl5 5l-5 5l-5 -5z" fill="%s"/>' % (n(x + 9), n(y + 4), t.bg))
            ix, iy, isz = x + cw / 2.0 - 22, y + 20, 44
            if ico.startswith("@"):
                d.add(builtin_icon(d, ico, ix, iy, isz, t.soft))
            else:
                d.add(icon(ico, ix, iy, isz, t.soft))
            size, track = fit(d, name, "mono", 14, 2, cw - 18)
            d.add(d.text(x + cw / 2.0, y + 96, name, "mono", size, fill=t.text, track=track, anchor="middle"))
    # selection cursor stepping through the cells
    frames = []
    count = len(cells_xy)
    for i, (x, y) in enumerate(cells_xy):
        frames.append("%s%%{transform:translate(%spx,%spx)}" % (n(i * 100.0 / count), n(x), n(y)))
    d.style(".sel{animation:sel %ss steps(1) infinite}@keyframes sel{%s}" % (n(count * 1.2), "".join(frames)))
    cur = '<rect x="-1" y="-1" width="%d" height="%d" rx="6" fill="%s" opacity=".1"/>' % (cw + 2, ch + 2, t.soft)
    cur += brackets(d, -5, -5, cw + 10, ch + 10, 20, t.soft, 3, 1)
    d.add('<g class="sel" style="transform:translate(%spx,%spx)">%s</g>' % (n(cells_xy[0][0]), n(cells_xy[0][1]), cur))
    ly = h - 30
    d.add('<path d="M%d %dh18l-18 18z" fill="%s"/>' % (x0, ly - 13, t.rune))
    d.add(d.text(x0 + 30, ly, "EQUIPPED · MAIN STACK", "mono", 13, fill=t.soft, track=2.4))
    d.add(d.text(1164, ly, "%d ITEMS" % count, "mono", 13, fill=t.dim, track=2.4, anchor="end"))
    return d


# ---- quest cards --------------------------------------------------------------

STATUS_STYLE = {
    "COMPLETE": ("rune", False, ""),
    "IN PROGRESS": ("soft", False, "pulse"),
    "SIDE QUEST": ("soft", True, ""),
    "LOCKED": ("dim", False, ""),
}


def quest(t, q):
    locked = q["status"] == "LOCKED"
    fill = mix(t.panel, t.bg, 0.62) if locked else t.panel
    d = Doc(600, 268, t, "Quest %s: %s. %s %s Status: %s." % (
        q["num"], q["title"].title(), q["pitch"], q["stack"].title(), q["status"].title()), radius=12, fill=fill)
    ink = t.dim if locked else t.text
    d.add(grid(d, 0.05 if locked else 0.09))
    d.add(brackets(d, 10, 10, 580, 248, 14, t.soft, 2, 0.45))
    d.add(num_tab(d, 0, 0, q["num"], 92, 40))

    color_key, dashed, cls = STATUS_STYLE[q["status"]]
    if cls == "pulse":
        d.style(".pulse{animation:pulse 2.8s ease-in-out infinite}@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}")
    svg, left = chip(d, 576, 16, q["status"], getattr(t, color_key), cls=cls, dashed=dashed)
    d.add(svg)
    if q.get("live"):
        svg, left = chip(d, left - 8, 16, "LIVE", t.rune, filled=True)
        d.add(svg)

    # vertical caption on the left edge
    d.add(d.vtext(32, 62, q["caption"], 19, fill=t.soft, opacity=0.9))
    ystart = 62 + len(q["caption"]) * 19 * 1.12 + 10
    d.add('<path d="M32 %sV240" stroke="%s" stroke-width="2" opacity=".3"/>' % (n(ystart), t.soft))

    size, track = fit(d, q["title"], "display", 30, 3, 500)
    d.add(d.text(64, 100, q["title"], "display", size, fill=ink, track=track))
    width = 380 if locked else 504
    y = 136
    for line in wrap(d, q["pitch"], "text", 19.5, 0.3, width)[:3]:
        d.add(d.text(64, y, line, "text", 19.5, fill=mix(ink, fill, 0.12), track=0.3))
        y += 27

    if locked:
        d.style(".spin{transform-box:fill-box;transform-origin:center;animation:spin 24s linear infinite}"
                "@keyframes spin{to{transform:rotate(360deg)}}")
        d.add('<g transform="translate(506 142)"><g class="spin"><circle r="50" fill="none" stroke="%s" stroke-width="3" '
              'stroke-dasharray="14 9" opacity=".6"/><circle r="38" fill="none" stroke="%s" stroke-width="1.5" opacity=".4"/>'
              '<path d="M0 -58v10M0 58v-10M-58 0h10M58 0h-10" stroke="%s" stroke-width="3" opacity=".6"/></g></g>' % (t.rune, t.rune, t.rune))
        d.add(art.lock(t, 506, 140, 0.8, t.soft))
        d.style("@keyframes h1{0%,8%{opacity:0}16%,88%{opacity:1}96%,100%{opacity:0}}"
                "@keyframes h2{0%,30%{opacity:0}38%,88%{opacity:1}96%,100%{opacity:0}}"
                "@keyframes h3{0%,52%{opacity:0}60%,88%{opacity:1}96%,100%{opacity:0}}"
                ".h1{animation:h1 10s linear infinite}.h2{animation:h2 10s linear infinite}.h3{animation:h3 10s linear infinite}")
        for i in range(3):
            hx = 80 + i * 40
            d.add('<g class="h%d">%s</g>' % (i + 1, heart(hx, 184, 30, t.seal)))
            d.add(heart(hx, 184, 30, "none", t.seal, 2))

    size, track = fit(d, q["stack"], "mono", 13.5, 1.6, 504)
    d.add(d.text(64, 224, q["stack"], "mono", size, fill=t.dim if locked else t.rune, track=track))
    if q.get("note"):
        size, track = fit(d, q["note"], "mono", 12, 2, 504)
        d.add(d.text(64, 247, q["note"], "mono", size, fill=t.dim, track=track))
    return d


def archive(t):
    d = Doc(1200, 54, t, C.ARCHIVE.title(), radius=10)
    size, track = fit(d, C.ARCHIVE, "mono", 15, 2.4, 1130)
    d.add(d.text(600, 33, C.ARCHIVE, "mono", size, fill=t.soft, track=track, anchor="middle", opacity=0.9))
    return d


# ---- side quests ----------------------------------------------------------------

def side_quests(t):
    d = Doc(1200, 520, t, "Side quests: drawing, cosplay props built by hand, and Kyoka, an original character", frame=True)
    d.add(grid(d, 0.05))
    top, bot, sl = 64, 492, 30
    shapes = [
        (24, 410, 380, 24),
        (424, 806, 776, 394),
        (820, 1176, 1176, 790),
    ]
    info = [
        ("01", "DRAWING", "絵描き", "ORIGINAL CHARACTERS", "落書き"),
        ("02", "COSPLAY PROPS", "手作り", "FOAM, PAINT, WAY TOO MUCH HOT GLUE", "工作"),
        ("03", "KYOKA", "雷雲", "THUNDER CLOUD · ORIGINAL CHARACTER", "雷雲"),
    ]
    paper = "#f1ecfa" if t.dark else "#fbf8f3"
    for i, (xa, xb, xc, xd) in enumerate(shapes):
        path = "M%d %dH%dL%d %dH%dZ" % (xa, top, xb, xc, bot, xd)
        if i == 1:
            path = "M%d %dH%dL%d %dH%dZ" % (xa, top, xb, xc, bot, xd)
        d.defs.append('<clipPath id="p%d"><path d="%s"/></clipPath>' % (i, path))
        g = ['<g clip-path="url(#p%d)">' % i]
        g.append('<path d="%s" fill="%s"/>' % (path, t.panel))
        if i == 0:
            g.append(art.sketch(t, 56, 96, 1.04))
        elif i == 1:
            g.append(art.props(t, 418, 100, 1.0))
            g.append(art.sword(t, 718, 398, 0.98, rotate=16))
            g.append(art.glint(d, 718, 398, 0.98, rotate=16))
            g.append(art.rupee(t, 452, 340, 34))
        else:
            uri = photo.kyoka(780, 700)
            if uri:
                g.append(photo.tag(uri, 788, 64, 390, 350))
            else:
                g.append(art.kyoka(t, 800, 74, 0.95))
        # caption band
        band = min(xa, xd)
        g.append('<rect x="%d" y="412" width="%d" height="90" fill="%s" opacity="%s"/>' % (
            band, max(xb, xc) - band, t.bg, n(0.86 if t.dark else 0.9)))
        g.append('<path d="M%d 412H%d" stroke="%s" stroke-width="2" opacity=".5"/>' % (band, max(xb, xc), t.soft))
        g.append("</g>")
        d.add("".join(g))
        d.add('<path d="%s" fill="none" stroke="%s" stroke-width="2"/>' % (path, t.soft))
        num, title, twin, sub, cap = info[i]
        lx = xd + 26 + (12 if i else 0)
        d.add(d.text(lx, 446, title, "display", 24, fill=t.text, track=4))
        tw = d.measure(title, "display", 24, 4)
        d.add(d.text(lx + tw + 16, 445, twin, "jp", 15, fill=t.soft, track=2))
        size, track = fit(d, sub, "mono", 12.5, 2, (xc - xd) - (120 if i == 2 else 60))
        d.add(d.text(lx, 472, sub, "mono", size, fill=t.rune, track=track))
        d.add(num_tab(d, xa, top, num, 78, 34))
    # the cat sits on the frame of the second panel
    d.add(art.cat(t, 690, top - 80 * 0.66, 0.66, t.soft))
    d.add(hanko(d, 1134, 452, 50, "雷", 6))
    d.add(d.text(24, 40, "OFF DUTY", "monob", 14, fill=t.soft, track=4))
    d.add('<path d="M140 35H560" stroke="%s" stroke-width="2" opacity=".35"/>' % t.rune)
    d.add(node(566, 35, t.rune, 4))
    return d


# ---- link -----------------------------------------------------------------------

def quote(t):
    d = Doc(1200, 176, t, "%s %s" % (C.QUOTE, C.QUOTE_JP))
    d.add(art.sword(t, 150, 160, 0.46))
    d.add(art.glint(d, 150, 160, 0.46))
    d.add(art.sword(t, 1050, 160, 0.46))
    d.add(art.glint(d, 1050, 160, 0.46))
    d.add(d.text(600, 78, C.QUOTE, "display", 34, fill=t.text, track=1.6, anchor="middle"))
    d.add(d.text(600, 112, C.QUOTE_JP, "jp", 15, fill=t.soft, track=5, anchor="middle"))
    d.style(".dn{animation:dn 2.4s ease-in-out infinite}@keyframes dn{0%,100%{opacity:.35;transform:translateY(0)}50%{opacity:1;transform:translateY(4px)}}")
    d.add('<path class="dn" d="M586 134l14 12l14 -12M586 148l14 12l14 -12" fill="none" stroke="%s" stroke-width="3" '
          'stroke-linecap="round" stroke-linejoin="round"/>' % t.rune)
    d.add(brackets(d, 14, 14, 1172, 148, 16, t.soft, 2, 0.5))
    return d


def badge(t, key, ico, label, handle):
    d = Doc(282, 78, t, "%s: %s" % (label.title(), handle), radius=10, fill=t.panel)
    d.add('<rect x="0" y="0" width="62" height="78" fill="%s" opacity="%s"/>' % (t.rune, n(0.12 if t.dark else 0.1)))
    d.add(icon(ico, 16, 24, 30, t.rune))
    d.add(d.text(78, 32, label, "monob", 13, fill=t.soft, track=3))
    size, track = fit(d, handle, "text", 19, 0.4, 190)
    d.add(d.text(78, 58, handle, "text", size, fill=t.text, track=track))
    d.add('<path d="M254 22l10 0l0 10M264 22l-12 12" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round" opacity=".8"/>' % t.soft)
    return d


def terminal(t):
    """Closing terminal: commands type themselves one after another, then loop."""
    d = Doc(1200, 66, t, "ailachu@hyrule:~$ " + " / ".join(C.COMMANDS), radius=10, fill=t.panel)
    for i in range(3):
        d.add('<circle cx="%d" cy="33" r="6" fill="%s" opacity="%s"/>' % (34 + i * 22, t.soft, n(0.9 - i * 0.25)))
    size, track = 20, 0.6
    x = 116
    for run, color in (("ailachu@hyrule", t.rune), (":", t.text), ("~", t.soft), ("$ ", t.text)):
        d.add(d.text(x, 40, run, "mono", size, fill=color, track=track))
        x += d.measure(run, "mono", size, track) + track
    slot = 4.0
    total = slot * len(C.COMMANDS)
    share = 100.0 / len(C.COMMANDS)
    for i, cmd in enumerate(C.COMMANDS):
        w = d.measure(cmd, "mono", size, track) + track
        typing = share * 0.45
        d.style(".c%d{opacity:0;animation:c%d %ss linear %ss infinite}"
                "@keyframes c%d{0%%,%s%%{opacity:1}%s%%,100%%{opacity:0}}" % (
                    i, i, n(total), n(i * slot), i, n(share - 0.01), n(share)))
        d.style(".k%d{animation:k%d %ss linear %ss infinite}"
                "@keyframes k%d{0%%{transform:translateX(0);animation-timing-function:steps(%d,end)}"
                "%s%%,100%%{transform:translateX(%spx)}}" % (
                    i, i, n(total), n(i * slot), i, len(cmd), n(typing), n(w)))
        cover = ('<g class="k%d"><rect x="%s" y="14" width="%s" height="38" fill="%s"/>'
                 '<rect x="%s" y="21" width="12" height="24" fill="%s"/></g>') % (
            i, n(x), n(w + 30), t.panel, n(x + 2), t.rune)
        d.add('<g class="c%d">%s%s</g>' % (i, d.text(x, 40, cmd, "mono", size, fill=t.text, track=track), cover))
    return d


# ---- showcase -------------------------------------------------------------------

def showcase(t, s):
    """Browser window with a screenshot of a live site."""
    iw, ih = 568, 340
    uri = photo.site(s["key"], s["crop"], iw * 2, ih * 2)
    if not uri:
        return None
    d = Doc(600, 470, t, "%s, live at %s" % (s["title"].title(), s["url"]), radius=12, fill=t.panel)
    # title bar
    for i in range(3):
        d.add('<circle cx="%d" cy="26" r="6" fill="%s" opacity="%s"/>' % (30 + i * 20, t.soft, n(0.9 - i * 0.25)))
    d.add('<rect x="104" y="12" width="392" height="28" rx="14" fill="%s" stroke="%s" stroke-opacity=".35"/>' % (t.bg, t.soft))
    d.add('<path d="M122 22v-3a4 4 0 0 1 8 0v3M119 22h14v10h-14z" fill="none" stroke="%s" stroke-width="1.8"/>' % t.rune)
    size, track = fit(d, s["url"], "mono", 14, 1, 330)
    d.add(d.text(144, 31, s["url"], "mono", size, fill=t.text, track=track))
    svg, _ = chip(d, 584, 13, "LIVE", t.rune, filled=True)
    d.add(svg)
    # screen
    x, y = 16, 52
    d.defs.append('<clipPath id="scr"><rect x="%d" y="%d" width="%d" height="%d" rx="6"/></clipPath>' % (x, y, iw, ih))
    d.add('<g clip-path="url(#scr)">%s%s</g>' % (photo.tag(uri, x, y, iw, ih), scanlines(d, 0.035)))
    d.add('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="none" stroke="%s" stroke-opacity=".5"/>' % (x, y, iw, ih, t.soft))
    d.add(brackets(d, x - 6, y - 6, iw + 12, ih + 12, 18, t.rune, 2, 0.9))
    # caption
    d.add(d.text(24, 434, s["title"], "display", 26, fill=t.text, track=4))
    d.add(d.text(24, 456, "OPEN THE SITE ▸", "mono", 12.5, fill=t.rune, track=2.4))
    d.add(d.text(576, 434, "画面", "jp", 20, fill=t.soft, track=4, anchor="end", opacity=0.8))
    return d


# ---- slate readout --------------------------------------------------------------

def slate(t):
    data = ghdata.load(refresh=True)
    done = sum(1 for q in C.QUESTS if q["status"] == "COMPLETE")
    live = sum(1 for q in C.QUESTS if q.get("live"))
    d = Doc(1200, 430, t, "Slate readout: %d of %d quests complete, %d live sites, %d public repos, on GitHub since %s. Languages: %s." % (
        done, len(C.QUESTS), live, data["public_repos"], data["since"],
        ", ".join(lang for lang, _ in data["languages"][:6])), radius=26, fill=t.panel)
    d.defs.append('<radialGradient id="glow"><stop offset="0" stop-color="%s" stop-opacity=".34"/>'
                  '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (t.rune, t.rune))
    d.add('<ellipse cx="600" cy="44" rx="320" ry="80" fill="url(#glow)"/>')
    d.add(rune_eye(d, 600, 40, 0.46, blink=True))
    d.add(d.text(44, 48, "SLATE // GITHUB READOUT", "mono", 14, fill=t.soft, track=3))
    d.add(d.text(1156, 48, "SYNCED %s" % data["fetched"], "mono", 14, fill=t.soft, track=3, anchor="end"))
    d.add('<path d="M28 86V76H1172V86" fill="none" stroke="%s" stroke-width="2" opacity=".5"/>' % t.rune)

    # screen
    sx, sy, sw, sh = 28, 96, 1144, 272
    d.add('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s"/>' % (sx, sy, sw, sh, t.bg))
    d.add('<g opacity=".6">%s</g>' % grid(d, 0.07, 24))

    tiles = [
        ("QUESTS COMPLETE", "%d/%d" % (done, len(C.QUESTS)), "クリア"),
        ("LIVE SITES", str(live), "公開"),
        ("PUBLIC REPOS", str(data["public_repos"]), "倉庫"),
        ("ON GITHUB SINCE", data["since"], "開始"),
    ]
    tw, th = 250, 112
    for i, (label, value, jp) in enumerate(tiles):
        tx = sx + 24 + (i % 2) * (tw + 16)
        ty = sy + 20 + (i // 2) * (th + 16)
        d.add('<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="%s" stroke="%s" stroke-opacity=".4"/>' % (tx, ty, tw, th, t.cell, t.rune))
        d.add('<rect x="%d" y="%d" width="4" height="%d" fill="%s"/>' % (tx, ty + 18, th - 36, t.rune))
        d.add(d.text(tx + 22, ty + 34, label, "mono", 13, fill=t.soft, track=2.4))
        d.add(d.text(tx + 22, ty + 90, value, "display", 46, fill=t.text, track=2))
        d.add(d.text(tx + tw - 18, ty + 90, jp, "jp", 16, fill=t.soft, track=2, anchor="end", opacity=0.7))

    # languages
    lx, ly, lw = sx + 580, sy + 20, 520
    d.add(d.text(lx, ly + 20, "LANGUAGES · BYTES OF CODE IN PUBLIC REPOS", "mono", 13, fill=t.soft, track=2.4))
    langs = data["languages"][:6]
    total = float(sum(size for _, size in data["languages"])) or 1.0
    shades = [t.accent, t.rune, t.soft if t.dark else t.text, mix(t.accent, t.bg, 0.45), mix(t.rune, t.bg, 0.45), t.dim]
    bx = lx
    bar_y = ly + 40
    for i, (lang, size) in enumerate(langs):
        bw = lw * size / total
        d.add('<rect x="%s" y="%d" width="%s" height="18" fill="%s"/>' % (n(bx), bar_y, n(max(bw - 2, 1.5)), shades[i]))
        bx += bw
    d.add('<rect x="%d" y="%d" width="%d" height="18" fill="none" stroke="%s" stroke-opacity=".3"/>' % (lx, bar_y, lw, t.soft))
    for i, (lang, size) in enumerate(langs):
        cx = lx + (i % 2) * 270
        cy = bar_y + 60 + (i // 2) * 44
        d.add('<rect x="%d" y="%d" width="14" height="14" rx="3" fill="%s"/>' % (cx, cy - 12, shades[i]))
        d.add(d.text(cx + 26, cy, lang.upper(), "mono", 15, fill=t.text, track=2))
        d.add(d.text(cx + 240, cy, "%.1f%%" % (100 * size / total), "mono", 15, fill=t.soft, track=1, anchor="end"))
    d.add('<path d="M%d %dV%d" stroke="%s" stroke-width="2" opacity=".25"/>' % (lx - 30, sy + 24, sy + sh - 24, t.soft))

    # bottom bar
    d.add('<path d="M28 378V388H1172V378" fill="none" stroke="%s" stroke-width="2" opacity=".5"/>' % t.rune)
    d.add(d.text(44, 414, "LAST PUSH %s" % (data["last_push"] or "-"), "mono", 13, fill=t.soft, track=2.4))
    d.add('<rect x="530" y="404" width="140" height="7" rx="3.5" fill="%s" opacity=".55"/>' % t.soft)
    d.add(d.text(1156, 414, "REFRESHED WEEKLY", "mono", 13, fill=t.soft, track=2.4, anchor="end"))
    return d


# ---- requests -------------------------------------------------------------------

def requests_board(t):
    d = Doc(1200, 420, t, "Request board, open for commissions: " + "; ".join(
        "%s: %s" % (title.title(), ", ".join(lines)) for title, _, lines, _ in C.REQUESTS)
        + ". Send a request on Telegram @ailachu_dev.", fill=t.bg)
    d.add(grid(d, 0.05))
    d.add(d.text(24, 44, "REQUEST BOARD", "monob", 16, fill=t.soft, track=4))
    d.add(d.text(214, 43, "依頼板", "jp", 17, fill=t.soft, track=4))
    d.style(".pulse{animation:pulse 2.4s ease-in-out infinite}@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}")
    svg, _ = chip(d, 1176, 22, "OPEN FOR COMMISSIONS", t.rune, cls="pulse")
    d.add(svg)
    cw, gap, top = 276, 12, 70
    for i, (title, ico, lines, proof) in enumerate(C.REQUESTS):
        x = 24 + i * (cw + gap)
        path = "M%d %dH%dV%dL%d %dH%dZ" % (x, top, x + cw, top + 246, x + cw - 22, top + 268, x)
        d.add('<path d="%s" fill="%s" stroke="%s" stroke-width="2" stroke-opacity=".7"/>' % (path, t.panel, t.soft))
        d.add(num_tab(d, x, top, "%02d" % (i + 1), 70, 32))
        d.add('<circle cx="%d" cy="%d" r="30" fill="%s" opacity="%s"/>' % (x + cw - 50, top + 58, t.rune, n(0.12 if t.dark else 0.1)))
        d.add(icon(ico, x + cw - 68, top + 40, 36, t.rune))
        size, track = fit(d, title, "display", 22, 3, cw - 40)
        d.add(d.text(x + 20, top + 124, title, "display", size, fill=t.text, track=track))
        for j, line in enumerate(lines):
            ly = top + 158 + j * 26
            d.add('<path d="M%d %dl5 5l-5 5l-5 -5z" fill="%s"/>' % (x + 24, ly - 11, t.rune))
            size, track = fit(d, line, "text", 16.5, 0.2, cw - 60)
            d.add(d.text(x + 38, ly, line, "text", size, fill=mix(t.text, t.panel, 0.1), track=track))
        size, track = fit(d, proof, "mono", 11.5, 1.6, cw - 40)
        d.add(d.text(x + 20, top + 250, proof, "mono", size, fill=t.dim, track=track))
    # call to action
    d.add('<rect x="24" y="358" width="1152" height="46" rx="8" fill="%s" opacity="%s"/>' % (t.accent, n(0.2 if t.dark else 0.14)))
    d.add('<rect x="24" y="358" width="1152" height="46" rx="8" fill="none" stroke="%s" stroke-opacity=".6"/>' % t.accent)
    d.add(icon("telegram", 44, 369, 24, t.rune))
    d.add(d.text(84, 388, "SEND A REQUEST", "monob", 15, fill=t.text, track=3))
    d.add(d.text(270, 388, "Telegram @ailachu_dev · a few lines about the task are enough to start", "text", 17, fill=t.soft, track=0.2))
    d.add('<path d="M1146 374l10 7l-10 7" fill="none" stroke="%s" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>' % t.rune)
    return d


# ---- footer ---------------------------------------------------------------------

def footer(t):
    d = Doc(1200, 260, t, "A tower at dusk. アイラ", frame=False)
    ink = "#0a0812" if t.dark else "#3b2280"
    d.add('<g opacity="%s">%s</g>' % (n(0.5 if t.dark else 0.4), halftone(640, 190, 96, 170, 15, 4.6, t.accent)))
    d.add('<circle cx="640" cy="190" r="96" fill="%s" opacity="%s"/>' % (t.accent, n(0.5 if t.dark else 0.3)))
    far = mix(t.bg, t.accent, 0.22)
    near = mix(t.bg, t.accent, 0.34) if t.dark else mix(t.bg, t.accent, 0.42)
    d.add('<path d="M0 214L90 176L170 200L280 150L380 196L470 170L560 206L680 160L790 200L900 172L1010 206L1110 178L1200 204V260H0Z" fill="%s"/>' % far)
    d.add(art.tower(t, 330, 238, 0.92))
    d.style(".spine{stroke-dasharray:.22 .78;animation:spine 6s linear infinite}@keyframes spine{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}")
    d.add('<path d="M330 236V100" stroke="%s" stroke-width="2" opacity=".35"/>' % t.rune)
    d.add('<path class="spine" pathLength="1" d="M330 236V100" stroke="%s" stroke-width="3.5" stroke-linecap="round"/>' % t.rune)
    d.add('<path d="M0 238C120 224 220 232 330 236C470 240 560 222 700 232C860 242 1010 224 1200 236V260H0Z" fill="%s"/>' % near)
    d.add(motes(d, 12, 120, 560, 250, 250, seed=11))
    d.add(d.text(1076, 150, C.NAME_KANA, "jp", 44, fill=t.text, track=6, anchor="end"))
    d.add(d.text(1076, 182, "END OF LOG", "mono", 13, fill=t.soft, track=3, anchor="end"))
    d.add(hanko(d, 1128, 142, 62))
    d.add(scanlines(d))
    d.add(brackets(d, 24, 24, 1152, 212, 18, t.rune, 2, 0.7))
    return d


# ---- portrait ---------------------------------------------------------------------

def portrait(t):
    """Photo card for the profile chapter. Built only when tools/source/photo.* exists."""
    uri = photo.portrait(t, 920, 1080)
    if not uri:
        return None
    d = Doc(520, 720, t, "Aila", radius=14, fill=t.panel)
    d.add(grid(d, 0.07))
    x, y, w, h = 30, 66, 460, 540
    cut = 26
    shape = "M%d %dH%dL%d %dV%dH%dL%d %dZ" % (x + cut, y, x + w, x + w, y, y + h - cut, x + w - cut, x, y + h)
    shape = "M%d %dH%dV%dL%d %dH%dV%dZ" % (x + cut, y, x + w, y + h - cut, x + w - cut, y + h, x, y + cut)
    d.defs.append('<clipPath id="ph"><path d="%s"/></clipPath>' % shape)
    # misregistered frames behind the photo
    d.add('<path d="%s" transform="translate(-7 -7)" fill="none" stroke="%s" stroke-width="3"/>' % (shape, t.rune))
    d.add('<path d="%s" transform="translate(7 7)" fill="none" stroke="%s" stroke-width="3"/>' % (shape, t.accent))
    d.add('<g clip-path="url(#ph)">%s%s</g>' % (photo.tag(uri, x, y, w, h), scanlines(d, 0.07)))
    d.add('<path d="%s" fill="none" stroke="%s" stroke-width="2"/>' % (shape, t.soft))
    d.add(brackets(d, x + 14, y + 14, w - 28, h - 28, 22, t.rune, 2, 0.9))
    d.add(num_tab(d, 0, 0, "P1", 92, 40))
    d.add(d.text(496, 40, "PLAYER ONE", "monob", 17, fill=t.soft, track=4, anchor="end"))
    d.add('<rect x="%d" y="%d" width="38" height="96" fill="%s" opacity=".9"/>' % (x + w - 62, y + 40, t.panel))
    d.add('<rect x="%d" y="%d" width="38" height="4" fill="%s"/>' % (x + w - 62, y + 40, t.rune))
    d.add(d.vtext(x + w - 43, y + 52, "開発者", 22, fill=t.text))
    d.add(d.text(30, 664, "AILA", "display", 44, fill=t.text, track=8))
    d.add(d.text(200, 662, C.NAME_KANA, "jp", 24, fill=t.soft, track=5))
    d.add(d.text(30, 698, "BACKEND · ALMATY", "mono", 18, fill=t.rune, track=3))
    d.add(hanko(d, 450, 662, 66))
    return d


def all_panels(t):
    """(name, builder) pairs. Builders run only for the panels being built."""
    if photo.find("photo"):
        yield "portrait", lambda: portrait(t)
    yield "hero", lambda: hero(t)
    yield "status", lambda: status(t)
    for key, tab, title, twin, mark in C.CHAPTERS:
        yield "chapter-" + key, (lambda a=(key, tab, title, twin, mark): chapter(t, *a))
    yield "arsenal", lambda: arsenal(t)
    for q in C.QUESTS:
        yield "quest-" + q["key"], (lambda q=q: quest(t, q))
    for sc in C.SHOWCASE:
        if photo.find("site-" + sc["key"]):
            yield "site-" + sc["key"], (lambda sc=sc: showcase(t, sc))
    yield "archive", lambda: archive(t)
    yield "slate", lambda: slate(t)
    yield "side-quests", lambda: side_quests(t)
    yield "requests", lambda: requests_board(t)
    yield "quote", lambda: quote(t)
    for key, ico, label, handle in C.LINKS:
        yield "badge-" + key, (lambda a=(key, ico, label, handle): badge(t, *a))
    yield "terminal", lambda: terminal(t)
    yield "footer", lambda: footer(t)
