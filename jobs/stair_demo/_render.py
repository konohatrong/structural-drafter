import sys
import pymupdf as fitz
d = fitz.open('out/STR-ST_Stair_ST-1_A3_RevA.pdf'); p = d[0]
p.get_pixmap(dpi=110).save('out/_p.png')
k = 72 / 25.4
for n, (x0, y0, x1, y1), dpi in [(a.split(':')[0], tuple(map(float, a.split(':')[1].split(','))), int(a.split(':')[2])) for a in sys.argv[1:]]:
    p.get_pixmap(dpi=dpi, clip=fitz.Rect(x0 * k, y0 * k, x1 * k, y1 * k)).save(f'out/_{n}.png')
