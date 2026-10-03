"""
Pens by colour and the linetype scale of standard set R2. No side effects: plot.py reads them without
building a drawing (td_engine creates its document at import).
"""
LTS = 3.75                         # LTSCALE (model space) for 1:25 with acadiso.lin (user, 2026-09-30)

# Pens by colour: ACI -> (lineweight 1/100 mm, screen %). One colour = one pen; NRW-EIT-R2.ctb is built from it.
PEN = {
    1: (50, 100),     # red: main bars, dowels
    30: (35, 100),    # orange: stirrups, ties, secondary bars
    4: (35, 100),     # cyan: concrete CUT, title text, title-block lines
    5: (25, 100),     # blue: concrete SEEN, construction joint, soil, drain
    6: (25, 100),     # magenta: cutting plane, property line, joints, symbols
    3: (18, 100),     # green: leaders, centre lines, geotextile, surcharge
    2: (18, 100),     # yellow: dimensions
    7: (18, 100),     # white: text, lean concrete, detail inserts
    10: (70, 100),    # sheet frame
    8: (18, 50),      # grey: breaks, arris, zone grid, thin title lines, notional lines, dim extension lines
    252: (25, 50),    # grey: hidden concrete, excavation, hidden drain
    9: (13, 50),      # grey: hatch, viewport, sheet edge
}
