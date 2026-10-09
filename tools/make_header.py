"""Builds assets/boot-day.svg and assets/boot-night.svg for Evan's GitHub profile.

An original 8-bit "boot screen": 22 columns like a VIC-20, wide pixels (3:2),
glyphs from Daniel Hepper's public-domain font8x8. Every glyph is drawn as
plain path data, so the SVG needs no fonts and survives GitHub's sanitizer.

Static state (no animation / reduced motion) == the final screen.

Usage (from the repo root):  python tools/make_header.py assets
Edit the strings in build() to change what the screen says.
"""
import re, sys
from pathlib import Path

# ---------- font ----------
FONT = {}
for line in Path(__file__).with_name("font8x8_basic.h").read_text().splitlines():
    m = re.match(r"\s*\{([^}]*)\},\s*// U\+([0-9A-F]{4})", line)
    if m:
        FONT[int(m.group(2), 16)] = [int(x, 16) for x in m.group(1).split(",")]
# pointier V (bit 0 = leftmost pixel) so it never reads as U
FONT[ord("V")] = [0x63, 0x63, 0x63, 0x36, 0x36, 0x1C, 0x08, 0x00]

# ---------- geometry (user units) ----------
import os
PX, PY = int(os.environ.get("PX", 3)), int(os.environ.get("PY", 2))   # one native pixel (wide, VIC-style)
LEAD = int(os.environ.get("LEAD", 9))     # native pixel rows per cell (8 is authentic; 9 adds a pixel of leading)
CW, CH = 8 * PX, LEAD * PY
COLS, ROWS = 22, int(os.environ.get("ROWS", 10))
BX, BY = int(os.environ.get("BX", 36)), int(os.environ.get("BY", 22))   # border thickness
OX, OY = BX, BY          # screen origin
W, H = COLS * CW + 2 * BX, ROWS * CH + 2 * BY   # 600 x 200


def glyph_runs(ch, gx, gy, scale=1, rows=range(8)):
    """Path commands for one glyph at unit position (gx, gy)."""
    out = []
    bits = FONT[ord(ch)]
    for r in rows:
        b, x = bits[r], 0
        while x < 8:
            if (b >> x) & 1:
                x0 = x
                while x < 8 and (b >> x) & 1:
                    x += 1
                w = (x - x0) * PX * scale
                out.append(f"M{gx + x0 * PX * scale} {gy + (r - rows.start) * PY * scale}h{w}v{PY * scale}h-{w}z")
            else:
                x += 1
    return "".join(out)


def text_d(s, col, row, scale=1, rows=range(8), dy=0):
    return "".join(
        glyph_runs(ch, OX + (col + i * scale) * CW, OY + row * CH + dy, scale, rows)
        for i, ch in enumerate(s) if ch != " "
    )


def cell(col, row):
    return f'x="{OX + col * CW}" y="{OY + row * CH}" width="{CW}" height="{CH}"'


# ---------- timeline (seconds) ----------
T_TYPE1, DT = 0.60, 0.055
CMD1 = 'LOAD"README",8'
T_ENTER1 = T_TYPE1 + len(CMD1) * DT + 0.13          # ~1.55
T_SEARCH, T_LOADING, T_READY2 = 1.70, 2.10, 2.60
T_TYPE2 = 2.85
CMD2 = "RUN"
T_CLR = T_TYPE2 + len(CMD2) * DT + 0.14              # ~3.15
T_OUT = [T_CLR + 0.05 + 0.04 * i for i in range(4)]  # big name, printed row by row
T_TAG = [T_OUT[-1] + 0.06 + 0.04 * i for i in range(3)]
T_DONE = T_TAG[-1] + 0.10

css_rules = {}


def hide_until(t):
    """class that keeps an element invisible until time t, then shows it for good"""
    k = f"u{int(round(t * 1000))}"
    css_rules[k] = f".{k}{{animation-duration:{t:.3f}s}}"
    return f"h {k}"


def window(a, b):
    """class that shows an element only during [a, b)"""
    k = f"w{int(round(a * 1000))}_{int(round(b * 1000))}"
    css_rules[k] = f".{k}{{animation-delay:{a:.3f}s;animation-duration:{b - a:.3f}s}}"
    return f"w {k}"


def build(pal):
    ink = pal["ink"]
    els = []

    # --- boot phase (only visible until CLR) ---
    boot = []
    boot.append(f'<path d="{text_d("** BITSMITHY BASIC **", 0, 0)}{text_d("3583 BYTES FREE", 0, 1)}{text_d("READY.", 0, 3)}"/>')
    for i, ch in enumerate(CMD1):
        boot.append(f'<path class="{hide_until(T_TYPE1 + i * DT)}" d="{text_d(ch, i, 4)}"/>')
    boot.append(f'<path class="{hide_until(T_SEARCH)}" d="{text_d("SEARCHING FOR README", 0, 6)}"/>')
    boot.append(f'<path class="{hide_until(T_LOADING)}" d="{text_d("LOADING", 0, 7)}"/>')
    boot.append(f'<path class="{hide_until(T_READY2)}" d="{text_d("READY.", 0, 8)}"/>')
    for i, ch in enumerate(CMD2):
        boot.append(f'<path class="{hide_until(T_TYPE2 + i * DT)}" d="{text_d(ch, i, 9)}"/>')
    # cursors: idle (blinking) before typing, then following the typed text
    boot.append(f'<g class="{window(0, T_TYPE1)}"><rect class="blink" {cell(0, 4)}/></g>')
    for k in range(1, len(CMD1) + 1):
        end = T_TYPE1 + k * DT if k < len(CMD1) else T_ENTER1
        boot.append(f'<rect class="{window(T_TYPE1 + (k - 1) * DT, end)}" {cell(k, 4)}/>')
    boot.append(f'<rect class="{window(T_READY2, T_TYPE2)}" {cell(0, 9)}/>')
    for k in range(1, len(CMD2) + 1):
        end = T_TYPE2 + k * DT if k < len(CMD2) else T_CLR
        boot.append(f'<rect class="{window(T_TYPE2 + (k - 1) * DT, end)}" {cell(k, 9)}/>')
    els.append(f'<g class="boot">{"".join(boot)}</g>')

    # --- program output (the static/final state) ---
    out = []
    top, bottom = range(0, 4), range(4, 8)
    out.append(f'<path class="{hide_until(T_OUT[0])}" d="{text_d("EVAN", 0, 0, 2, top)}"/>')
    out.append(f'<path class="{hide_until(T_OUT[1])}" d="{text_d("EVAN", 0, 0, 2, bottom, 8 * PY)}"/>')
    out.append(f'<path class="{hide_until(T_OUT[2])}" d="{text_d("WIELAND", 0, 2, 2, top)}"/>')
    out.append(f'<path class="{hide_until(T_OUT[3])}" d="{text_d("WIELAND", 0, 2, 2, bottom, 8 * PY)}"/>')
    for i, line in enumerate(["COMPILERS, AI VIDEO", "LOOPS AND HUMAN", "APPROVAL FOR AGENTS."]):
        out.append(f'<path class="{hide_until(T_TAG[i])}" d="{text_d(line, 0, 5 + i)}"/>')
    out.append(f'<path class="{hide_until(T_DONE)}" d="{text_d("READY.", 0, 8)}"/>')
    out.append(f'<g class="{hide_until(T_DONE)}"><rect class="blink" {cell(0, 9)}/></g>')
    els.append("".join(out))

    css = (
        "path,rect{shape-rendering:crispEdges}"
        ".boot{opacity:0;animation:keep %.3fs step-end}" % T_CLR +
        "@keyframes keep{from,to{opacity:1}}"
        ".h{animation-name:hide;animation-timing-function:step-end}"
        "@keyframes hide{from,to{opacity:0}}"
        ".w{opacity:0;animation-name:keep;animation-timing-function:step-end}"
        ".blink{animation:blink .66s step-end infinite}"
        "@keyframes blink{50%{opacity:0}}"
        + "".join(css_rules.values()) +
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
    )
    title = "Evan Wieland: compilers, AI video loops and human approval for agents"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W * 2}" height="{H * 2}" role="img" aria-label="{title}">'
        f"<title>{title}</title>"
        f"<style>{css}</style>"
        f'<rect width="{W}" height="{H}" fill="{pal["border"]}"/>'
        f'<rect x="{OX}" y="{OY}" width="{COLS * CW}" height="{ROWS * CH}" fill="{pal["screen"]}"/>'
        f'<g fill="{ink}">{"".join(els)}</g>'
        "</svg>"
    )


PALETTES = {
    # POKE 36879,27 -- white screen, cyan border, blue ink (the power-on look)
    "day": {"border": "#7CDDE4", "screen": "#FFFFFF", "ink": "#3B3FCB"},
    # POKE 36879,14 : POKE 646,3 -- black screen, blue border, cyan ink
    "night": {"border": "#3B3FCB", "screen": "#000000", "ink": "#7CDDE4"},
}

if __name__ == "__main__":
    outdir = Path(sys.argv[1] if len(sys.argv) > 1 else "assets")
    outdir.mkdir(parents=True, exist_ok=True)
    for name, pal in PALETTES.items():
        css_rules.clear()
        svg = build(pal)
        (outdir / f"boot-{name}.svg").write_text(svg)
        print(name, len(svg), "bytes")
