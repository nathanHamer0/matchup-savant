# BUG

import pytest
from fastapi.testclient import TestClient
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))
from main import app
import data_loader

client = TestClient(app)


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
