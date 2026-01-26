from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import traceback

import chess

from engine import play_move

app = FastAPI(title='Chess AI Backend')

# ---------------------------
# CORS (for React frontend)
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrict later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Request model
# ---------------------------
class MoveRequest(BaseModel):
    fen: str
    move: str
    max_time: float = 1.0   # seconds

# ---------------------------
# Health check
# ---------------------------
@app.get("/")
def health():
    return {"status": "ok"}

# ---------------------------
# Play move endpoint
# ---------------------------
@app.post("/move")
def move_piece(req: MoveRequest):
    try:
        new_fen, ai_move = play_move(fen=req.fen, move_uci=req.move, max_time=req.max_time)

        return {
            "fen": new_fen,
            "ai_move": ai_move
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))