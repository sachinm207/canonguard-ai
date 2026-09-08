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
from .agents.ingestion_agent import ingestion_agent

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
        "active_universe": ch_engine.get_active_universe(),
        "target_latency_budget": "< 20ms"
    }

@app.get("/api/universes")
def get_universes():
    """Returns all available franchise universes and the active one."""
    return {
        "active_universe": ch_engine.get_active_universe(),
        "universes": ch_engine.get_all_universes()
    }

class SwitchUniverseRequest(BaseModel):
    universe_id: str

@app.post("/api/universe/switch")
def switch_universe(req: SwitchUniverseRequest):
    """Switches the active franchise canon in the ClickHouse engine."""
    success = ch_engine.switch_universe(req.universe_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Universe '{req.universe_id}' not found.")
    active = ch_engine.get_active_universe()
    logger.info(f"Switched active universe to {active['name']} ({req.universe_id})")
    return {"status": "SUCCESS", "active_universe": active}

@app.get("/api/universes/archived")
def get_archived_universes():
    """Returns all archived universes with lore roster and rule details."""
    archived = ch_engine.get_archived_universes()
    return {
        "total": len(archived),
        "universes": archived
    }

class ArchiveUniverseRequest(BaseModel):
    universe_id: str

@app.post("/api/universe/archive")
def archive_universe_post(req: ArchiveUniverseRequest):
    """Archives an active universe into the cold lore repository."""
    success = ch_engine.archive_universe(req.universe_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Universe '{req.universe_id}' not found.")
    return {
        "status": "SUCCESS",
        "archived_universe_id": req.universe_id,
        "active_universe": ch_engine.get_active_universe()
    }

@app.post("/api/universe/{universe_id}/archive")
def archive_universe_path_post(universe_id: str):
    """Archives an active universe into the cold lore repository (path param)."""
    return archive_universe_post(ArchiveUniverseRequest(universe_id=universe_id))

class RestoreUniverseRequest(BaseModel):
    universe_id: str

@app.post("/api/universe/restore")
def restore_universe_post(req: RestoreUniverseRequest):
    """Restores an archived universe back into active ClickHouse engine memory."""
    success = ch_engine.restore_archived_universe(req.universe_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Archived universe '{req.universe_id}' not found.")
    return {
        "status": "SUCCESS",
        "restored_universe_id": req.universe_id,
        "active_universe": ch_engine.get_active_universe()
    }

@app.post("/api/universe/{universe_id}/restore")
def restore_universe_path_post(universe_id: str):
    """Restores an archived universe back into active ClickHouse engine memory (path param)."""
    return restore_universe_post(RestoreUniverseRequest(universe_id=universe_id))

@app.delete("/api/universe/archived/{universe_id}")
def delete_archived_universe(universe_id: str):
    """Permanently purges an archived universe."""
    success = ch_engine.delete_archived_universe(universe_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Archived universe '{universe_id}' not found.")
    return {
        "status": "SUCCESS",
        "deleted_universe_id": universe_id
    }

@app.delete("/api/universe/{universe_id}")
def delete_universe(universe_id: str):
    """Deletes a custom franchise universe from ClickHouse."""
    success = ch_engine.delete_universe(universe_id)
    if not success:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete universe '{universe_id}'. Either it does not exist or it is a protected core universe."
        )
    return {
        "status": "SUCCESS",
        "deleted_universe_id": universe_id,
        "active_universe": ch_engine.get_active_universe()
    }

class DeleteUniverseRequest(BaseModel):
    universe_id: str

@app.post("/api/universe/delete")
def delete_universe_post(req: DeleteUniverseRequest):
    """Deletes a custom franchise universe from ClickHouse (POST alternative)."""
    return delete_universe(req.universe_id)

@app.post("/api/universe/{universe_id}/delete")
def delete_universe_path_post(universe_id: str):
    """Deletes a custom franchise universe from ClickHouse (POST path alternative)."""
    return delete_universe(universe_id)

@app.post("/api/universe/reset-defaults")
def reset_default_universes():
    """Restores all default built-in canons and custom samples."""
    universes = ch_engine.reset_defaults()
    return {
        "status": "SUCCESS",
        "universes": universes,
        "active_universe": ch_engine.get_active_universe()
    }

class IngestLoreDocumentRequest(BaseModel):
    universe_name: str
    genre: Optional[str] = "Custom Sci-Fi / Fantasy"
    era: Optional[str] = "Current Timeline"
    description: Optional[str] = "User-uploaded franchise story bible."
    document_content: str

@app.post("/api/universe/ingest-document")
def ingest_lore_document(req: IngestLoreDocumentRequest):
    """
    Ingests a user's custom Lore Bible / Story Bible document into ClickHouse.
    Extracts characters, dates, destroyed relics, and universe invariants,
    registers the custom universe, and immediately activates it.
    Rejects duplicate franchise names.
    """
    import re
    import uuid

    # Prevent duplicate universe names
    existing = ch_engine.find_universe_by_name(req.universe_name)
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"A universe named '{req.universe_name}' already exists (ID: {existing['id']}). Please choose a unique name or delete the existing universe first."
        )

    clean_name = re.sub(r'[^A-Z0-9]', '_', req.universe_name.upper())[:15].strip('_')
    uid = f"CUSTOM_{clean_name}_{str(uuid.uuid4())[:4]}"
    
    characters = []
    relationships = []
    rules = []
    events = []

    # 1. Try parsing as JSON first
    import json
    doc_trimmed = req.document_content.strip()
    is_json = False
    if doc_trimmed.startswith("{") or doc_trimmed.startswith("["):
        try:
            parsed = json.loads(doc_trimmed)
            is_json = True
            if isinstance(parsed, dict):
                for c in parsed.get("characters", []):
                    c_name = c.get("name", "Unknown")
                    d_year = c.get("death_year")
                    s_start = c.get("stasis_start_year")
                    s_end = c.get("stasis_end_year")
                    stat = c.get("status", ("STASIS" if s_start else ("DEAD" if d_year else "ALIVE"))).upper()
                    characters.append({
                        "character_id": str(uuid.uuid4()),
                        "name": c_name,
                        "aliases": c.get("aliases", []),
                        "species": c.get("species", "HUMAN"),
                        "birth_year": c.get("birth_year", 1950),
                        "death_year": d_year,
                        "status": stat,
                        "stasis_start_year": s_start,
                        "stasis_end_year": s_end,
                        "home_planet": c.get("home_planet", "Earth"),
                        "powers": c.get("powers", ["Custom Ability"])
                    })
                for r in parsed.get("relics", []):
                    r_name = r.get("name", "Relic")
                    dest_yr = r.get("destruction_year") or r.get("destroyed_year") or 2000
                    relationships.append({
                        "relationship_id": str(uuid.uuid4()),
                        "subject_name": "Franchise Order",
                        "predicate": "POSSESSES",
                        "object_name": r_name,
                        "valid_from_year": r.get("valid_from_year", 1900),
                        "valid_to_year": dest_yr,
                        "status": r.get("status", "DESTROYED").upper(),
                        "source_media": "Uploaded Story Bible"
                    })
                for rule in parsed.get("rules", []):
                    stmt = rule.get("rule_statement") or rule.get("rule_text") or rule.get("statement") or str(rule)
                    rules.append({
                        "rule_id": str(uuid.uuid4()),
                        "category": rule.get("category", "PHYSICS"),
                        "entity_or_species": rule.get("entity_or_species", "Uploaded Rule"),
                        "rule_statement": stmt,
                        "canon_tier": "ABSOLUTE"
                    })
        except Exception as ex:
            logger.warning(f"Could not parse JSON bible: {ex}")
            is_json = False

    # 2. If not JSON, parse line-by-line (Markdown, tagged plaintext, or prose)
    if not is_json:
        lines = req.document_content.splitlines()
        for line in lines:
            l = line.strip().lstrip("-*#").strip()
            if not l:
                continue
            if any(l.lower().startswith(p) for p in ["character:", "name:", "hero:", "villain:"]):
                parts = l.split(":", 1)
                raw_name = parts[1].strip()
                name_match = re.match(r'([^(]+)', raw_name)
                c_name = name_match.group(1).strip() if name_match else raw_name
                b_match = re.search(r'born[:\s]+(\d+)', raw_name, re.I)
                d_match = re.search(r'died[:\s]+(\d+)', raw_name, re.I)
                stasis_match = re.search(r'stasis[:\s]+(\d+)\s*-\s*(\d+)', raw_name, re.I)
                b_year = int(b_match.group(1)) if b_match else 1950
                d_year = int(d_match.group(1)) if d_match else None
                s_start = int(stasis_match.group(1)) if stasis_match else None
                s_end = int(stasis_match.group(2)) if stasis_match else None
                status = "STASIS" if s_start else ("DEAD" if d_year else "ALIVE")
                characters.append({
                    "character_id": str(uuid.uuid4()),
                    "name": c_name,
                    "aliases": [],
                    "species": "HUMAN",
                    "birth_year": b_year,
                    "death_year": d_year,
                    "status": status,
                    "stasis_start_year": s_start,
                    "stasis_end_year": s_end,
                    "home_planet": "Earth",
                    "powers": ["Custom Ability"]
                })
            elif any(l.lower().startswith(p) for p in ["relic:", "artifact:", "weapon:", "item:"]):
                parts = l.split(":", 1)
                raw_relic = parts[1].strip()
                r_match = re.match(r'([^(]+)', raw_relic)
                r_name = r_match.group(1).strip() if r_match else raw_relic
                dest_match = re.search(r'(?:destroyed|shattered|melted|lost)(?:\s+in)?[:\s]+(\d+)', raw_relic, re.I)
                dest_year = int(dest_match.group(1)) if dest_match else 2000
                relationships.append({
                    "relationship_id": str(uuid.uuid4()),
                    "subject_name": "Franchise Order",
                    "predicate": "POSSESSES",
                    "object_name": r_name,
                    "valid_from_year": 1900,
                    "valid_to_year": dest_year,
                    "status": "DESTROYED",
                    "source_media": "Uploaded Story Bible"
                })
            elif any(l.lower().startswith(p) for p in ["rule:", "axiom:", "law:"]):
                parts = l.split(":", 1)
                stmt = parts[1].strip()
                rules.append({
                    "rule_id": str(uuid.uuid4()),
                    "category": "PHYSICS",
                    "entity_or_species": "Uploaded Rule",
                    "rule_statement": stmt,
                    "canon_tier": "ABSOLUTE"
                })

        # If document was raw prose without tags, extract capitalized entity names
        if not characters:
            found_names = re.findall(r'\b([A-Z][a-z]+ [A-Z][a-z]+|[A-Z][a-z]{3,})\b', req.document_content)
            unique_names = list(dict.fromkeys(found_names))[:8]
            for name in unique_names:
                characters.append({
                    "character_id": str(uuid.uuid4()),
                    "name": name,
                    "aliases": [],
                    "species": "HUMAN",
                    "birth_year": 1960,
                    "death_year": 2010 if "died" in req.document_content.lower() else None,
                    "status": "DEAD" if "died" in req.document_content.lower() else "ALIVE",
                    "stasis_start_year": None,
                    "stasis_end_year": None,
                    "home_planet": "Earth",
                    "powers": ["Leadership"]
                })

    # Ingest into ClickHouse
    universe_metadata = ch_engine.ingest_custom_universe(
        universe_id=uid,
        name=req.universe_name,
        genre=req.genre or "Custom Lore",
        era=req.era or "Active Era",
        description=req.description or "User-uploaded story bible.",
        characters=characters,
        timeline_events=events,
        relationships=relationships,
        lore_rules=rules
    )

    logger.info(f"Custom universe '{req.universe_name}' ({uid}) ingested into ClickHouse with {len(characters)} characters, {len(relationships)} relics, {len(rules)} rules.")
    return {
        "status": "SUCCESS",
        "universe": universe_metadata,
        "characters_ingested": len(characters),
        "relics_ingested": len(relationships),
        "rules_ingested": len(rules)
    }

class ScriptFilePayload(BaseModel):
    filename: str
    content: str

class IngestFromScreenplaysRequest(BaseModel):
    universe_name: str
    genre: Optional[str] = None
    era: Optional[str] = None
    description: Optional[str] = None
    scripts: List[ScriptFilePayload]

@app.post("/api/universe/ingest-from-screenplays")
def ingest_from_screenplays(req: IngestFromScreenplaysRequest):
    """
    Method B: Uses Gemini AI to analyze a catalog/batch of past screenplays,
    automatically extracts the temporal timeline, characters (lifespans, stasis),
    relics (creation, destruction dates), and hard universe invariants, and seeds
    them directly into ClickHouse as an active Studio Franchise.
    """
    import re
    import uuid

    if not req.scripts:
        raise HTTPException(status_code=400, detail="No screenplay scripts provided.")

    # Prevent duplicate universe names
    existing = ch_engine.find_universe_by_name(req.universe_name)
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"A universe named '{req.universe_name}' already exists (ID: {existing['id']}). Please choose a unique name or delete the existing universe first."
        )

    clean_name = re.sub(r'[^A-Z0-9]', '_', req.universe_name.upper())[:15].strip('_')
    uid = f"CUSTOM_{clean_name}_{str(uuid.uuid4())[:4]}"

    scripts_dicts = [{"filename": s.filename, "content": s.content} for s in req.scripts]
    
    # Run AI Ingestion Agent extraction (Gemini 2.5 Flash + fallback)
    extracted = ingestion_agent.extract_canon_from_screenplay_batch(
        scripts=scripts_dicts,
        franchise_name=req.universe_name,
        user_genre=req.genre,
        user_era=req.era
    )

    characters = []
    for c in extracted.get("characters", []):
        characters.append({
            "character_id": str(uuid.uuid4()),
            "name": c.get("name", "Unknown"),
            "aliases": c.get("aliases", []),
            "species": c.get("species", "HUMAN"),
            "birth_year": c.get("birth_year", 1950),
            "death_year": c.get("death_year"),
            "status": c.get("status", "ALIVE").upper(),
            "stasis_start_year": c.get("stasis_start_year"),
            "stasis_end_year": c.get("stasis_end_year"),
            "home_planet": c.get("home_planet", "Earth"),
            "powers": c.get("powers", ["Extracted Lore Role"])
        })

    relationships = []
    for r in extracted.get("relics", []):
        dest_yr = r.get("destruction_year") or 2000
        relationships.append({
            "relationship_id": str(uuid.uuid4()),
            "subject_name": req.universe_name,
            "predicate": "POSSESSES",
            "object_name": r.get("name", "Relic"),
            "valid_from_year": r.get("valid_from_year", 1900),
            "valid_to_year": dest_yr,
            "status": r.get("status", "DESTROYED").upper(),
            "source_media": f"Screenplay Batch ({len(req.scripts)} scripts)"
        })

    rules = []
    for rule in extracted.get("rules", []):
        stmt = rule.get("rule_statement") or str(rule)
        rules.append({
            "rule_id": str(uuid.uuid4()),
            "category": rule.get("category", "PHYSICS"),
            "entity_or_species": rule.get("entity_or_species", req.universe_name),
            "rule_statement": stmt,
            "canon_tier": "ABSOLUTE"
        })

    events = []
    for ev in extracted.get("timeline_events", []):
        events.append({
            "event_id": str(uuid.uuid4()),
            "title": ev.get("event_summary", "Milestone"),
            "year": ev.get("year", 1982),
            "location": ev.get("location", "Main Base"),
            "canon_tier": "PRIMARY",
            "media_type": "SCRIPT_CATALOG",
            "description": ev.get("event_summary", "")
        })

    universe_metadata = ch_engine.ingest_custom_universe(
        universe_id=uid,
        name=req.universe_name,
        genre=extracted.get("genre") or req.genre or "Sci-Fi / Space Opera",
        era=extracted.get("era") or req.era or "Legacy Timeline",
        description=extracted.get("description") or req.description or f"AI-extracted canon from {len(req.scripts)} screenplay scripts.",
        characters=characters,
        timeline_events=events,
        relationships=relationships,
        lore_rules=rules,
        default_year=extracted.get("default_year", 1982),
        default_location=extracted.get("default_location", "Main Base")
    )

    logger.info(f"Method B: Ingested {len(req.scripts)} screenplays into '{req.universe_name}' ({uid}) via AI: {len(characters)} chars, {len(relationships)} relics, {len(rules)} rules.")
    return {
        "status": "SUCCESS",
        "universe": universe_metadata,
        "characters_ingested": len(characters),
        "relics_ingested": len(relationships),
        "rules_ingested": len(rules),
        "events_ingested": len(events),
        "scripts_processed": len(req.scripts)
    }

class ScreenplayUploadRequest(BaseModel):
    content: str
    filename: Optional[str] = "Screenplay.fountain"

@app.post("/api/screenplay/parse")
def parse_screenplay_upload(req: ScreenplayUploadRequest):
    """
    Parses an uploaded screenplay file (.fountain, .txt),
    extracts slugline, scene year, and location, and runs real-time validation.
    """
    import re
    slug_match = re.search(r'(?:INT\.|EXT\.)[^\n]+', req.content)
    slug = slug_match.group(0).strip() if slug_match else "INT. BERLIN SAFEHOUSE - NIGHT - 1982"
    
    year_match = re.search(r'\b(1\d{3}|2\d{3})\b', slug)
    if not year_match:
        year_match = re.search(r'\b(1\d{3}|2\d{3})\b', req.content)
    scene_year = int(year_match.group(1)) if year_match else 1982

    # Extract location from slugline
    loc = "Main Safehouse"
    if "-" in slug:
        parts = slug.split("-")
        if len(parts) >= 2:
            loc = parts[0].replace("INT.", "").replace("EXT.", "").strip()

    first_action_line = ""
    for line in req.content.splitlines():
        l = line.strip()
        if l and not l.startswith("INT.") and not l.startswith("EXT.") and not l.isupper():
            first_action_line = l
            break
    if not first_action_line:
        first_action_line = req.content.strip()[:200]

    # Validate against current active universe
    val_result = orchestrator.validate_screenplay_stream(
        text=first_action_line,
        screenplay_title=req.filename,
        fallback_year=scene_year,
        fallback_location=loc
    )

    return {
        "filename": req.filename,
        "slugline": slug,
        "scene_year": scene_year,
        "location": loc,
        "content": req.content,
        "preview_line": first_action_line,
        "validation": val_result
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
    chars = [c for c in ch_engine.characters if c.get("universe_id") == ch_engine.active_universe_id]
    if query:
        q = query.lower()
        chars = [c for c in chars if q in c["name"].lower() or any(q in a.lower() for a in c.get("aliases", []))]
    return {"total": len(chars), "universe": ch_engine.active_universe_id, "characters": chars[:50]}

@app.get("/api/lore/timeline")
def get_timeline():
    """Returns canonical timeline events."""
    events = [e for e in ch_engine.timeline_events if e.get("universe_id") == ch_engine.active_universe_id]
    return {"total": len(events), "universe": ch_engine.active_universe_id, "events": events}

@app.get("/api/lore/rules")
def get_lore_rules():
    """Returns absolute physical, biological, and technological lore invariants."""
    rules = [r for r in ch_engine.lore_rules if r.get("universe_id") == ch_engine.active_universe_id]
    return {"total": len(rules), "universe": ch_engine.active_universe_id, "rules": rules}

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
