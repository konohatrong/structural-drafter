"""
Compare a set's PDF against a reference PDF (e.g. the former paper-space version), page by page.

usage: python compare_pdf.py <new.pdf> <reference.pdf> [dpi]
Prints the share of differing pixels per page, and the "unmatched" ink: dark pixels with no dark pixel within
TOL px in the other file (sub-pixel shifts pass, missing or moved items do not). Writes _diff_p<n>.png
(red = unmatched ink in new, blue = unmatched ink in reference) next to the new PDF for pages with unmatched ink.
"""
import sys
from pathlib import Path

import fitz
import numpy as np

new, ref = Path(sys.argv[1]), Path(sys.argv[2])
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 150
TOL = 2


def near(m, r=TOL):
    """dilate a boolean mask by r pixels (square)"""
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


a, b = fitz.open(new), fitz.open(ref)
print(f"pages: new {a.page_count}, reference {b.page_count}")
for i in range(min(a.page_count, b.page_count)):
    pa = a[i].get_pixmap(dpi=dpi, colorspace=fitz.csGRAY)
    pb = b[i].get_pixmap(dpi=dpi, colorspace=fitz.csGRAY)
    x = np.frombuffer(pa.samples, np.uint8).reshape(pa.h, pa.w).astype(int)
    y = np.frombuffer(pb.samples, np.uint8).reshape(pb.h, pb.w).astype(int)
    d = np.abs(x - y) > 64
    share = d.mean() * 100
    ix, iy = x < 128, y < 128
    un_x, un_y = ix & ~near(iy), iy & ~near(ix)
    print(f"page {i + 1}: {d.sum():7d} px differ ({share:.3f} %), unmatched ink: new {un_x.sum()}, reference {un_y.sum()}")
    if un_x.sum() + un_y.sum():
        img = np.stack([np.minimum(x, y)] * 3, -1).astype(np.uint8)
        img = (255 - (255 - img) * 0.25).astype(np.uint8)      # faint background
        img[near(un_x, 3)] = (220, 0, 0)                         # unmatched ink in new
        img[near(un_y, 3)] = (0, 90, 220)                        # unmatched ink in reference
        out = new.parent / f"_diff_p{i + 1}.png"
        fitz.Pixmap(fitz.csRGB, pa.w, pa.h, img.tobytes(), False).save(out)
