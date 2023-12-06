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
    got = solve.parse_map_entry_line(given)
    assert got == want


def test_entry_map_returns_correct_value_in_range():
    entry = solve.MapEntry(dst_start=10, src_start=15, range_length=3)
    given = [15, 16, 17]
    want = [10, 11, 12]

    for g, w in zip(given, want):
        assert entry.map(g) == w


def test_entry_map_raises_on_value_out_of_range():
    entry = solve.MapEntry(dst_start=10, src_start=15, range_length=3)
    with pytest.raises(ValueError):
        entry.map(14)
    with pytest.raises(ValueError):
        entry.map(18)


def test_select_correct_map_entry():
    map_entries = [
        solve.MapEntry(dst_start=100, src_start=5, range_length=5),
        solve.MapEntry(dst_start=200, src_start=10, range_length=5),
        solve.MapEntry(dst_start=300, src_start=15, range_length=5),
    ]
    given = 12
    want = [False, True, False]
    got = [m.value_in_range(given) for m in map_entries]
    assert got == want


def test_map_input():
    map_entries = [
        solve.MapEntry(dst_start=100, src_start=10, range_length=5),
        solve.MapEntry(dst_start=200, src_start=20, range_length=5),
    ]
    m = solve.Map("a", "b", map_entries)

    given = 22
    want = 202
    got = m.map(given)
    assert got == want


def test_map_input_out_of_range():
    map_entries = [
        solve.MapEntry(dst_start=100, src_start=10, range_length=5),
        solve.MapEntry(dst_start=200, src_start=20, range_length=5),
    ]
    m = solve.Map("a", "b", entries=map_entries)

    given = [1, 18, 999]
    want = [1, 18, 999]
    for g, w in zip(given, want):
        assert m.map(g) == w


def test_build_seed_to_soil_map_with_sorted_entries():
    given = [
        "seed-to-soil map:",
        "50 98 2",
        "52 50 48",
        "",
    ]
    map_entries = [
        solve.MapEntry(dst_start=52, src_start=50, range_length=48),
        solve.MapEntry(dst_start=50, src_start=98, range_length=2),
    ]

    want = solve.Map(source="seed", target="soil", entries=map_entries)
    got = solve.build_maps_from_lines(given)[0]

    assert got == want


def test_chaining_maps():
    map_1_entries = [
        solve.MapEntry(dst_start=50, src_start=98, range_length=2),
        solve.MapEntry(dst_start=52, src_start=50, range_length=48),
    ]
    map_1 = solve.Map(source="seed", target="soil", entries=map_1_entries)
    map_2_entries = [
        solve.MapEntry(dst_start=0, src_start=15, range_length=37),
        solve.MapEntry(dst_start=37, src_start=52, range_length=2),
        solve.MapEntry(dst_start=39, src_start=0, range_length=15),
    ]
    map_2 = solve.Map(source="seed", target="soil", entries=map_2_entries)
    maps = [map_1, map_2]

    given = 50
    want = 37
    got = solve.calculate(given, maps)

    assert got == want


def test_part_1():
    want = 35
    got = solve.part_1(TEST_INPUT)
    assert got == want


def test_parse_seeds_as_ranges():
    given = "seeds: 79 14 55 13"
    want = [range(79, 79 + 14), range(55, 55 + 13)]
    got = solve.parse_seeds_as_ranges(given)
    assert got == want


def test_map_range_to_ranges():
    map_1_entries = [
        solve.MapEntry(dst_start=100, src_start=0, range_length=10),
        solve.MapEntry(dst_start=200, src_start=10, range_length=10),
    ]
    map_ = solve.Map(source="seed", target="soil", entries=map_1_entries)

    given = range(0, 20)
    want = [range(100, 110), range(200, 210)]
    got = solve.map_range_to_ranges(given, map_)

    assert got == want


def test_map_range_without_overlap():
    map_1_entries = [solve.MapEntry(dst_start=200, src_start=10, range_length=10)]
    map_ = solve.Map(source="seed", target="soil", entries=map_1_entries)

    given = range(0, 10)
    want = [range(0, 10)]
    got = solve.map_range_to_ranges(given, map_)

    assert got == want


def test_part_2():
    want = 46
    got = solve.part_2(TEST_INPUT)
    assert got == want
