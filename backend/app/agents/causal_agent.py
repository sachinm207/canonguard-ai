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
    canon_authority: Optional[str] = "PRIMARY CANON (Tier 1 Invariant)"
    canonical_source: Optional[str] = None
    canonical_excerpt: Optional[str] = None
    canonical_status: Optional[str] = None
    temporal_anchor: Optional[str] = None

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
                planet = char.get("home_planet") or "Cryo-Vault"
                stasis_range = f"from {s_start} to {s_end}" if (s_start and s_end) else (f"sealed in {s_start}" if s_start else "during this era")
                violations.append(ContradictionViolation(
                    violation_id=f"RETCON-TEMP-{char_name.upper()}",
                    severity="CRITICAL_RETCON",
                    category="TEMPORAL_STATUS",
                    flagged_phrase=char_name,
                    explanation=f"Accidental Retcon: {char_name} is in cryogenic stasis {stasis_range} in {planet}. Physical activity in {scene_year} breaks established continuity.",
                    canon_reference=f"{char_name} Canon Dossier",
                    confidence_score=0.99,
                    canon_authority="PRIMARY CANON (Biological / Chronological Invariant)",
                    canonical_source=f"{char_name} Personnel Registry & Cryo-Manifest",
                    canonical_excerpt=f"Continuity Record: {char_name} was placed into suspended animation {stasis_range} at the deep-storage vault on {planet}. Physical presence or activity during this window constitutes a severe causal paradox.",
                    canonical_status=f"IN CRYOGENIC STASIS ({stasis_range})",
                    temporal_anchor=f"{s_start or '?'} – {s_end or '?'}"
                ))
            elif eval_result == "DEAD_BEFORE_SCENE":
                d_year = char.get("death_year")
                if d_year is not None:
                    years_dead = scene_year - d_year
                    exp = f"Continuity Violation: {char_name} died in {d_year} ({years_dead} years prior to this scene)."
                else:
                    exp = f"Continuity Violation: {char_name} is deceased prior to {scene_year}."
                violations.append(ContradictionViolation(
                    violation_id=f"RETCON-DEATH-{char_name.upper()}",
                    severity="CRITICAL_RETCON",
                    category="TEMPORAL_STATUS",
                    flagged_phrase=char_name,
                    explanation=exp,
                    canon_reference="Canon Archive",
                    confidence_score=1.0,
                    canon_authority="PRIMARY CANON (Mortal Invariant)",
                    canonical_source=f"Canon Necrology Archive / {char_name} Record",
                    canonical_excerpt=f"Established Canon: {char_name} died in year {d_year if d_year is not None else 'prior eras'}. Canonical history confirms no survival or resurrection in this timeline.",
                    canonical_status=f"DECEASED in {d_year}" if d_year is not None else "DECEASED",
                    temporal_anchor=f"Deceased {d_year}" if d_year is not None else "Prior Era"
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
                    confidence_score=1.0,
                    canon_authority="PRIMARY CANON (Chronological Invariant)",
                    canonical_source=f"Timeline Chronology / {char_name} Birth Record",
                    canonical_excerpt=f"Timeline Fact: {char_name} was born in {b_year}. Interacting or acting in scene year {scene_year} predates this character's existence.",
                    canonical_status=f"UNBORN until {b_year}",
                    temporal_anchor=f"Birth Year: {b_year}"
                ))

        # 2. Evaluate Relic / Object Lifecycle
        for relic in relic_status.get("results", []):
            eval_result = relic.get("evaluation")
            obj_name = relic.get("object_name")
            if eval_result == "DESTROYED_OR_INACTIVE":
                v_to = relic.get("valid_to_year")
                source = relic.get("source_media", "Canon Core")
                dest_text = f"in {v_to}" if v_to else "prior to this scene"
                violations.append(ContradictionViolation(
                    violation_id=f"RETCON-RELIC-{obj_name.upper().replace(' ', '_')}",
                    severity="CRITICAL_RETCON",
                    category="RELIC_DESTRUCTION",
                    flagged_phrase=obj_name,
                    explanation=f"Causal Paradox: The {obj_name} was pulverized and destroyed {dest_text}. Possession or use in {scene_year} violates causal continuity.",
                    canon_reference=f"Established in '{source}'",
                    confidence_score=0.98,
                    canon_authority="PRIMARY CANON (Physical Artifact Invariant)",
                    canonical_source=source,
                    canonical_excerpt=f"Canonical Screenplay Event: In '{source}', the {obj_name} was completely destroyed {dest_text}. All components were obliterated with no operational remnants surviving.",
                    canonical_status=f"DESTROYED ({dest_text})",
                    temporal_anchor=f"Obliterated {dest_text}"
                ))

        # 3. Evaluate Physical / Biological / Magical Lore Axioms
        raw_lower = raw_text.lower()
        loc_lower = str(claim.get("location", "")).lower()

        # Universe 1: Planet Zora
        if "zora" in loc_lower or "zoran" in loc_lower or "zora" in raw_lower:
            if any(term in raw_lower for term in ["removes his helmet", "removes her helmet", "takes a deep breath", "breathes the air", "inhales the atmosphere"]):
                violations.append(ContradictionViolation(
                    violation_id="RETCON-BIO-ZORA-ATMOSPHERE",
                    severity="CRITICAL_RETCON",
                    category="BIOLOGICAL_INVARIANT",
                    flagged_phrase="removes his helmet and takes a deep breath",
                    explanation="Fatal Biological Invariant: The atmosphere of Planet Zora is 85% toxic ammonia and 15% methane. Breathing without a pressurized helmet is lethal within seconds.",
                    canon_reference="ChronoVerse Universal Lore Axiom #4 (Zoran Atmospheric Survey)",
                    confidence_score=0.99,
                    canon_authority="PRIMARY CANON (Astrophysical & Biochemical Axiom)",
                    canonical_source="ChronoVerse Universal Lore Axiom #4 (Zoran Atmospheric Survey)",
                    canonical_excerpt="Planetary Survey: Planet Zora's ambient atmosphere comprises 85% anhydrous ammonia and 15% volatile methane. Unprotected inhalation causes pulmonary caustic trauma and suffocation within 10-15 seconds.",
                    canonical_status="LETHAL AMMONIA ATMOSPHERE",
                    temporal_anchor="Permanent Planetary Invariant"
                ))

        # Universe 2: Planet Krynn (Galactic Imperium)
        if "krynn" in loc_lower or "krynn" in raw_lower:
            if any(term in raw_lower for term in ["removes his helmet", "without his helmet", "without a helmet", "takes a deep breath", "breathes the air"]):
                violations.append(ContradictionViolation(
                    violation_id="RETCON-BIO-KRYNN-VACUUM",
                    severity="CRITICAL_RETCON",
                    category="BIOLOGICAL_INVARIANT",
                    flagged_phrase="takes a deep breath of the air without his helmet",
                    explanation="Fatal Physical Invariant: Planet Krynn is an airless obsidian rock with 0% atmospheric oxygen and lethal cosmic radiation. Unpressurized exposure causes immediate decompression.",
                    canon_reference="Galactic Imperium Astrogation Code §14 (Krynn Vacuum Hazard)",
                    confidence_score=0.99,
                    canon_authority="PRIMARY CANON (Planetary Environment Axiom)",
                    canonical_source="Galactic Imperium Astrogation Code §14 (Krynn Vacuum Hazard)",
                    canonical_excerpt="Astrogation Warning: Planet Krynn maintains 0.00 bar atmosphere. Biological exposure without active pressurized life support leads to explosive depressurization and catastrophic embolisms.",
                    canonical_status="ZERO-OXYGEN HARD VACUUM",
                    temporal_anchor="Permanent Planetary Invariant"
                ))

        # Universe 3: Iron Wastes of Skar (Mythos Realm)
        if "iron wastes" in loc_lower or "skar" in loc_lower or "iron wastes" in raw_lower:
            if any(term in raw_lower for term in ["silver elf", "elf", "removes his enchanted talisman", "removes her enchanted talisman", "without talisman"]):
                violations.append(ContradictionViolation(
                    violation_id="RETCON-MAGIC-SKAR-WARD",
                    severity="CRITICAL_RETCON",
                    category="MAGICAL_AXIOM",
                    flagged_phrase="removes his enchanted talisman",
                    explanation="Ancient Ward Invariant: The Iron Wastes of Skar are sealed with the Ancient Dragon Ward. Silver Elves entering without an enchanted talisman suffer spontaneous soul combustion.",
                    canon_reference="Mythos Realm High Canon (Tome of Wards, Cap. IX)",
                    confidence_score=0.99,
                    canon_authority="PRIMARY CANON (Magical Invariant & Ancient Wards)",
                    canonical_source="Mythos Realm High Canon (Tome of Wards, Cap. IX)",
                    canonical_excerpt="Tome of Wards: The Ancient Dragon Ward instantly incinerates the mystical life essence of any Silver Elf crossing the Iron Wastes boundary lacking attuned protective talisman.",
                    canonical_status="LETHAL DRAGON WARD ACTIVE",
                    temporal_anchor="First Era through Present"
                ))

        # Dynamic check across custom lore rules
        for rule in lore_rules:
            entity = rule.get("entity_or_species", "").lower()
            stmt = rule.get("rule_statement", "")
            cat = rule.get("category", "LORE_INVARIANT")
            if entity and (entity in raw_lower or entity in loc_lower):
                if any(w in raw_lower for w in ["violates", "removes", "destroys", "burns", "without"]):
                    rule_id = f"RETCON-RULE-{entity[:10].upper().replace(' ', '_')}"
                    if not any(v.violation_id == rule_id for v in violations):
                        violations.append(ContradictionViolation(
                            violation_id=rule_id,
                            severity="CRITICAL_RETCON",
                            category=f"{cat}_INVARIANT",
                            flagged_phrase=entity,
                            explanation=f"Lore Invariant Violation: {stmt}",
                            canon_reference=f"Universal Lore Rule ({cat})",
                            confidence_score=0.95,
                            canon_authority="ESTABLISHED UNIVERSE LORE INVARIANT",
                            canonical_source=rule.get("source_media", "Franchise Story Bible"),
                            canonical_excerpt=stmt,
                            canonical_status=f"ACTIVE INVARIANT ({cat})",
                            temporal_anchor="Universal Timeline"
                        ))

        return violations

causal_agent = CausalContradictionAgent()
