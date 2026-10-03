"""
Text widths measured from the Arial Narrow font files, so the engines can wrap notes and pack note columns to
the plotted size. AutoCAD's TTF text height is the cap height, so widths are scaled by the height of "H".
"""
import os
import re
import sys
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen as _BP
from fontTools.ttLib import TTFont as _TTF

FONT_DIR = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
_FONTS = {}
for _k, _f in (("AN", "ARIALN.TTF"), ("ANB", "ARIALNB.TTF")):
    if not (FONT_DIR / _f).exists():
        sys.exit(f"!! font {_f} (Arial Narrow) not found in {FONT_DIR}: the notes are measured with it - install it")
    _t = _TTF(str(FONT_DIR / _f))
    _gs = _t.getGlyphSet()
    _bp = _BP(_gs)
    _gs[_t.getBestCmap()[ord("H")]].draw(_bp)
    _FONTS[_k] = (_t.getBestCmap(), _t["hmtx"], _bp.bounds[3])


def text_w(s, h, style="AN"):
    """plotted width of a single-line string at text height h (AutoCAD TTF height = cap height)"""
    cmap, hm, cap = _FONTS[style]
    return sum(hm[cmap.get(ord(c), cmap[ord("M")])][0] for c in s) / cap * h


_UNIT = re.compile(r"^(mm|m|kN|kPa|MPa|t|kg|%|µm|°|mm2|kN/m)[,.;:)]*$")


def wrap(s, h, width, keep_units=False):
    """greedy wrap at real glyph widths. keep_units: a number and its unit never split across lines
    ("60 mm", "0.030 m"; annotation rule 2.4.2)"""
    words = s.split()
    if keep_units:
        out_w = []
        for w in words:
            if out_w and _UNIT.match(w) and out_w[-1][-1:].isdigit():
                out_w[-1] += " " + w
            else:
                out_w.append(w)
        words = out_w
    out, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if cur and text_w(t, h) > width:
            out.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        out.append(cur)
    return out
