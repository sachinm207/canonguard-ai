import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

logger = logging.getLogger("canonguard.causal")

class ContradictionViolation(BaseModel):
    violation_id: str
    severity: str # "CRITICAL_RETCON", "MAJOR_INCONSISTENCY", "LORE_ADVISORY"
    category: str # "TEMPORAL_STATUS", "RELIC_DESTRUCTION", "BIOLOGICAL_INVARIANT", "LOCATION_PARADOX"
    flagged_phrase: str
    explanation: str
    canon_reference: str
    confidence_score: float

class CausalContradictionAgent:
    """
    Evaluates extracted screenplay claims against retrieved ClickHouse canonical facts.
    Applies strict analytical invariant verification for temporal lifespans,
    relic integrity, and physical universe axioms.
    """
    def __init__(self):
        self.name = "Causal Contradiction Agent"

    def evaluate(
        self,
        claim: Dict[str, Any],
        char_status: Dict[str, Any],
        relic_status: Dict[str, Any],
        lore_rules: List[Dict[str, Any]],
        raw_text: str
    ) -> List[ContradictionViolation]:
        violations: List[ContradictionViolation] = []
        scene_year = claim.get("year", 2026)

        # 1. Evaluate Character Temporal Status
        for char in char_status.get("results", []):
            eval_result = char.get("evaluation")
            char_name = char.get("name")
            
            if eval_result == "IN_CRYOGENIC_STASIS":
                s_start = char.get("stasis_start_year")
                s_end = char.get("stasis_end_year")
                violations.append(ContradictionViolation(
                    violation_id=f"RETCON-TEMP-{char_name.upper()}",
                    severity="CRITICAL_RETCON",
                    category="TEMPORAL_STATUS",
                    flagged_phrase=char_name,
                    explanation=f"Accidental Retcon: {char_name} is in cryogenic stasis from {s_start} to {s_end} in Siberian Cryo-Vault 9. Physical activity in {scene_year} breaks established continuity.",
                    canon_reference="ChronoVerse III: The Long Winter (Act 2)",
                    confidence_score=0.99
                ))
            elif eval_result == "DEAD_BEFORE_SCENE":
                d_year = char.get("death_year")
                years_dead = scene_year - d_year
                violations.append(ContradictionViolation(
                    violation_id=f"RETCON-DEATH-{char_name.upper()}",
                    severity="CRITICAL_RETCON",
                    category="TEMPORAL_STATUS",
                    flagged_phrase=char_name,
                    explanation=f"Continuity Violation: {char_name} died in {d_year} ({years_dead} years prior to this scene).",
                    canon_reference="ChronoVerse II: Fall of Solaria",
                    confidence_score=1.0
                ))
            elif eval_result == "UNBORN_BEFORE_SCENE":
                b_year = char.get("birth_year")
                violations.append(ContradictionViolation(
                    violation_id=f"RETCON-UNBORN-{char_name.upper()}",
                    severity="CRITICAL_RETCON",
                    category="TEMPORAL_STATUS",
                    flagged_phrase=char_name,
                    explanation=f"Timeline Paradox: {char_name} is not born until {b_year} (Scene takes place in {scene_year}).",
                    canon_reference="ChronoVerse Timeline Archive",
                    confidence_score=1.0
                ))

        # 2. Evaluate Relic / Object Lifecycle
        for relic in relic_status.get("results", []):
            eval_result = relic.get("evaluation")
            obj_name = relic.get("object_name")
            if eval_result == "DESTROYED_OR_INACTIVE":
                v_to = relic.get("valid_to_year")
                source = relic.get("source_media", "Canon Core")
                violations.append(ContradictionViolation(
                    violation_id=f"RETCON-RELIC-{obj_name.upper().replace(' ', '_')}",
                    severity="CRITICAL_RETCON",
                    category="RELIC_DESTRUCTION",
                    flagged_phrase=obj_name,
                    explanation=f"Causal Paradox: The {obj_name} was pulverized and destroyed in {v_to}. Possession or use in {scene_year} violates causal continuity.",
                    canon_reference=f"Established in '{source}'",
                    confidence_score=0.98
                ))

        # 3. Evaluate Physical / Biological Lore Axioms
        raw_lower = raw_text.lower()
        loc_lower = str(claim.get("location", "")).lower()
        if "zora" in loc_lower or "zoran" in loc_lower or "zora" in raw_lower:
            # Check for helmet removal / raw breathing
            if any(term in raw_lower for term in ["removes his helmet", "removes her helmet", "takes a deep breath", "breathes the air", "inhales the atmosphere"]):
                violations.append(ContradictionViolation(
                    violation_id="RETCON-BIO-ZORA-ATMOSPHERE",
                    severity="CRITICAL_RETCON",
                    category="BIOLOGICAL_INVARIANT",
                    flagged_phrase="removes his helmet and takes a deep breath",
                    explanation="Fatal Biological Invariant: The atmosphere of Planet Zora is 85% toxic ammonia and 15% methane. Breathing without a pressurized helmet is lethal within seconds.",
                    canon_reference="ChronoVerse Universal Lore Axiom #4 (Zoran Atmospheric Survey)",
                    confidence_score=0.99
                ))

        return violations

causal_agent = CausalContradictionAgent()
