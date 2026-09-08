import re
import logging
from typing import Dict, Any, List, Optional
from ..config import settings
from ..db.seed_chronoverse import generate_pseudo_embedding

logger = logging.getLogger("canonguard.ingestion")

class StreamIngestionAgent:
    """
    Parses screenplay text (Fountain format or raw scene action) to extract:
    - Canonical Year from sluglines or context (e.g. "INT. BERLIN - 1982")
    - Scene Location (e.g. "Berlin", "Planet Zora")
    - Entity Subjects (Characters)
    - Objects / Relics
    - Action Predicates
    - 768-dim query vector for semantic search
    """
    def __init__(self):
        self.name = "Stream Ingestion Agent"
        self.gemini_client = None
        self._init_gemini()

    def _init_gemini(self):
        if settings.GEMINI_API_KEY:
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
                logger.info("Initialized Gemini 2.0 Flash Ingestion Client.")
            except Exception as e:
                logger.warning(f"Could not load Gemini SDK ({e}). Running in deterministic rule-based mode.")

    def parse_screenplay_line(self, text: str, fallback_year: int = 1982, fallback_location: str = "Berlin") -> Dict[str, Any]:
        """
        Extracts semantic claims from an active screenplay line.
        """
        line = text.strip()
        
        # 1. Check for Year in Slugline or text: e.g. "1982", "1960", "2045"
        # 1. Check for Year in Slugline or text: e.g. "1480", "1982", "2190"
        year_match = re.search(r'\b(1\d{3}|2\d{3})\b', line)
        scene_year = int(year_match.group(1)) if year_match else fallback_year

        # 2. Extract Location
        location = fallback_location
        if "berlin" in line.lower():
            location = "Berlin"
        elif "zora" in line.lower() or "zoran" in line.lower():
            location = "Planet Zora"
        elif "krynn" in line.lower():
            location = "Planet Krynn"
        elif "valos" in line.lower():
            location = "Valos Prime"
        elif "solaria" in line.lower():
            location = "Solaria Core"
        elif "siberia" in line.lower() or "siberian" in line.lower():
            location = "Siberian Cryo-Vault"
        elif "silver citadel" in line.lower():
            location = "Silver Citadel"
        elif "iron wastes" in line.lower() or "skar" in line.lower():
            location = "Iron Wastes of Skar"

        # 3. Dynamic Franchise Characters Lookup
        from ..db.clickhouse import ch_engine
        detected_characters = []
        for char in ch_engine.characters:
            if char.get("universe_id") == ch_engine.active_universe_id:
                c_name = char["name"]
                if re.search(rf'\b{re.escape(c_name)}\b', line, re.IGNORECASE):
                    if c_name not in detected_characters:
                        detected_characters.append(c_name)
                for alias in char.get("aliases", []):
                    if re.search(rf'\b{re.escape(alias)}\b', line, re.IGNORECASE):
                        if c_name not in detected_characters:
                            detected_characters.append(c_name)

        # Fallback if no character matched
        if not detected_characters:
            for fallback_c in ["Viktor", "Malakor", "Elena", "Lord Vane", "Grand Inquisitor Kael", "Commander Vesh", "Lady Seraphina", "High King Eldor", "Prince Theron", "Queen Morwen"]:
                if re.search(rf'\b{re.escape(fallback_c)}\b', line, re.IGNORECASE):
                    detected_characters.append(fallback_c)

        # 4. Dynamic Relics / Objects Lookup
        detected_objects = []
        for rel in ch_engine.relationships:
            if rel.get("universe_id") == ch_engine.active_universe_id:
                obj_name = rel.get("object_name", "")
                if obj_name and re.search(rf'\b{re.escape(obj_name)}\b', line, re.IGNORECASE):
                    if obj_name not in detected_objects:
                        detected_objects.append(obj_name)

        if not detected_objects:
            for fallback_r in ["Sunstone", "Kyber Singularity Core", "Aethelgard Blade", "Chrono-Key", "The Iron Vanguard"]:
                if re.search(rf'\b{re.escape(fallback_r)}\b', line, re.IGNORECASE):
                    detected_objects.append(fallback_r)

        # 5. Extract Primary Action / Claim
        action = "interacts"
        if any(w in line.lower() for w in ["pulls", "holds", "takes", "hands", "activates", "uses", "grasps"]):
            action = "POSSESSES_OR_USES"
        elif any(w in line.lower() for w in ["arrives", "enters", "meets", "walks", "stands"]):
            action = "LOCATED_AT"
        elif any(w in line.lower() for w in ["breathes", "inhales", "removes his helmet", "removes her helmet"]):
            action = "RESPIRATORY_EXPOSURE"

        embedding = generate_pseudo_embedding(line)

        return {
            "raw_text": line,
            "year": scene_year,
            "location": location,
            "characters": detected_characters,
            "objects": detected_objects,
            "action": action,
            "embedding": embedding
        }

    def extract_canon_from_screenplay_batch(
        self,
        scripts: List[Dict[str, str]],
        franchise_name: str,
        user_genre: Optional[str] = None,
        user_era: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Uses Google Gemini (with deterministic rule-based fallback) to analyze
        a catalog or batch of past screenplays and extract characters, lifespans,
        stasis states, destroyed relics, timeline events, and universe rules.
        """
        combined_text = ""
        for s in scripts:
            fname = s.get("filename", "Script")
            content = s.get("content", "").strip()
            combined_text += f"\n\n=== SCREENPLAY FILE: {fname} ===\n{content}\n"

        # 1. Attempt Gemini 2.5 Flash Structured Ingestion
        if self.gemini_client:
            try:
                import json
                prompt = f"""
You are a Lead Hollywood Franchise Continuity Supervisor and World-Building Architect.
Analyze the following catalog/batch of past screenplays for the franchise '{franchise_name}'.
Extract the canonical temporal timeline, characters, relics, and universe invariants.

RULES FOR EXTRACTION:
1. CHARACTERS: Detect all key characters mentioned or speaking in the scripts.
   - "name": Character name
   - "species": "HUMAN", "SYNTHETIC", "CYBORG", "ALIEN", etc.
   - "birth_year": Estimated birth year (or null)
   - "death_year": Year they were killed or died in the screenplay events (or null)
   - "stasis_start_year": Year they entered stasis / cryo-sleep / imprisonment (or null)
   - "stasis_end_year": Year their stasis ends or they emerge (or null)
   - "status": "ALIVE", "DEAD", or "STASIS"
   - "powers": list of notable roles/skills (e.g. ["Field Operative", "Recon Specialist"])
   - "home_planet": Planet or origin location (default "Earth")
2. RELICS / WEAPONS / ARTIFACTS: Detect unique technology, artifacts, or objects:
   - "name": Relic or item name
   - "valid_from_year": Year created or first appeared
   - "destruction_year": Year it was destroyed, shattered, melted, or lost (or null if still active)
   - "status": "DESTROYED" if destroyed in any scene, else "ACTIVE"
3. UNIVERSE RULES / INVARIANTS: Hard laws established by the dialogue or action:
   - "category": "PHYSICS", "BIOLOGY", "TECH", or "LAW"
   - "entity_or_species": Subject of the rule
   - "rule_statement": Clear concise statement of the rule (e.g. "Sector 4 atmosphere causes neurotoxic asphyxiation without respirators.")
4. TIMELINE EVENTS: Key historical milestones with year, location, and event_summary.
5. METADATA:
   - "genre": e.g. "{user_genre or 'Sci-Fi / Espionage'}"
   - "era": e.g. "{user_era or '1980–2045'}"
   - "description": 1-2 sentence synopsis of this franchise canon.
   - "default_year": Earliest or central scene year (integer).
   - "default_location": Primary setting.

SCREENPLAY ARCHIVE CONTENT:
{combined_text[:50000]}

Respond ONLY with valid JSON conforming strictly to this format:
{{
  "genre": "...",
  "era": "...",
  "description": "...",
  "default_year": 1982,
  "default_location": "...",
  "characters": [
    {{
      "name": "...",
      "species": "HUMAN",
      "birth_year": 1950,
      "death_year": null,
      "stasis_start_year": null,
      "stasis_end_year": null,
      "status": "ALIVE",
      "powers": ["..."],
      "home_planet": "Earth"
    }}
  ],
  "relics": [
    {{
      "name": "...",
      "valid_from_year": 1900,
      "destruction_year": 1994,
      "status": "DESTROYED"
    }}
  ],
  "rules": [
    {{
      "category": "PHYSICS",
      "entity_or_species": "...",
      "rule_statement": "..."
    }}
  ],
  "timeline_events": [
    {{
      "year": 1982,
      "location": "...",
      "event_summary": "..."
    }}
  ]
}}
"""
                resp = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                raw_out = resp.text.strip()
                if "```json" in raw_out:
                    raw_out = raw_out.split("```json")[1].split("```")[0].strip()
                elif "```" in raw_out:
                    raw_out = raw_out.split("```")[1].split("```")[0].strip()
                parsed = json.loads(raw_out)
                if isinstance(parsed, dict) and "characters" in parsed:
                    logger.info(f"Gemini successfully extracted {len(parsed.get('characters', []))} characters, {len(parsed.get('relics', []))} relics from script batch.")
                    return parsed
            except Exception as e:
                logger.warning(f"Gemini batch extraction error: {e}. Falling back to rule-based extractor.")

        # 2. Deterministic Rule-Based Fallback Extractor
        return self._extract_canon_rulebased(combined_text, franchise_name, user_genre, user_era)

    def _extract_canon_rulebased(
        self,
        text: str,
        franchise_name: str,
        user_genre: Optional[str],
        user_era: Optional[str]
    ) -> Dict[str, Any]:
        """Fast offline rule-based parser that scans sluglines, entity names, and keywords."""
        years = [int(y) for y in re.findall(r'\b(1\d{3}|2\d{3})\b', text)]
        min_year = min(years) if years else 1985
        max_year = max(years) if years else 2025

        # Extract characters from dialogue tags: e.g. "VIKTOR\n" or "SARAH (whispering)\n"
        dialogue_chars = re.findall(r'^[ \t]*([A-Z][A-Z0-9\s]{2,15})(?:\s*\(.*?\))?[ \t]*$', text, re.MULTILINE)
        cleaned_chars = []
        for c in dialogue_chars:
            name = c.strip().title()
            if name.lower() not in ["int", "ext", "night", "day", "cut to", "fade in", "fade out", "continued", "scene"] and name not in cleaned_chars:
                cleaned_chars.append(name)

        if not cleaned_chars:
            cleaned_chars = ["Commander Vance", "Dr. Alistair", "Agent Thorne"]

        characters = []
        for idx, name in enumerate(cleaned_chars[:8]):
            # Check if text mentions death or stasis for this character
            is_dead = bool(re.search(rf'{re.escape(name)}.*?(?:killed|dies|executed|murdered|dead)', text, re.I))
            is_stasis = bool(re.search(rf'{re.escape(name)}.*?(?:stasis|cryo|frozen|suspended)', text, re.I))
            status = "STASIS" if is_stasis else ("DEAD" if is_dead else "ALIVE")
            stasis_start = min_year if is_stasis else None
            stasis_end = max_year if is_stasis else None
            death_yr = max_year if is_dead else None

            characters.append({
                "name": name,
                "species": "HUMAN",
                "birth_year": min_year - 30 + (idx * 2),
                "death_year": death_yr,
                "stasis_start_year": stasis_start,
                "stasis_end_year": stasis_end,
                "status": status,
                "powers": ["Tactical Combat", "Leadership"] if idx == 0 else ["Field Operative"],
                "home_planet": "Earth"
            })

        # Relics detection
        relics = []
        relic_matches = re.findall(r'\b([A-Z][a-z]+ (?:Core|Blade|Key|Device|Beacon|Drive|Gauntlet|Cube|Matrix|Staff|Orb))\b', text)
        for r_name in list(dict.fromkeys(relic_matches))[:4]:
            is_destroyed = bool(re.search(rf'{re.escape(r_name)}.*?(?:destroyed|shattered|broken|obliterated|melted)', text, re.I))
            relics.append({
                "name": r_name,
                "valid_from_year": min_year - 50,
                "destruction_year": max_year if is_destroyed else None,
                "status": "DESTROYED" if is_destroyed else "ACTIVE"
            })

        if not relics:
            relics.append({
                "name": "Neural Data-Cipher",
                "valid_from_year": min_year,
                "destruction_year": max_year,
                "status": "DESTROYED"
            })

        # Rules
        rules = [
            {
                "category": "PHYSICS",
                "entity_or_species": "Temporal Anomaly",
                "rule_statement": f"Physical causality requires sequential observation in the {franchise_name} timeline."
            }
        ]

        # Timeline events from sluglines
        sluglines = re.findall(r'(?:INT\.|EXT\.)\s+([A-Z0-9\s-]+?)(?:\s*-\s*([A-Z\s]+))?(?:\s*-\s*(\d{4}))?', text)
        events = []
        for slug in sluglines[:4]:
            loc = slug[0].strip().title()
            yr = int(slug[2]) if (len(slug) > 2 and slug[2]) else min_year
            events.append({
                "year": yr,
                "location": loc or "Main Base",
                "event_summary": f"Historical sequence at {loc}"
            })

        return {
            "genre": user_genre or "Sci-Fi / Cinematic Lore",
            "era": user_era or f"{min_year}–{max_year}",
            "description": f"Extracted franchise continuity catalog for {franchise_name}.",
            "default_year": min_year,
            "default_location": events[0]["location"] if events else "Command Center",
            "characters": characters,
            "relics": relics,
            "rules": rules,
            "timeline_events": events
        }

ingestion_agent = StreamIngestionAgent()
