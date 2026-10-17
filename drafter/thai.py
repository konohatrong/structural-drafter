"""
drafter.thai: Thai text for AutoCAD (opt-in).

AutoCAD (Core Console plot, AutoCAD 2024) draws Thai TrueType text without shaping: every tone mark and the
thanthakhat sit at the high position (TH Sarabun New: 1.42 - 1.76 x cap height), whether or not there is an upper
vowel under them, and on the tall consonants ป ฝ ฟ ฬ the marks and upper vowels are not moved off the stem. In a
tight block of lines (the A3 title block signature table: 2.2 mm text at 3.6 mm pitch) the mark of "ด้" in "บางด้วน"
reached into the line above and read as a hook under its letters (RPM Staircase B3, 17/10/2026; TEXT and MTEXT
behave the same in TH Sarabun New, SarabunPSK, Leelawadee, Tahoma and Angsana New).

cad_thai(s) does the shaping itself with the font's positioned glyphs (the Microsoft Thai private-use set, present
in TH Sarabun New):
    - a tone mark or thanthakhat with no upper vowel under it -> its low glyph U+F70A - F70E
      (low-left U+F705 - F709 after ป ฝ ฟ ฬ);
    - before sara am (U+0E33) the mark stays high, as the font draws it ("น้ำ" unchanged);
    - after ป ฝ ฟ ฬ an upper vowel -> its left glyph (U+F701 - F704, F710 - F712) and a high mark over it -> its
      high-left glyph (U+F713 - F717).

Use it only on Thai strings written into the DXF for AutoCAD (title block names, Thai notes). Keep plain Unicode
everywhere else (reports, DOCX, the PDF text check): the private-use glyphs are not searchable and shape wrongly in
software that does its own shaping. The font must carry the private-use set; check a new font with fontTools.
Rule: docs/general/DRAWING_PRODUCTION.md §8.
"""

TALL = "ปฝฟฬ"               # ป ฝ ฟ ฬ: marks and upper vowels shift left of the stem
MARKS = "่้๊๋์"        # mai ek, tho, tri, chattawa; thanthakhat
UPPER_LEFT = {                                   # upper vowel -> its left glyph (after ป ฝ ฟ ฬ)
    "ั": "",                          # mai han-akat
    "ิ": "",                          # sara i
    "ี": "",                          # sara ii
    "ึ": "",                          # sara ue
    "ื": "",                          # sara uee
    "็": "",                          # mai taikhu
    "ํ": "",                          # nikhahit
}
MARK_LOW, MARK_LOW_LEFT, MARK_HIGH_LEFT = 0xF70A, 0xF705, 0xF713   # first of five glyphs, in MARKS order
SARA_AM = "ำ"


def cad_thai(s):
    """s with Thai marks replaced by the positioned glyphs AutoCAD needs (module docstring). Other characters,
    and text already converted, pass unchanged."""
    out, base, upper = [], "", False
    for i, c in enumerate(s):
        nxt = s[i + 1] if i + 1 < len(s) else ""
        if c in MARKS:
            k = MARKS.index(c)
            if not upper and nxt != SARA_AM:
                c = chr((MARK_LOW_LEFT if base in TALL else MARK_LOW) + k)
            elif base in TALL:                          # high over an upper vowel or before sara am
                c = chr(MARK_HIGH_LEFT + k)
        elif c in UPPER_LEFT:
            upper = True
            if base in TALL:
                c = UPPER_LEFT[c]
        elif "ก" <= c <= "ฮ":                # a consonant starts a new cell
            base, upper = c, False
        out.append(c)
    return "".join(out)
