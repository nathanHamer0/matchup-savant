# LOOK: disabled as is artifact of prior - now disregarded - design
# import pandas
# import os

# DATA_DIR = os.path.join(os.path.dirname(__file__), '../backend/data')

# def batter_run_value_per_100_std() -> dict:
#     BATTER_DIR = os.path.join(DATA_DIR, 'batters')
#     batter_pitch_rv_stats = pandas.read_csv(os.path.join(BATTER_DIR, "batter_pitch_rv_stats.csv"))
#     print("Standard Deviations of Batter Run Value Per 100 Pitches League-Wide for All Applicable Pitch Types\n-------------------------------------------------------------------------------------------")
#     batter_pitch_rv_stds = {}
#     for pitch in ["FF", "FC", "FS", "SI", "SL", "CU", "CH"]:
#         batter_pitch_rv_std = batter_pitch_rv_stats[pitch].std()
#         batter_pitch_rv_stds[pitch] = batter_pitch_rv_std
#         print(f'{pitch}: {batter_pitch_rv_std}')
#     return batter_pitch_rv_stds

# def pitcher_run_value_per_100_std() -> dict:
#     PITCHER_DIR = os.path.join(DATA_DIR, 'pitchers')
#     pitcher_pitch_rv_stats = pandas.read_csv(os.path.join(PITCHER_DIR, "pitcher_pitch_rv_stats.csv"))
#     print("Standard Deviations of Pitcher Run Value Per 100 Pitches League-Wide for All Applicable Pitch Types\n-------------------------------------------------------------------------------------------")
#     pitcher_pitch_rv_stds = {}
#     for pitch in ["FF", "FC", "FS", "SI", "SL", "CU", "CH"]:
#         pitcher_pitch_rv_std = pitcher_pitch_rv_stats[pitch].std()
#         pitcher_pitch_rv_stds[pitch] = pitcher_pitch_rv_std
#         print(f'{pitch}: {pitcher_pitch_rv_std}')
#     return pitcher_pitch_rv_stds

# def main():
#     batter_run_value_per_100_std()
#     pitcher_run_value_per_100_std()

# if __name__ == "__main__":
#     main()
