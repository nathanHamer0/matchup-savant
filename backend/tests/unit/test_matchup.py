import pytest
from unittest.mock import Mock
import pandas
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))
import matchup


def df(entry: dict[str, list[int | float]]) -> pandas.DataFrame:
    """Generates a one-row one-column data-frame given a dicitionary entry.

    Args:
        entry (dict[str, list[int | float]]): Dicitionary entry.

    Returns:
        DataFrame: Data-frame version of given dictionary entry.
    """
    return pandas.DataFrame(entry)


def test_get_freqs_valid():
    """Test a split-frequeuncy distribution with valid input."""
    # Define inputs
    pitcher_splits = {"ff": df({"pitches": [70]}), "sl": df({"pitches": [30]})}
    pitcher_total = 100

    # Call and verify
    res = matchup.get_freqs(pitcher_splits, pitcher_total)
    assert res == pytest.approx({"ff": 0.7, "sl": 0.3})


def test_pitch_type_matchup_valid():
    """Test a per-pitch-type matchup with valid input."""
    # Define inputs
    batter_pitch_types = {
        "ff": df({"batter_run_value_per_100": [0.4]}),
        "sl": df({"batter_run_value_per_100": [-0.1]}),
        "ch": df({"batter_run_value_per_100": [1.4]}),
    }
    pitcher_pitch_types = {
        "ff": df({"pitcher_run_value_per_100": [1.4]}),
        "sl": df({"pitcher_run_value_per_100": [0.9]}),
    }
    pitch_type_freqs = {"ff": 0.7, "sl": 0.3}

    # Call and verify
    res = matchup.pitch_type_matchup(
        batter_pitch_types, pitcher_pitch_types, pitch_type_freqs
    )
    assert res["grand_pitch_type_score"] == pytest.approx(-1.0)
    assert res["pitch_type_scores"] == pytest.approx({"ff": -0.7, "sl": -0.3})


def test_zone_matchup_valid():
    """Test a per-zone matchup with valid input."""
    # Define inputs
    batter_zone = {
        "1": df({"batter_run_value_per_100": [2.0]}),
        "2": df({"batter_run_value_per_100": [0.5]}),
        "3": df({"batter_run_value_per_100": [-0.3]}),
    }
    pitcher_zone = {
        "1": df({"pitcher_run_value_per_100": [1.0]}),
        "2": df({"pitcher_run_value_per_100": [-0.5]}),
    }
    zone_freqs = {"1": 0.5, "2": 0.5}

    # Call and verify
    res = matchup.zone_matchup(batter_zone, pitcher_zone, zone_freqs)
    assert res["grand_zone_score"] == pytest.approx(1.0)
    assert res["zone_scores"] == pytest.approx({"1": 0.5, "2": 0.5})


def test_matchup_valid(mocker):
    """Test a comprehensive matchup with valid input."""
    # Define inputs
    player_matchup = ("thing_one", "thing_two")
    batter_pitch_types = {
        "ff": df({"batter_run_value_per_100": [0.4]}),
        "sl": df({"batter_run_value_per_100": [-0.1]}),
        "ch": df({"batter_run_value_per_100": [1.4]}),
    }
    pitcher_pitch_types = {
        "ff": df({"pitcher_run_value_per_100": [1.4]}),
        "sl": df({"pitcher_run_value_per_100": [0.9]}),
    }
    batter_zone = {
        "1": df({"batter_run_value_per_100": [2.0]}),
        "2": df({"batter_run_value_per_100": [0.5]}),
        "3": df({"batter_run_value_per_100": [-0.3]}),
    }
    pitcher_zone = {
        "1": df({"pitcher_run_value_per_100": [1.0]}),
        "2": df({"pitcher_run_value_per_100": [-0.5]}),
    }
    pitcher_total = 100

    # Stub dependencies
    mocker.patch(
        "matchup.get_freqs",
        side_effect=[{"ff": 0.7, "sl": 0.3}, {"1": 0.5, "2": 0.5}],
    )
    mocker.patch(
        "matchup.pitch_type_matchup",
        return_value={
            "grand_pitch_type_score": -1.0,
            "pitch_type_scores": {"ff": -0.7, "sl": -0.3},
        },
    )
    mocker.patch(
        "matchup.zone_matchup",
        return_value={"grand_zone_score": 1.0, "zone_scores": {"1": 0.5, "2": 0.5}},
    )

    # Call and verify
    res = matchup.matchup(
        player_matchup,
        batter_pitch_types,
        batter_zone,
        pitcher_pitch_types,
        pitcher_zone,
        pitcher_total,
    )
    assert res == {
        "player_matchup": player_matchup,
        "grand_score": 0.0,
        "grand_pitch_type_score": -1.0,
        "grand_zone_score": 1.0,
        "pitch_type_frequencies": {"ff": 0.7, "sl": 0.3},
        "zone_frequencies": {"1": 0.5, "2": 0.5},
        "pitch_type_scores": {"ff": -0.7, "sl": -0.3},
        "zone_scores": {"1": 0.5, "2": 0.5},
    }


# TODO Negative cases
