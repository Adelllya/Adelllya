"""Raster images inside the panels: Kyoka's art and the portrait photo.

Put the files in tools/source:
    kyoka.jpg   the character art, used as it is
    photo.jpg   a portrait photo (jpg or png), recoloured into the palette
"""
import base64
import io
import os

from PIL import Image, ImageEnhance, ImageOps

import content as C

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "source")


def find(name):
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        path = os.path.join(SOURCE, name + ext)
        if os.path.exists(path):
            return path
    return None


def _rgb(hex_color):
    return tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5))


def cover(im, w, h, focus=(0.5, 0.4)):
    """Crop to the w:h ratio around a focus point, then resize."""
    im = ImageOps.exif_transpose(im).convert("RGB")
    sw, sh = im.size
    ratio = w / float(h)
    if sw / float(sh) > ratio:
        cw, ch = int(sh * ratio), sh
    else:
        cw, ch = sw, int(sw / ratio)
    left = int(max(0, min(sw - cw, sw * focus[0] - cw / 2.0)))
    top = int(max(0, min(sh - ch, sh * focus[1] - ch / 2.0)))
    return im.crop((left, top, left + cw, top + ch)).resize((w, h), Image.LANCZOS)


def duotone(im, stops):
    """Map brightness onto palette colours. stops: [(0..255, '#hex'), ...]"""
    grey = ImageOps.autocontrast(im.convert("L"), cutoff=1)
    grey = ImageEnhance.Contrast(grey).enhance(1.12)
    stops = [(p, _rgb(c)) for p, c in stops]
    lut = []
    for channel in range(3):
        for v in range(256):
            for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
                if p0 <= v <= p1:
                    f = (v - p0) / float(p1 - p0)
                    lut.append(int(round(c0[channel] + (c1[channel] - c0[channel]) * f)))
                    break
    return Image.merge("RGB", [grey] * 3).point(lut)


def data_uri(im, quality=84):
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def tag(uri, x, y, w, h):
    return '<image href="%s" x="%d" y="%d" width="%d" height="%d" preserveAspectRatio="xMidYMid slice"/>' % (uri, x, y, w, h)


def kyoka(w, h):
    path = find("kyoka")
    if not path:
        return None
    return data_uri(cover(Image.open(path), w, h, focus=(0.5, 0.44)), 86)


def portrait(theme, w, h):
    path = find("photo")
    if not path:
        return None
    im = ImageOps.exif_transpose(Image.open(path))
    sw, sh = im.size
    l, t, r, b = C.PHOTO_BOX
    im = cover(im.crop((int(sw * l), int(sh * t), int(sw * r), int(sh * b))), w, h, focus=C.PHOTO_FOCUS)
    if theme.dark:
        stops = [(0, "#0a0812"), (70, "#1b1233"), (150, "#7b4dff"), (215, "#c9b3ff"), (255, "#f1ecfa")]
    else:
        stops = [(0, "#3b2280"), (110, "#6a4bd6"), (200, "#c9b3ff"), (255, "#f5f1ea")]
    return data_uri(duotone(im, stops), 84)


def site(key, crop, w, h):
    """A live-site screenshot, cropped, kept in its own colours."""
    path = find("site-" + key)
    if not path:
        return None
    im = Image.open(path).convert("RGB").crop(crop)
    return data_uri(cover(im, w, h, focus=(0.5, 0.5)), 80)
