"""
drafter.thai.cad_thai: Thai marks mapped to the font's positioned glyphs for AutoCAD (DRAWING_PRODUCTION.md §8).
"""
import pytest

from drafter.thai import cad_thai


@pytest.mark.parametrize("text, expected", [
    ("บางด้วน", "บางดวน"),                     # tone mark, no upper vowel: low (RPM B3 title block)
    ("พจนีย์", "พจนีย"),                       # thanthakhat, no upper vowel: low
    ("สวัสดิ์", "สวัสดิ์"),                          # thanthakhat over sara i: stays high
    ("น้ำ", "น้ำ"),                                  # before sara am: stays high
    ("ปี่", "ป"),                        # ป: upper vowel left, mark high-left
    ("ป่า", "ปา"),                             # ป, no upper vowel: low-left
    ("ปั้น", "ปน"),                      # ป: mai han-akat left, mark high-left
])
def test_cad_thai(text, expected):
    assert cad_thai(text) == expected


def test_cad_thai_leaves_other_text_and_is_idempotent():
    s = "88/853 บางด้วน ภาษีเจริญ  ส-สถ 4003"
    assert cad_thai("STEEL STAIR 1:50 Ø16") == "STEEL STAIR 1:50 Ø16"
    assert cad_thai(cad_thai(s)) == cad_thai(s)
    assert cad_thai("ภาษีเจริญ") == "ภาษีเจริญ"                 # no marks
