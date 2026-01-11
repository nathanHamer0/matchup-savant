from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import matchup, data_loader, name_utils

app = FastAPI(title="Matchup Savant")

# Connect frontend and backend servers Via Cross-Origin-Resource-Sharing (CORS) middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "https://nathanhamer0.github.io",
    ],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/players")
def get_players() -> dict:
    return {
        "batters": data_loader.get_all_batters(),
        "pitchers": data_loader.get_all_pitchers(),
    }


@app.get("/matchup")
def get_matchup(batter: str, pitcher: str) -> dict:
    batter_pitch_types, batter_zone = data_loader.load_batter(
        name_utils.snake_to_inverted_name(batter)
    )
    pitcher_pitch_types, pitcher_zone, total_pitches = data_loader.load_pitcher(
        name_utils.snake_to_inverted_name(pitcher)
    )
    return matchup.matchup(
        (batter, pitcher),
        batter_pitch_types,
        batter_zone,
        pitcher_pitch_types,
        pitcher_zone,
        total_pitches,
    )
