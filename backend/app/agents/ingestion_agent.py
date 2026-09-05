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
        year_match = re.search(r'\b(19\d{2}|20\d{2})\b', line)
        scene_year = int(year_match.group(1)) if year_match else fallback_year

        # 2. Extract Location
        location = fallback_location
        if "berlin" in line.lower():
            location = "Berlin"
        elif "zora" in line.lower() or "zoran" in line.lower():
            location = "Planet Zora"
        elif "solaria" in line.lower():
            location = "Solaria Core"
        elif "siberia" in line.lower() or "siberian" in line.lower():
            location = "Siberian Cryo-Vault"

        # 3. Known Franchise Characters Lookup
        known_characters = ["Viktor", "Malakor", "Elena", "Lord Vane", "Aria Starkov", "Marcus Kovacs", "Selene Drake"]
        detected_characters = []
        for char in known_characters:
            if re.search(rf'\b{re.escape(char)}\b', line, re.IGNORECASE):
                detected_characters.append(char)

        # 4. Known Relics / Objects Lookup
        known_relics = ["Sunstone", "Quantum Chronometer", "Aegis Blade", "Chrono-Key", "The Iron Vanguard"]
        detected_objects = []
        for relic in known_relics:
            if re.search(rf'\b{re.escape(relic)}\b', line, re.IGNORECASE):
                detected_objects.append(relic)

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
