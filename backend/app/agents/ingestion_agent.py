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

ingestion_agent = StreamIngestionAgent()
