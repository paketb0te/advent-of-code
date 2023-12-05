import pytest
import solve

TEST_INPUT = "test_input.txt"


def test_parse_mapping_name():
    given = "soil-to-fertilizer map:"
    want = "soil", "fertilizer"
    got = solve.parse_mapping_name(given)
    assert got == want


def test_parse_seeds():
    given = "seeds: 79 14"
    want = [79, 14]
    got = solve.parse_seeds(given)
    assert got == want


def test_parse_map_line():
    given = "0 15 37"
    want = solve.MapEntry(dst_start=0, src_start=15, range_length=37)
    got = solve.parse_map_line(given)
    assert got == want


def test_entry_map():
    entry = solve.MapEntry(dst_start=0, src_start=15, range_length=10)

    given = [15, 16, 24]
    want = [0, 1, 9]

    for g, w in zip(given, want):
        assert entry.map(g) == w

    with pytest.raises(ValueError):
        entry.map(14)
    with pytest.raises(ValueError):
        entry.map(25)
