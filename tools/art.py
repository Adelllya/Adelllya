"""Original flat-vector illustrations. All drawn by hand in code, in the palette."""
from kit import halftone, mix, n


def _ink(t):
    return "#0a0812" if t.dark else "#3b2280"


def kyoka(t, x, y, scale=1.0):
    """Kyoka, "Thunder Cloud": profile bust in a 360 x 360 box, facing right."""
    ink = _ink(t)
    hair = t.accent
    hair_d = mix(t.accent, "#0a0812", 0.38) if t.dark else mix(t.accent, "#3b2280", 0.55)
    hair_l = t.soft if t.dark else mix(t.accent, "#f5f1ea", 0.45)
    skin = "#f1ecfa" if t.dark else "#fbf8f3"
    shade = mix(skin, t.accent, 0.22)
    cloth = "#1b1233" if t.dark else "#3b2280"
    cloth_l = mix(cloth, t.accent, 0.45)
    cape = t.soft if t.dark else mix(t.accent, "#f5f1ea", 0.55)
    g = ['<g transform="translate(%s %s) scale(%s)">' % (n(x), n(y), n(scale))]

    # ponytail behind everything
    g.append('<path d="M150 66C138 14 66 0 38 44C8 92 40 150 28 214C20 262 34 318 62 360H150C126 322 122 282 134 240'
             'C150 190 136 140 168 96Z" fill="%s"/>' % hair)
    g.append('<path d="M112 40C70 34 50 66 52 110C54 160 74 196 64 250C58 290 70 330 88 360H116C98 322 96 286 106 246'
             'C120 192 100 150 100 108C100 78 108 58 128 48Z" fill="%s"/>' % hair_d)
    g.append('<path d="M60 70C48 104 66 140 60 186C56 214 48 232 50 262C62 232 76 210 78 178C80 140 62 108 60 70Z" fill="%s"/>' % hair_l)

    # back hair under the head
    g.append('<path d="M128 108C118 150 124 196 150 232L196 214L178 150Z" fill="%s"/>' % hair_d)

    # neck and shoulders
    g.append('<path d="M168 176L166 222C166 232 204 236 210 222L206 182Z" fill="%s"/>' % shade)
    g.append('<path d="M92 360C90 300 110 250 162 226C178 240 200 240 214 224C262 238 288 280 292 360Z" fill="%s"/>' % cloth)
    g.append('<path d="M162 226C150 262 118 300 84 318C88 284 106 250 142 232Z" fill="%s"/>' % cape)
    g.append('<path d="M214 224C236 250 262 264 292 268C282 244 258 230 232 224Z" fill="%s"/>' % cape)
    g.append('<path d="M176 250C190 262 204 262 216 250L210 300C200 312 188 312 180 300Z" fill="%s"/>' % cloth_l)
    # choker
    g.append('<path d="M166 200C180 208 196 208 209 200L210 212C196 220 180 220 166 212Z" fill="%s"/>' % ink)
    g.append('<circle cx="190" cy="214" r="4" fill="%s"/>' % t.soft)
    # crimson cord at the waist
    g.append('<path d="M112 334C160 346 230 346 284 330L286 346C232 360 160 360 110 350Z" fill="%s"/>' % t.seal)
    g.append('<path d="M196 342C186 330 172 330 170 340C168 350 184 352 196 346C208 352 224 350 222 340C220 330 206 330 196 342Z" fill="%s"/>' % t.seal)

    # face, profile to the right
    g.append('<path d="M140 92C150 62 196 56 212 84C218 96 222 106 221 116L219 124L234 142C236 146 232 148 224 148'
             'L226 155L221 159L224 165L220 172C220 184 210 192 198 190L176 184C154 176 138 150 138 122Z" fill="%s"/>' % skin)
    g.append('<path d="M176 184L198 190C206 191 212 188 216 182C204 184 190 180 176 170Z" fill="%s"/>' % shade)
    # ear
    g.append('<path d="M160 128C150 122 146 134 150 144C154 154 162 156 166 150Z" fill="%s"/>' % shade)
    # eye
    g.append('<path d="M196 120C202 114 212 113 219 117L217 121C211 119 204 120 199 124Z" fill="%s"/>' % ink)
    g.append('<path d="M203 122C208 120 213 120 216 122C217 130 214 139 209 141C204 138 202 130 203 122Z" fill="%s"/>' % hair)
    g.append('<path d="M207 125C210 124 213 124 215 125C215 130 213 135 210 137C207 134 206 130 207 125Z" fill="%s"/>' % ink)
    g.append('<circle cx="208" cy="126" r="2" fill="%s"/>' % skin)
    g.append('<path d="M194 108C202 102 212 102 221 106L220 109C212 106 203 107 196 111Z" fill="%s"/>' % hair_d)
    # mouth
    g.append('<path d="M214 159C218 160 221 160 224 158" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round"/>' % hair_d)

    # hair cap, bangs, side lock
    g.append('<path d="M120 124C108 70 150 34 196 48C210 52 220 64 222 80L186 76C166 96 156 124 158 160'
             'C146 176 130 160 120 124Z" fill="%s"/>' % hair)
    g.append('<path d="M150 62C172 42 206 46 220 74L224 106L213 92L210 114L199 95L192 110L185 90'
             'C176 84 166 82 156 88Z" fill="%s"/>' % hair)
    g.append('<path d="M172 96C164 130 168 168 178 200C182 182 184 158 182 130C181 114 178 102 172 96Z" fill="%s"/>' % hair)
    g.append('<path d="M156 58C172 48 192 50 206 62C190 58 172 62 160 74Z" fill="%s"/>' % hair_l)
    # tie
    g.append('<path d="M138 60C146 50 160 50 168 58L162 72C156 66 148 66 142 72Z" fill="%s"/>' % cape)

    # raised arm and open palm
    g.append('<path d="M262 300C276 270 292 250 310 236L332 252C316 270 304 296 298 330Z" fill="%s"/>' % cape)
    for bx, by, ang, ln in ((320, 210, 22, 32), (329, 212, 36, 36), (337, 217, 50, 33), (343, 224, 64, 27), (309, 228, -34, 24)):
        g.append('<rect x="-4.5" y="%s" width="9" height="%s" rx="4.5" transform="translate(%s %s) rotate(%s)" fill="%s"/>' % (
            n(-ln), n(ln + 6), n(bx), n(by), n(ang), skin))
    g.append('<path d="M306 244C298 228 304 210 320 204L346 218C354 228 350 242 338 248L318 258Z" fill="%s"/>' % skin)
    g.append('<path d="M312 240C322 244 334 242 342 234" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round"/>' % shade)
    g.append('<path d="M300 238C310 236 324 242 332 252L322 266C314 258 304 254 294 256Z" fill="%s"/>' % ink)

    # lightning over the palm
    g.append('<g transform="translate(-4 -34)">')
    g.append('<path d="M318 96L336 134L322 138L346 190L300 148L316 142L296 108Z" fill="%s"/>' % t.soft)
    g.append('<path d="M320 112L332 136L320 140L334 170L308 148L322 142L308 118Z" fill="%s"/>' % t.rune)
    g.append('<path d="M286 150l-12 -6 M356 146l14 -8 M354 176l12 6 M290 180l-10 10" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % t.soft)
    g.append("</g>")
    g.append("</g>")
    return "".join(g)


def cat(t, x, y, scale=1.0, color=None):
    """Small sitting cat, 80 x 80, the feet rest on y = 80."""
    c = color or t.soft
    eye = t.bg
    g = ['<g transform="translate(%s %s) scale(%s)">' % (n(x), n(y), n(scale))]
    g.append('<path d="M60 78C76 78 84 92 78 106C74 116 62 116 60 108" fill="none" stroke="%s" stroke-width="7" stroke-linecap="round"/>' % c)
    g.append('<path d="M18 80C14 56 22 40 40 40C58 40 66 56 62 80Z" fill="%s"/>' % c)
    g.append('<path d="M16 30L20 6L34 18C38 17 42 17 46 18L60 6L64 30C66 44 56 52 40 52C24 52 14 44 16 30Z" fill="%s"/>' % c)
    g.append('<ellipse cx="31" cy="32" rx="3.4" ry="4.6" fill="%s"/><ellipse cx="49" cy="32" rx="3.4" ry="4.6" fill="%s"/>' % (eye, eye))
    g.append('<path d="M37 40L43 40L40 44Z" fill="%s"/>' % eye)
    g.append("</g>")
    return "".join(g)


def sword(t, x, y, scale=1.0, rotate=0, blade=None, guard=None):
    """Original sword silhouette, pointing up, 60 x 300, origin at the pommel centre."""
    blade = blade or t.soft
    guard = guard or t.accent
    ink = _ink(t)
    g = ['<g transform="translate(%s %s) rotate(%s) scale(%s)">' % (n(x), n(y), n(rotate), n(scale))]
    g.append('<path d="M-9 -78L-11 -250L0 -292L11 -250L9 -78Z" fill="%s"/>' % blade)
    g.append('<path d="M0 -78L0 -292L11 -250L9 -78Z" fill="%s" opacity=".55"/>' % mix(blade, ink, 0.35))
    g.append('<path d="M-44 -96C-30 -84 -14 -80 0 -80C14 -80 30 -84 44 -96L38 -74C26 -66 12 -64 0 -64C-12 -64 -26 -66 -38 -74Z" fill="%s"/>' % guard)
    g.append('<path d="M0 -98L9 -84L0 -70L-9 -84Z" fill="%s"/>' % t.rune)
    g.append('<rect x="-6" y="-64" width="12" height="50" rx="3" fill="%s"/>' % mix(guard, ink, 0.45))
    g.append('<path d="M-6 -52h12M-6 -40h12M-6 -28h12" stroke="%s" stroke-width="2" opacity=".7"/>' % t.soft)
    g.append('<path d="M0 -16L10 -4L0 8L-10 -4Z" fill="%s"/>' % guard)
    g.append("</g>")
    return "".join(g)


def glint(doc, x, y, scale=1.0, rotate=0):
    """A light running along a blade, once every few seconds."""
    doc.style(".glint{animation:glint 6s ease-in-out infinite}"
              "@keyframes glint{0%,60%{transform:translateY(0);opacity:0}65%{opacity:.9}90%{opacity:.9}100%{transform:translateY(-200px);opacity:0}}")
    return ('<g transform="translate(%s %s) rotate(%s) scale(%s)"><path class="glint" d="M-9 -90L9 -96L9 -84L-9 -78Z" fill="%s"/></g>'
            % (n(x), n(y), n(rotate), n(scale), "#f1ecfa" if doc.t.dark else "#fbf8f3"))


def rupee(t, x, y, size=40, fill=None):
    fill = fill or t.rune
    s = size / 40.0
    return ('<g transform="translate(%s %s) scale(%s)"><path d="M0 -20L12 -8V8L0 20L-12 8V-8Z" fill="%s"/>'
            '<path d="M0 -12L6 -6V6L0 12L-6 6V-6Z" fill="%s" opacity=".35"/></g>') % (n(x), n(y), n(s), fill, t.bg)


def triforce(t, x, y, size=60, fill=None):
    fill = fill or t.soft
    h = size * 0.866
    return '<path d="M%s %sl%s %sh-%sz m-%s %sl%s %sh-%sz m%s 0l%s %sh-%sz" fill="%s"/>' % (
        n(x), n(y - h / 2), n(size / 4), n(h / 2), n(size / 2),
        n(size / 4), n(h / 2), n(size / 4), n(h / 2), n(size / 2),
        n(size / 2), n(size / 4), n(h / 2), n(size / 2), fill)


def korok_leaf(t, x, y, scale=1.0, rotate=0, fill=None):
    fill = fill or t.rune
    return ('<g transform="translate(%s %s) rotate(%s) scale(%s)">'
            '<path d="M0 -40C22 -30 30 -6 22 14C16 28 6 34 0 40C-6 34 -16 28 -22 14C-30 -6 -22 -30 0 -40Z" fill="%s"/>'
            '<path d="M0 -30V52" stroke="%s" stroke-width="3" stroke-linecap="round"/>'
            '<path d="M0 -8L12 -18M0 8L14 -2M0 -8L-12 -18M0 8L-14 -2" stroke="%s" stroke-width="2.4" stroke-linecap="round" fill="none"/></g>') % (
        n(x), n(y), n(rotate), n(scale), fill, t.bg, t.bg)


def sketch(t, x, y, scale=1.0):
    """A sketchbook page with a pencil, 300 x 260."""
    ink = _ink(t)
    paper = "#f1ecfa" if t.dark else "#fbf8f3"
    line = "#3b2280"
    g = ['<g transform="translate(%s %s) scale(%s)">' % (n(x), n(y), n(scale))]
    g.append('<g transform="rotate(-6 150 130)">')
    g.append('<rect x="44" y="26" width="196" height="224" rx="6" fill="%s" opacity=".5"/>' % t.accent)
    g.append('<rect x="34" y="16" width="196" height="224" rx="6" fill="%s"/>' % paper)
    for i in range(7):
        g.append('<circle cx="46" cy="%d" r="4" fill="%s"/>' % (38 + i * 30, ink))
    # the drawing: a face in three quarter view, construction lines, a leaf
    g.append('<circle cx="134" cy="106" r="44" fill="none" stroke="%s" stroke-width="3"/>' % line)
    g.append('<path d="M100 120C104 158 124 176 140 176C156 176 172 158 174 126" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % line)
    g.append('<path d="M92 106H178M134 62V176" stroke="%s" stroke-width="1.6" stroke-dasharray="5 5" opacity=".6"/>' % line)
    g.append('<path d="M108 118q10 -8 20 0M142 118q10 -8 20 0" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % line)
    g.append('<path d="M98 84C110 56 150 50 172 78C160 72 148 74 140 82C128 72 110 74 98 84Z" fill="%s"/>' % t.accent)
    g.append('<path d="M64 206h110M64 220h70" stroke="%s" stroke-width="3" stroke-linecap="round" opacity=".5"/>' % line)
    g.append("</g>")
    # pencil
    g.append('<g transform="translate(262 232) rotate(-38)">')
    g.append('<rect x="-150" y="-9" width="120" height="18" fill="%s"/>' % t.accent)
    g.append('<rect x="-150" y="-9" width="120" height="6" fill="%s" opacity=".5"/>' % t.soft)
    g.append('<rect x="-168" y="-9" width="18" height="18" rx="3" fill="%s"/>' % t.seal)
    g.append('<path d="M-30 -9L0 0L-30 9Z" fill="%s"/>' % paper)
    g.append('<path d="M-10 -3L0 0L-10 3Z" fill="%s"/>' % ink)
    g.append("</g>")
    g.append("</g>")
    return "".join(g)


def props(t, x, y, scale=1.0):
    """Cosplay workbench: a foam sword, a shield blank, a glue gun. 300 x 260."""
    ink = _ink(t)
    g = ['<g transform="translate(%s %s) scale(%s)">' % (n(x), n(y), n(scale))]
    # shield blank
    g.append('<path d="M60 40H170V130C170 176 140 204 115 216C90 204 60 176 60 130Z" fill="%s"/>' % mix(t.accent, ink, 0.35))
    g.append('<path d="M72 52H158V130C158 166 136 190 115 202C94 190 72 166 72 130Z" fill="none" stroke="%s" stroke-width="3"/>' % t.soft)
    g.append(triforce(t, 115, 112, 56, t.soft))
    # glue gun
    g.append('<g transform="translate(206 186)">')
    g.append('<path d="M-40 -30H40L52 -22V-6H8L2 40H-24L-18 -6H-40Z" fill="%s"/>' % t.accent)
    g.append('<path d="M52 -18H70V-10H52Z" fill="%s"/>' % t.soft)
    g.append('<path d="M-40 -24H-58V-12H-40Z" fill="%s"/>' % t.soft)
    g.append('<path d="M74 -14q10 14 0 26q-10 -12 0 -26Z" fill="%s"/>' % t.rune)
    g.append("</g>")
    g.append("</g>")
    return "".join(g)


def tower(t, x, y, scale=1.0):
    """Tower silhouette, 160 wide, 230 tall, origin at the centre of its base."""
    ink = _ink(t)
    body = mix(t.accent, ink, 0.55) if t.dark else mix(t.accent, "#f5f1ea", 0.25)
    dark = mix(t.accent, ink, 0.75) if t.dark else mix(t.accent, "#3b2280", 0.5)
    g = ['<g transform="translate(%s %s) scale(%s)">' % (n(x), n(y), n(scale))]
    g.append('<path d="M-34 0L-20 -150H20L34 0Z" fill="%s"/>' % body)
    g.append('<path d="M0 0V-150H20L34 0Z" fill="%s"/>' % dark)
    for i in range(5):
        yy = -24 - i * 26
        g.append('<path d="M%s %sL%s %s" stroke="%s" stroke-width="2" opacity=".7"/>' % (
            n(-31 + i * 2.3), n(yy), n(31 - i * 2.3), n(yy - 12), t.bg))
    g.append('<path d="M-70 -150H70L58 -168H-58Z" fill="%s"/>' % dark)
    g.append('<path d="M-58 -168H58L46 -178H-46Z" fill="%s"/>' % body)
    g.append('<path d="M-46 -178L-40 -196L-28 -178Z M46 -178L40 -196L28 -178Z" fill="%s"/>' % body)
    g.append('<path d="M-18 -178L0 -232L18 -178Z" fill="%s"/>' % body)
    g.append('<path d="M0 -178V-232L18 -178Z" fill="%s"/>' % dark)
    g.append("</g>")
    return "".join(g)


def lock(t, x, y, scale=1.0, color=None):
    """Padlock, 48 x 60, centred."""
    c = color or t.soft
    return ('<g transform="translate(%s %s) scale(%s)">'
            '<path d="M-14 -6V-18C-14 -36 14 -36 14 -18V-6" fill="none" stroke="%s" stroke-width="7"/>'
            '<rect x="-24" y="-8" width="48" height="38" rx="6" fill="%s"/>'
            '<circle cy="8" r="6" fill="%s"/><rect x="-3" y="10" width="6" height="12" rx="2" fill="%s"/></g>') % (
        n(x), n(y), n(scale), c, c, t.bg, t.bg)
