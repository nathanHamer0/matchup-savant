from pandas import DataFrame

# from scripts.compute_empirical_distribution import percentalize_matchup [LOOK: currently disabled]

# Update normality scale after fielding yields across database [TODO]
# See sources.txt
# Computed via scripts/compute_league_stats.py
# MEAN_RUN_VAL_PER_100 = 0.000
# BATTER_STD_RUN_VAL_PER_100 = {
#     'ff': 0.938,
#     'fc': 2.077,
#     'fs': 2.573,
#     'si': 1.419,
#     'sl': 0.956,
#     'cu': 1.650,
#     'ch': 1.678
# }
# PITCHER_STD_RUN_VAL_PER_100 = {
#     'ff': 0.892,
#     'FC': 4.612,
#     'FS': 2.585,
#     'SI': 1.810,
#     'SL': 1.671,
#     'CU': 1.363,
#     'CH': 1.503
# }

# Arbitraraly selected
PITCH_TYPE_WEIGHT = 0.5
ZONE_WEIGHT = 0.5


def get_freqs(
    pitcher_splits: dict[str | int, DataFrame], pitcher_total: int
) -> dict[str | int, float]:
    """Receives a pitcher's split data and total pitches as arguments, calculates the frequency per split, and returns a dictionary of those splits' frequencies (for that pitcher).

    Args:
        pitcher_splits (dict[str|int, DataFrame]): Logged rows consisting of pitcher split-adherent data (including number of pitches) for every logged split.
        pitcher_total (int): Total number of pitches thrown by pitcher.

    Returns:
        dict[str|int, float]: Pitch frequencies by split (for the given pitcher).
    """
    # Divide number of split-adherent pitches by total number of pitches for every pitch split
    freqs = {}
    for s in pitcher_splits:
        freqs[s] = pitcher_splits[s]["pitches"].iloc[0] / pitcher_total
    return freqs


def pitch_type_matchup(
    batter_pitch_types: dict[str, DataFrame],
    pitcher_pitch_types: dict[str, DataFrame],
    pitch_type_freqs: dict[str, float],
) -> dict[str, float | dict[str, float]]:
    """Receives a batter's and pitcher's respective pitch-type data as arguments, compares said data against eachother, and returns a matchup score.

    Args:
        batter_pitch_types (dict[str, DataFrame]): Logged rows consisting of batter pitch-type data (including RV/100) for every logged pitch-type.
        pitcher_pitch_types (dict[str, DataFrame]): Logged rows consisting of pitcher pitch-type data (including RV/100) for every logged pitch-type.
        pitch_type_freqs (dict[str, float]): Pitch frequencies by pitch-type (for the given pitcher).

    Returns:
        dict[str, float | dict[str, float]]:
            Dictionary with keys:
                - "grand_pitch_type_score": float; pitcher-arsenal-cumulative pitch-type matchup score.
                - "pitch_type_scores": dict[str, float]; [TODO] normalized and frequency-weighted matchup scores per pitch-type; (+) for batter advantage, (0) for no advantage, and (-) for pitcher advantage.
    """
    pitch_type_scores = {}
    batter_grand_pitch_type_score = 0.0
    pitcher_grand_pitch_type_score = 0.0
    for p in pitcher_pitch_types:
        # Locate pitch's usage frequency and respective run values and weight said run values by usage frequency and [TODO] normalize them to a z-score
        freq = pitch_type_freqs[p]
        if p not in batter_pitch_types:
            batter_pitch_type_score = 0.0
        else:
            batter_pitch_type_score = (
                freq * batter_pitch_types[p]["batter_run_value_per_100"].iloc[0]
            )
        pitcher_pitch_type_score = (
            freq * pitcher_pitch_types[p]["pitcher_run_value_per_100"].iloc[0]
        )

        # Log to returnables and compare respective normalized and frequency-weighted run values
        batter_grand_pitch_type_score += batter_pitch_type_score
        pitcher_grand_pitch_type_score += pitcher_pitch_type_score
        pitch_type_scores[p] = (
            batter_pitch_type_score - pitcher_pitch_type_score
        )  # imposed direction

    return {
        "grand_pitch_type_score": batter_grand_pitch_type_score
        - pitcher_grand_pitch_type_score,
        "pitch_type_scores": pitch_type_scores,
    }


def zone_matchup(
    batter_zone: dict[int, DataFrame],
    pitcher_zone: dict[int, DataFrame],
    zone_freqs: dict[int, float],
) -> dict[str, float | dict[str, float]]:
    """Receives a batter's and pitcher's respective zone data as arguments, compares said data against eachother, and returns a matchup score.

    Args:
        batter_zone (dict[int, DataFrame]): Logged rows consisting of batter zone data (including RV/100) for every logged zone-cell.
        pitcher_zone (dict[int, DataFrame]): Logged rows consisting of pitcher zone data (including RV/100) for every logged zone-cell.
        zone_freqs (dict[int, float]): Pitch frequencies by zone-cell (for the given pitcher).

    Returns:
        dict[str, float | dict[str, float]]:
            Dictionary with keys:
                - "grand_zone_score": float; cumulative zone location matchup score.
                - "zone_scores": dict[str, float]; [TODO] normalized and frequency-weighted matchup scores per zone cell; (+) for batter advantage, (0) for no advantage, and (-) for pitcher advantage.
    """
    zone_scores = {}
    batter_zone_score = 0.0
    pitcher_zone_score = 0.0
    for z in pitcher_zone:
        # Locate cell's usage frequency and respective run values and weight said run values by usage frequency and [TODO] normalize them to a z-score
        freq = zone_freqs[z]
        if z not in batter_zone:
            batter_zone_cell_score = 0.0
        else:
            batter_zone_cell_score = (
                freq * batter_zone[z]["batter_run_value_per_100"].iloc[0]
            )
        pitcher_zone_cell_score = (
            freq * pitcher_zone[z]["pitcher_run_value_per_100"].iloc[0]
        )

        # Log to returnables and compare respective normalized and frequency-weighted run values
        batter_zone_score += batter_zone_cell_score
        pitcher_zone_score += pitcher_zone_cell_score
        zone_scores[z] = (
            batter_zone_cell_score - pitcher_zone_cell_score
        )  # inherent direction

    return {
        "grand_zone_score": batter_zone_score - pitcher_zone_score,
        "zone_scores": zone_scores,
    }


def matchup(
    player_matchup: tuple[str],
    batter_pitch_types: dict[str, DataFrame],
    batter_zone: dict[int, DataFrame],
    pitcher_pitch_types: dict[str, DataFrame],
    pitcher_zone: dict[int, DataFrame],
    pitcher_total: int,
) -> dict[str, tuple[str] | float | dict[str, float]]:
    """Receives a batter's and pitcher's respective pitch-type and zone data as arguments, compares said data against eachother, and returns a matchup score.

    Args:
        player_matchup (tuple[str]): players of the matchup.
        batter_pitch_types (dict[str, DataFrame]): Logged rows consisting of batter pitch-type data (including RV/100) for every logged pitch-type.
        batter_zone (dict[int, DataFrame]): Logged rows consisting of batter zone data (including RV/100) for every logged zone-cell.
        pitcher_pitch_types (dict[str, DataFrame]): Logged rows consisting of pitcher pitch-type data (including RV/100) for every logged pitch-type.
        pitcher_zone (dict[int, DataFrame]): Logged rows consisting of pitcher zone data (including RV/100) for every logged zone-cell.
        pitcher_total (int): Total number of pitches thrown by pitcher.

    Returns:
        dict[str, tuple[str] | float | dict[str, float]]:
            Dictionary with keys:
                - "player_matchup": tuple[str]; players of the matchup.
                - "grand_score": float; pitch-type-zone-cumulative matchup score.
                - "grand_pitch_type_score": float; pitch-type-cumulative matchup score.
                - "grand_zone_score": float; zone-cumulative matchup score.
                - "pitch_type_frequencies": dict[str, float]; usage-frequencies by pitch-type (for the pitcher).
                - "zone_frequencies": dict[int, float]; frequencies by zone-cell (for the pitcher).
                - "pitch_type_scores": dict[str, float]; [TODO] normalized and frequency-weighted matchup scores per pitch-type; (+) for batter advantage, (0) for no advantage, and (-) for pitcher advantage.
                - "zone_scores": dict[str, float]; [TODO] normalized and frequency-weighted matchup scores per zone cell; (+) for batter advantage, (0) for no advantage, and (-) for pitcher advantage.
    """
    pitch_type_freqs = get_freqs(pitcher_pitch_types, pitcher_total)
    zone_freqs = get_freqs(pitcher_zone, pitcher_total)
    pitch_type_matchup_scores = pitch_type_matchup(
        batter_pitch_types, pitcher_pitch_types, pitch_type_freqs
    )
    zone_matchup_scores = zone_matchup(batter_zone, pitcher_zone, zone_freqs)

    return {
        "player_matchup": player_matchup,
        "grand_score": PITCH_TYPE_WEIGHT
        * pitch_type_matchup_scores["grand_pitch_type_score"]
        + ZONE_WEIGHT * zone_matchup_scores["grand_zone_score"],
        "grand_pitch_type_score": pitch_type_matchup_scores["grand_pitch_type_score"],
        "grand_zone_score": zone_matchup_scores["grand_zone_score"],
        "pitch_type_frequencies": pitch_type_freqs,
        "zone_frequencies": zone_freqs,
        "pitch_type_scores": pitch_type_matchup_scores["pitch_type_scores"],
        "zone_scores": zone_matchup_scores["zone_scores"],
    }
