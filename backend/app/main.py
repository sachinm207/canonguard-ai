import time
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .config import settings
from .db.clickhouse import ch_engine
from .db.seed_chronoverse import seed_chronoverse_data
from .agents.orchestrator import orchestrator, ValidationResponse
from .agents.mitigation_agent import MitigationOption
from .agents.causal_agent import ContradictionViolation

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("canonguard.api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Boot sequence: Initialize database and seed ChronoVerse lore
    logger.info("Initializing CanonGuard Engine and Seeding ChronoVerse...")
    seed_chronoverse_data()
    yield
    logger.info("Shutting down CanonGuard Engine.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Sub-20ms Cinematic Franchise Continuity & Retcon Prevention Engine powered by ClickHouse & Gemini.",
    lifespan=lifespan
)

# Enable CORS for Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SceneValidationRequest(BaseModel):
    text: str
    scene_year: int = 1982
    location: str = "Berlin"
    screenplay_title: str = "Untitled Screenplay"

import os
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

@app.get("/")
def root():
    index_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/index.html"))
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "track": "ClickHouse Partner Track",
        "universe": settings.UNIVERSE_ID,
        "status": "ONLINE",
        "docs": "/docs"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "HEALTHY",
        "engine_mode": "Native ClickHouse" if ch_engine.is_native else "Embedded High-Performance Columnar",
        "characters_loaded": len(ch_engine.characters),
        "events_loaded": len(ch_engine.timeline_events),
        "relationships_loaded": len(ch_engine.relationships),
        "lore_rules_loaded": len(ch_engine.lore_rules),
        "audit_logs_count": len(ch_engine.audit_logs),
        "target_latency_budget": "< 20ms"
    }

@app.post("/api/validate-scene", response_model=ValidationResponse)
def validate_scene(req: SceneValidationRequest):
    """
    Validate a single screenplay action line or slugline in real-time.
    Returns sub-20ms retcon evaluation and 3 creative mitigation solutions.
    """
    result = orchestrator.validate_screenplay_stream(
        text=req.text,
        screenplay_title=req.screenplay_title,
        fallback_year=req.scene_year,
        fallback_location=req.location
    )
    return result

@app.get("/api/lore/characters")
def get_characters(query: Optional[str] = None):
    """Browse or search canonical characters in the universe."""
    chars = ch_engine.characters
    if query:
        q = query.lower()
        chars = [c for c in chars if q in c["name"].lower() or any(q in a.lower() for a in c.get("aliases", []))]
    return {"total": len(chars), "characters": chars[:50]}

@app.get("/api/lore/timeline")
def get_timeline():
    """Returns canonical timeline events."""
    return {"total": len(ch_engine.timeline_events), "events": ch_engine.timeline_events}

@app.get("/api/lore/rules")
def get_lore_rules():
    """Returns absolute physical, biological, and technological lore invariants."""
    return {"total": len(ch_engine.lore_rules), "rules": ch_engine.lore_rules}

@app.get("/api/audit-logs")
def get_audit_logs():
    """Returns real-time telemetry logs of caught retcons and query latencies."""
    return {"total": len(ch_engine.audit_logs), "logs": ch_engine.audit_logs}

@app.websocket("/ws/screenplay")
async def websocket_screenplay_stream(websocket: WebSocket):
    """
    Bi-directional real-time WebSocket stream for the Screenplay Web Editor.
    As the writer types, debounced tokens stream in and instant squiggly lint
    decorations are emitted back in sub-20 milliseconds.
    """
    await websocket.accept()
    logger.info("Screenplay WebSocket stream client connected.")
    try:
        while True:
            data = await websocket.receive_json()
            # Expected payload: {"text": "...", "scene_year": 1982, "location": "Berlin", "title": "..."}
            text = data.get("text", "")
            year = data.get("scene_year", 1982)
            location = data.get("location", "Berlin")
            title = data.get("title", "Active Screenplay")

            if not text.strip():
                await websocket.send_json({"type": "EMPTY_LINE"})
                continue

            result = orchestrator.validate_screenplay_stream(
                text=text,
                screenplay_title=title,
                fallback_year=year,
                fallback_location=location
            )

            await websocket.send_json({
                "type": "LINT_RESULT",
                "status": result.status,
                "scene_year": result.scene_year,
                "location": result.location,
                "query_latency_ms": result.query_latency_ms,
                "violations": [v.model_dump() for v in result.violations],
                "mitigations": [m.model_dump() for m in result.mitigations],
                "claim_details": result.claim_details
            })

    except WebSocketDisconnect:
        logger.info("Screenplay WebSocket client disconnected.")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.close()
        except:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=False)
