from __future__ import annotations

import threading
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from rag.engine import get_engine, peek_engine

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"

_boot_error: str | None = None
_boot_lock = threading.Lock()


def _safe_engine() -> ChatEngine:
    global _boot_error
    with _boot_lock:
        try:
            return get_engine()
        except Exception as exc:  # noqa: BLE001
            _boot_error = str(exc)
            raise


@asynccontextmanager
async def lifespan(_: FastAPI):
    thread = threading.Thread(target=_safe_engine, daemon=True)
    thread.start()
    yield


app = FastAPI(title="FH Data Chat", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if STATIC.exists():
    app.mount("/static", StaticFiles(directory=STATIC), name="static")


class HistoryTurn(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    history: list[HistoryTurn] = Field(default_factory=list)


@app.get("/")
def dashboard():
    html = ROOT / "dashboard_csuite_fhsaude.html"
    if html.exists():
        return FileResponse(html)
    return FileResponse(STATIC / "chat.html")


@app.get("/chat")
def chat_page():
    return FileResponse(STATIC / "chat.html")


@app.get("/api/health")
def health():
    engine = peek_engine()
    if engine is None:
        return {
            "ok": False,
            "ready": False,
            "index": _boot_error or "inicializando motor RAG",
            "error": _boot_error,
            "deals": 0,
            "chunks": 0,
            "model": None,
        }
    return {"ok": True, **engine.status, "error": _boot_error}


@app.post("/api/chat")
def chat(payload: ChatRequest):
    engine = peek_engine()
    if engine is None:
        raise HTTPException(status_code=503, detail=_boot_error or "Motor RAG ainda está subindo.")
    if not engine.status["ready"]:
        raise HTTPException(status_code=503, detail=f"Indexando a base: {engine.status['index']}")
    question = payload.message.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Mensagem vazia.")
    history = [turn.model_dump() for turn in payload.history]
    try:
        return engine.ask(question, history)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"Falha no Gemini: {exc}") from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8765, reload=False)
