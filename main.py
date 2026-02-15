from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from engine import engine

app = FastAPI()

# Allow frontend (localhost:3000) to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/start")
async def start():
    return engine.start_session()


@app.post("/answer")
async def answer(data: dict):
    session_id = data.get("session_id")
    value = data.get("value")

    return engine.submit_answer(session_id, value)