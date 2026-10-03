"""
Typical members of standard set R2 (user, 2026-09-30): every typical detail draws THESE sizes, so a column is
the same 400 wide in a section, a plan and an elevation, and a beam the same 300 x 600 on every sheet.
Typical details are N.T.S.: members at true size (placed at the dummy 1:25), LENGTHS shortened with break lines.
"""
# columns
COL = 400                      # square column 400 x 400, 8-DB20 (3 bars per face)
CVR = 40                       # clear cover to ties / stirrups (beams, columns)
DT = 9                         # tie / stirrup drawn (RB9 ordinary, DB10 intermediate / special)
DBM = 20                       # main bar DB20

# beams
BEAM_B, BEAM_H = 300, 600      # typical (main) beam b x h
SEC_B, SEC_H = 250, 450        # secondary beam b x h

# slabs
SLAB_T = 150                   # slab on beams
SLAB_CVR = 20                  # cover to slab bars (not exposed, <= DB16)
DBS = 12                       # slab bar DB12
FLAT_T = 200                   # flat slab
DROP_H = 50                    # drop panel projection below the flat slab (>= h/4)
SOG_T = 150                    # slab on ground

# foundations / walls
FOOT_B, FOOT_T = 1600, 600     # isolated footing B x B x T
LEAN_T = 50                    # lean concrete
WALL_T = 200                   # RC wall

# drawn lengths (N.T.S.) - lengths only, never member sizes
STOREY_D = 2400                # clear storey height drawn (floor top to beam soffit)
SPAN_D = 3600                  # clear span drawn
STUB_D = 350                   # member stub drawn beyond a support
LAP_D = 800                    # lap length drawn (real value: 1002 TABLE 6)
LO_D = 500                     # lo drawn
