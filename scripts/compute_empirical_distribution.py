# LOOK: currently disabled
# TODO: requires documentation
# import json, random, copy
# from backend import data_loader, matchup, name_utils

# SCALARS = [
#     "grand_score",
#     "grand_pitch_type_score",
#     "grand_zone_score",
#     "pitch_type_scores",
#     "zone_scores",
# ]


# def compute_all_matchups():
#     with open("matchup_yields.jsonl", "w") as f:
#         batters = data_loader.get_all_batters()
#         pitchers = data_loader.get_all_pitchers()
#         loaded_batters = {}
#         loaded_pitchers = {}
#         i = 0
#         while i < 50000:
#             b = random.choice(batters)["snake"]
#             p = random.choice(pitchers)["snake"]

#             if b in loaded_batters:
#                 b_pitch_type = loaded_batters[b][0]
#                 b_zone = loaded_batters[b][1]
#             else:
#                 b_pitch_type, b_zone = data_loader.load_batter(
#                     name_utils.snake_to_inverted_name((b))
#                 )
#                 loaded_batters[b] = [b_pitch_type, b_zone]
#             if p in loaded_pitchers:
#                 p_pitch_type = loaded_pitchers[p][0]
#                 p_zone = loaded_pitchers[p][1]
#                 total_pitches = loaded_pitchers[p][2]
#             else:
#                 p_pitch_type, p_zone, total_pitches = data_loader.load_pitcher(
#                     name_utils.snake_to_inverted_name((p))
#                 )
#                 loaded_pitchers[p] = [p_pitch_type, p_zone, total_pitches]

#             res = matchup.matchup(
#                 (b, p), b_pitch_type, b_zone, p_pitch_type, p_zone, total_pitches
#             )
#             f.write(json.dumps(res, default=float) + "\n")
#             i += 1


# def get_ranked_scalar_lists():
#     with open("matchup_yields.jsonl", "r") as f:
#         # Initalize destination structure
#         dest = {}
#         for scal in SCALARS:
#             if "grand" in scal:
#                 dest[scal] = []
#             else:
#                 dest[scal] = {}
#                 sample = json.loads(f.readline())[scal]
#                 for split in sample:
#                     dest[scal][split] = []
#                 f.seek(0)

#         # Extract scalar yields from each matchup
#         for line in f:
#             matchup = json.loads(line)
#             for scal in SCALARS:
#                 src = matchup[scal]

#                 # Handle sub-scores (dict[str, float])
#                 if type(src) == dict:
#                     for split in src:
#                         if split not in dest[scal]:
#                             dest[scal][split] = []
#                         dest[scal][split].append(src[split])

#                 # Handle grand-scores (float)
#                 else:
#                     dest[scal].append(src)

#         # Sort (rank) scalar yields
#         for scal in SCALARS:
#             if "grand" in scal:
#                 dest[scal] = sorted(dest[scal])  # BUG
#             else:
#                 for split in dest[scal]:
#                     dest[scal][split] = sorted(dest[scal][split])  # BUG

#     with open("ranked_scalar_yields.jsonl", "w") as f:
#         f.write(json.dumps(dest, default=float) + "\n")


# def get_rank(score: float, rankings: list[float]) -> int:
#     # (ascending) binary search BUG
#     lo, hi = 0, len(rankings)
#     while lo < hi:
#         mid = (lo + hi) // 2
#         if score >= rankings[mid]:
#             hi = mid
#         else:
#             lo = mid + 1
#     return lo + 1


# def get_rank_partition(score: float, rankings: list[float]) -> int | float:
#     #     # Partition ranking scales into batter-favourable (>0.0) and pitcher-favourable (<0.0) scales
#     #     sign_rankings = []
#     #     if score > 0.0:
#     #         for s in rankings:
#     #             if s > 0:
#     #                 sign_rankings.append(s)
#     #         sign_rankings.reverse()
#     #     elif score < 0.0:
#     #         for s in rankings:
#     #             if s < 0:
#     #                 sign_rankings.append(s)
#     #         sign_rankings.reverse()
#     #     else:
#     #         return 0.5, 1

#     #     # binary search
#     #     lo, hi = 0, len(sign_rankings)
#     #     while hi > lo:
#     #         mid = (hi + lo) // 2
#     #         if score < sign_rankings[mid]:
#     #             lo = mid + 1
#     #         else:
#     #             hi = mid
#     #     return lo + 1, len(sign_rankings)
#     ...


# def percentalize_matchup(matchup: dict[str, float | dict[str, float]]):
#     with open("ranked_scalar_yields.jsonl", "r") as f:
#         rankings = json.loads(f.read())

#     ret_matchup = copy.deepcopy(matchup)
#     for scal in SCALARS:
#         if "grand" in scal:
#             rank = get_rank(matchup[scal], rankings[scal])
#             N = len(rankings[scal])
#             ret_matchup[scal] = 100 * (rank - 0.5) / N
#         else:
#             for split in matchup[scal]:
#                 rank = get_rank(matchup[scal][split], rankings[scal][str(split)])
#                 N = len(rankings[scal][str(split)])
#                 ret_matchup[scal][split] = 100 * (rank - 0.5) / N
#     return ret_matchup


# if __name__ == "__main__":
#     get_ranked_scalar_lists()
