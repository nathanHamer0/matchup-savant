from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# from fastapi.middleware.cors import CORSMiddleware

import matchup
import data_loader
import name_utils

# app = FastAPI(title="Matchup Savant")
app = FastAPI()

# # Connect frontend and backend servers Via Cross-Origin-Resource-Sharing (CORS) middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:8080",
#         "https://nathanhamer0.github.io",
#     ],  # frontend origin
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
    pass


@app.get("/players")
async def get_players() -> dict:
    return {
        "batters": data_loader.get_all_batters(),
        "pitchers": data_loader.get_all_pitchers(),
    }
    pass


@app.get("/matchup")
async def get_matchup(batter: str, pitcher: str) -> dict:
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
    pass


# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")


# Serve index.html at root
@app.get("/")
async def read_root():
    return FileResponse("static/index.html")
