from fastapi import FastAPI

app = FastAPI(title="Matchup Savant")

@app.get("/health")
def health():
    return {"status": "ok"}