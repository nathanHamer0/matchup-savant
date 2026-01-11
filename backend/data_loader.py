import pandas
from pandas import DataFrame
import os
from . import name_utils

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

PITCH_TYPES = ["ff", "fc", "si", "fs", "cu", "sl", "ch", "st", "kc"]
ZONES = range(1, 19)

def load_batter(name: str) -> dict[str|int, DataFrame]:
    """Receives a batter's name as an argument, from local Baseball Savant .csv's, extracts the batter's row of statistical data for every applicable pitch-type and zone-cell, and returns a dictionary of those pitch-types' and zone-cells' rows of data (for that batter).

    Args:
        name (str): Batter's name.

    Returns:
        dict[str|int, DataFrame]: statistical data-frames by pitch-type and/or zone-cell (for the given batter).
    """
    BATTER_DIR = os.path.join(DATA_DIR, 'batters_alpha')
    
    # Retrieve and log batter's data-frame for every applicable pitch-type
    BATTER_PITCH_TYPE_DIR = os.path.join(BATTER_DIR, 'batter_pitch_type')
    pitch_types = {}
    for p in PITCH_TYPES:
        pitch_type = pandas.read_csv(os.path.join(BATTER_PITCH_TYPE_DIR, f'batter_{p}.csv'))
        batter_pitch_type = pitch_type[(pitch_type["player_name"]).str.lower() == name.lower()]    # Standardize to lower-case in case of 'McDonald's' type captialization obscuring equivalencies
        if not batter_pitch_type.empty:
            pitch_types[p] = batter_pitch_type
        
    # Retrieve and log batter's data-frame for every applicable zone-cell
    BATTER_ZONE_DIR = os.path.join(BATTER_DIR, f'batter_zone')
    zones = {}
    for z in ZONES:
        zone = pandas.read_csv(os.path.join(BATTER_ZONE_DIR, f'batter_zone_{z}.csv'))
        batter_zone = zone[(zone["player_name"]).str.lower() == name.lower()]
        if not batter_zone.empty:
            zones[z] = batter_zone
        
    return pitch_types, zones

def load_pitcher(name: str) -> dict[str|int, DataFrame] | int:
    """Receives a pitcher's name as an argument, from local Baseball Savant .csv's, extracts the pitcher's row of statistical data for every applicable pitch-type and zone-cell, and returns a dictionary of those pitch-types' and zone-cells' rows of data (for that pitcher).

    Args:
        name (str): Pitcher's name.

    Returns:
        dict[str|int, DataFrame]: statistical data-frames by pitch-type and/or zone-cell (for the given pitcher).
        int: Total number of pitches thrown by pitcher.
    """
    PITCHER_DIR = os.path.join(DATA_DIR, 'pitchers_alpha')
    
    # Retrieve and log pitcher's data-frame for every applicable pitch-type
    PITCHER_PITCH_TYPE_DIR = os.path.join(PITCHER_DIR, 'pitcher_pitch_type')
    pitch_types = {}
    for p in PITCH_TYPES:
        pitch_type = pandas.read_csv(os.path.join(PITCHER_PITCH_TYPE_DIR, f'pitcher_{p}.csv'))
        pitcher_pitch_type = pitch_type[(pitch_type["player_name"]).str.lower() == name.lower()]
        if not pitcher_pitch_type.empty:
            pitch_types[p] = pitcher_pitch_type
        
    # Retrieve and log pitcher's data-frame for every applicable zone-cell
    PITCHER_ZONE_DIR = os.path.join(PITCHER_DIR, f'pitcher_zone')
    zones = {}
    for z in ZONES:
        zone = pandas.read_csv(os.path.join(PITCHER_ZONE_DIR, f'pitcher_zone_{z}.csv'))
        pitcher_zone = zone[(zone["player_name"]).str.lower() == name.lower()]
        if not pitcher_zone.empty:
            zones[z] = pitcher_zone
            
    # Retrieve pitcher's total number of pitches
    pitch_total = pandas.read_csv(os.path.join(PITCHER_DIR, f'pitcher_total.csv'))
    pitcher = pitch_total[(pitch_total["player_name"]).str.lower() == name.lower()]
    if not pitcher.empty:
            total_pitches = pitcher["pitches"].iloc[0]

    try:
        return pitch_types, zones, total_pitches
    except:
        raise KeyError(f'ERROR: {name} does not exist within the database.')
    
def get_all_batters() -> list[str]:
    BATTER_DIR = os.path.join(DATA_DIR, 'batters_alpha')
    batters_df = pandas.read_csv(os.path.join(BATTER_DIR, f'batter_total.csv'))
    
    batters = []
    for b in batters_df["player_name"]:
        batters.append({"standard_name": name_utils.inverted_name_to_standard_name(b), "snake": name_utils.inverted_name_to_snake(b)})
        
    return batters

def get_all_pitchers() -> list[dict[str, str]]:
    PITCHER_DIR = os.path.join(DATA_DIR, 'pitchers_alpha')
    pitchers_df = pandas.read_csv(os.path.join(PITCHER_DIR, f'pitcher_total.csv'))
    
    pitchers = []
    for p in pitchers_df["player_name"]:
        pitchers.append({"standard_name": name_utils.inverted_name_to_standard_name(p), "snake": name_utils.inverted_name_to_snake(p)})
        
    return pitchers