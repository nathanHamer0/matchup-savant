from fastapi.testclient import TestClient
import sys
import pathlib
import os
import pandas

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))

os.environ["ENV"] = "test"
from main import app

client = TestClient(app)


def df(entry: dict[str, list[int | float]]) -> pandas.DataFrame:
    """Generates a one-row one-column data-frame given a dicitionary entry.

    Args:
        entry (dict[str, list[int | float]]): Dicitionary entry.

    Returns:
        DataFrame: Data-frame version of given dictionary entry.
    """
    return pandas.DataFrame(entry)


def test_players_endpoint_valid(mocker):
    """Test the /players API route with valid input."""
    # Stub dependencies
    mocker.patch(
        "data_loader.get_all_batters",
        return_value=[{"standard_name": "Thing One", "snake": "thing_one"}],
    )
    mocker.patch(
        "data_loader.get_all_pitchers",
        return_value=[{"standard_name": "Thing Two", "snake": "thing_two"}],
    )

    # Fetch and verify
    response = client.get("/players")
    assert response.status_code == 200
    assert response.json() == {
        "batters": [{"standard_name": "Thing One", "snake": "thing_one"}],
        "pitchers": [{"standard_name": "Thing Two", "snake": "thing_two"}],
    }


def test_matchup_endpoint_valid(mocker):
    """Test the /matchup API route with valid input."""
    # Stub dependencies
    mocker.patch(
        "name_utils.snake_to_inverted_name",
        side_effect=["One, Thing", "Two, Thing"],
    )
    mocker.patch(
        "data_loader.load_batter",
        return_value=(
            {
                "ff": df({"batter_run_value_per_100": [0.4]}),
                "sl": df({"batter_run_value_per_100": [-0.1]}),
                "ch": df({"batter_run_value_per_100": [1.4]}),
            },
            {
                "1": df({"batter_run_value_per_100": [2.0]}),
                "2": df({"batter_run_value_per_100": [0.5]}),
                "3": df({"batter_run_value_per_100": [-0.3]}),
            },
        ),
    )
    mocker.patch(
        "data_loader.load_pitcher",
        return_value=(
            {
                "ff": df({"pitcher_run_value_per_100": [1.4]}),
                "sl": df({"pitcher_run_value_per_100": [0.9]}),
            },
            {
                "1": df({"pitcher_run_value_per_100": [1.0]}),
                "2": df({"pitcher_run_value_per_100": [-0.5]}),
            },
            100,
        ),
    )
    mocker.patch(
        "matchup.matchup",
        return_value={
            "player_matchup": ("thing_one", "thing_two"),
            "grand_score": 0.0,
            "grand_pitch_type_score": -1.0,
            "grand_zone_score": 1.0,
            "pitch_type_frequencies": {"ff": 0.7, "sl": 0.3},
            "zone_frequencies": {"1": 0.5, "2": 0.5},
            "pitch_type_scores": {"ff": -0.7, "sl": -0.3},
            "zone_scores": {"1": 0.5, "2": 0.5},
        },
    )

    # Fetch and verify
    response = client.get(
        "/matchup", params={"batter": "thing_one", "pitcher": "thing_two"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "player_matchup": [
            "thing_one",
            "thing_two",
        ],  # JSON encoding converts tuple to list
        "grand_score": 0.0,
        "grand_pitch_type_score": -1.0,
        "grand_zone_score": 1.0,
        "pitch_type_frequencies": {"ff": 0.7, "sl": 0.3},
        "zone_frequencies": {"1": 0.5, "2": 0.5},
        "pitch_type_scores": {"ff": -0.7, "sl": -0.3},
        "zone_scores": {"1": 0.5, "2": 0.5},
    }


# TODO Negative cases
