"""
drafter.tis_sections: the TIS 1227 / TIS 1228 catalogue and the true outlines (user 2026-10-18; steel S4.15).
Every outline's area must match the area its standard tabulates, so a wrong radius, flange slope, bend radius or a row
read into the wrong size shows here.
"""
import pytest

from drafter import tis_sections as T


def test_catalogue_complete():
    cat = T.catalogue()
    kinds = {}
    for s in cat.values():
        kinds[s["kind"]] = kinds.get(s["kind"], 0) + 1
    assert kinds["H"] == 80 and kinds["I"] == 20 and kinds["C"] == 17
    assert kinds["L"] >= 55 and kinds["LC"] >= 30 and kinds["CC"] >= 30
    assert all(s["src"].startswith(("TIS 1227", "TIS 1228")) for s in cat.values())


@pytest.mark.parametrize("name", sorted(T.catalogue()))
def test_outline_area_matches_the_table(name):
    s = T.section(name)
    a = T.area(T.outline(name)) / 100.0                               # cm2
    assert abs(a - s["area_cm2"]) / s["area_cm2"] < 0.02, (name, a, s["area_cm2"])


def test_known_sections():
    h = T.section("H 150x150x7x10")
    assert h["r"] == 11 and h["area_cm2"] == pytest.approx(40.14)
    c = T.section("C 150x75x6.5x10")
    assert (c["r1"], c["r2"]) == (10, 5)
    assert T.section("L 65x65x6")["r1"] == 8.5


def test_unknown_name_says_the_nearest():
    with pytest.raises(KeyError, match="nearest"):
        T.section("H 150x150x9x12")


def test_profile_accepts_a_name():
    from drafter.steel_access import profile
    loops = profile("LC 100x50x20x2.3")
    assert len(loops) == 1 and len(loops[0]) > 20
