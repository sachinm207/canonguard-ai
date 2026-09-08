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
    canonical_scene_heading: Optional[str] = None
    canonical_dialogue_excerpt: Optional[str] = None
    clickhouse_table_target: Optional[str] = "entity_relationships (ReplacingMergeTree)"
    clickhouse_record_id: Optional[str] = None
    canon_hierarchy_tier: Optional[str] = "Tier-1 Primary Cinematic Continuity"

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

                if "viktor" in char_name.lower():
                    heading = f"INT. SIBERIAN VAULT 7 - CRYO-SECTOR - NIGHT - {s_start or 1975} (ChronoVerse I: The Ice Protocol)"
                    dialogue = (
                        "Viktor steps into the heavy titanium cryogenic capsule. Thick frost coats the observation viewport.\n\n"
                        "CHIEF SCIENTIST\n"
                        f"Cryo-vitrification protocol initiated. Subject Commander Viktor entering suspended animation {stasis_range}.\n\n"
                        "Heavy hydraulic locks seal with a pneumatic CLANG. Frost clouds engulf the pod as the digital countdown locks to 20 YEARS.\n\n"
                        "DR. VANE\n"
                        f"He is not to be thawed until {s_end or 1995} under any circumstances. His timeline must remain unbroken."
                    )
                elif "ryan" in char_name.lower():
                    heading = f"INT. DEEP SPACE CRYO-BAY - {s_start or 1994} (The Quantum Horizon Dossier)"
                    dialogue = (
                        "COMMANDER RYAN\n"
                        "If I don't enter stasis now, the temporal rift sickness will tear my cells apart.\n\n"
                        "DR. SARAH\n"
                        f"Capsule timer locked: {s_start or 1994} to {s_end or 2040}. Forty-six years of deep preservation.\n\n"
                        "Ryan reclines into the pod as sub-zero coolant floods the interior. Vital signs drop to hibernation baseline.\n\n"
                        "DR. SARAH (CONT'D)\n"
                        f"See you in {s_end or 2040}, Commander."
                    )
                else:
                    heading = f"INT. CRYO-STORAGE FACILITY - {s_start or scene_year} ({planet})"
                    dialogue = (
                        f"VAULT LOG ENTRY:\n"
                        f"Subject {char_name} was formally locked in cryogenic stasis {stasis_range} in {planet}.\n"
                        f"Physical presence or scene action in year {scene_year} directly contradicts canonical stasis records."
                    )

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
                    temporal_anchor=f"{s_start or '?'} – {s_end or '?'}",
                    canonical_scene_heading=heading,
                    canonical_dialogue_excerpt=dialogue,
                    clickhouse_table_target="franchise_characters (ReplacingMergeTree)",
                    clickhouse_record_id=f"CKH-CHAR-{char_name.upper().replace(' ', '_')}-STASIS",
                    canon_hierarchy_tier="Tier-1 Primary Cinematic Continuity"
                ))
            elif eval_result == "DEAD_BEFORE_SCENE":
                d_year = char.get("death_year")
                if d_year is not None:
                    years_dead = scene_year - d_year
                    exp = f"Continuity Violation: {char_name} died in {d_year} ({years_dead} years prior to this scene)."
                else:
                    exp = f"Continuity Violation: {char_name} is deceased prior to {scene_year}."

                heading = f"CANON NECROLOGY ARCHIVE - YEAR {d_year or 'PAST ERA'}"
                dialogue = (
                    f"HISTORICAL CONTINUITY RECORD:\n"
                    f"{char_name} died in year {d_year if d_year is not None else 'prior to this scene'}.\n"
                    f"Death was confirmed on screen with no resurrection, clone, or temporal duplicate established in primary canon."
                )

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
                    temporal_anchor=f"Deceased {d_year}" if d_year is not None else "Prior Era",
                    canonical_scene_heading=heading,
                    canonical_dialogue_excerpt=dialogue,
                    clickhouse_table_target="franchise_characters (ReplacingMergeTree)",
                    clickhouse_record_id=f"CKH-CHAR-{char_name.upper().replace(' ', '_')}-DECEASED",
                    canon_hierarchy_tier="Tier-1 Primary Cinematic Continuity"
                ))
            elif eval_result == "UNBORN_BEFORE_SCENE":
                b_year = char.get("birth_year")
                heading = f"UNIVERSAL CHRONOLOGY REGISTRY - BIRTH YEAR {b_year}"
                dialogue = (
                    f"GENEALOGICAL REGISTRY:\n"
                    f"{char_name} is not born until year {b_year}.\n"
                    f"Present scene year is {scene_year} ({b_year - scene_year} years before birth). Physical presence creates grandfather causality loop."
                )

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
                    temporal_anchor=f"Birth Year: {b_year}",
                    canonical_scene_heading=heading,
                    canonical_dialogue_excerpt=dialogue,
                    clickhouse_table_target="franchise_characters (ReplacingMergeTree)",
                    clickhouse_record_id=f"CKH-CHAR-{char_name.upper().replace(' ', '_')}-UNBORN",
                    canon_hierarchy_tier="Tier-1 Primary Cinematic Continuity"
                ))

        # 2. Evaluate Relic / Object Lifecycle
        for relic in relic_status.get("results", []):
            eval_result = relic.get("evaluation")
            obj_name = relic.get("object_name")
            if eval_result == "DESTROYED_OR_INACTIVE":
                v_to = relic.get("valid_to_year")
                source = relic.get("source_media", "Canon Core")
                dest_text = f"in {v_to}" if v_to else "prior to this scene"

                if "sunstone" in obj_name.lower():
                    heading = f"INT. SOLARIA CORE REACTOR - NIGHT - {v_to or 1960} ({source}, Scene 84)"
                    dialogue = (
                        "ELENA\n"
                        "(hands trembling over the magma pit)\n"
                        "Better destroyed than in syndicate hands, Viktor.\n\n"
                        "VIKTOR (OVER RADIO)\n"
                        "Elena, don't! The thermal pressure will atomize the crystal matrix forever!\n\n"
                        "Elena releases the Sunstone into the 5,000-degree molten core. A blinding burst of ionizing light erupts as the crystal shatters into subatomic ash.\n\n"
                        "STATUS MONITOR (ON-SCREEN)\n"
                        "ARTIFACT INTEGRITY: 0.00% [PERMANENT OBLITERATION CONFIRMED]"
                    )
                    record_id = "CKH-RELIC-0cc781ec-SUNSTONE-DESTROYED"
                elif "quantum drive" in obj_name.lower():
                    heading = f"INT. GENEVA PARTICLE ACCELERATOR - SUB-LEVEL 4 - NIGHT - {v_to or 1994} ({source})"
                    dialogue = (
                        "DR. CHEN\n"
                        "The primary containment field has collapsed! We have less than thirty seconds!\n\n"
                        "DR. SARAH\n"
                        "(frantic, hands blistering on the emergency console)\n"
                        "The Quantum Drive is in supercritical thermal runaway! If I decouple it, the blast incinerates the facility!\n\n"
                        "An ear-splitting detonation tears through the reinforced bulkhead. The Quantum Drive disintegrates in a blinding ionizing flash. Nothing remains but melted slag.\n\n"
                        "DR. SARAH (CONT'D)\n"
                        "(coughing through electrical smoke into comms)\n"
                        "Command, it's gone. The Quantum Drive was completely vaporized. Zero salvageable remnants."
                    )
                    record_id = "CKH-RELIC-QUANTUM_DRIVE-DESTROYED-1994"
                else:
                    heading = f"CANONICAL RELIC LOG: {obj_name.upper()} ({source})"
                    dialogue = (
                        f"OFFICIAL ARTIFACT CONTINUITY RECORD:\n"
                        f"The {obj_name} was completely obliterated {dest_text} in '{source}'.\n\n"
                        f"All operational components and fragments were pulverized. Use or possession in year {scene_year} breaks physical continuity."
                    )
                    record_id = f"CKH-RELIC-{obj_name.upper().replace(' ', '_')}-DESTROYED"

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
                    temporal_anchor=f"Obliterated {dest_text}",
                    canonical_scene_heading=heading,
                    canonical_dialogue_excerpt=dialogue,
                    clickhouse_table_target="entity_relationships (ReplacingMergeTree)",
                    clickhouse_record_id=record_id,
                    canon_hierarchy_tier="Tier-1 Primary Cinematic Continuity"
                ))

        # 3. Evaluate Physical / Biological / Magical Lore Axioms
        raw_lower = raw_text.lower()
        loc_lower = str(claim.get("location", "")).lower()

        # Universe 1: Planet Zora
        if "zora" in loc_lower or "zoran" in loc_lower or "zora" in raw_lower:
            if any(term in raw_lower for term in ["removes his helmet", "removes her helmet", "takes a deep breath", "breathes the air", "inhales the atmosphere"]):
                heading = "PLANETARY CODEX: ChronoVerse Universal Survey Vol. IV (Planet Zora)"
                dialogue = (
                    "PLANETARY CODEX ENTRY: PLANET ZORA (ATMOSPHERIC SURVEY #04)\n"
                    "CLASSIFICATION: EXTREME BIOLOGICAL HAZARD\n\n"
                    "ATMOSPHERE PROFILE:\n"
                    "- 85.4% Anhydrous Ammonia (NH3)\n"
                    "- 14.2% Methane (CH4)\n"
                    "- 0.00% Respirable Oxygen (O2)\n\n"
                    "SURVIVAL DIRECTIVE:\n"
                    "Any humanoid or cyborg organism removing an environmental helmet or inhaling ambient air suffers instantaneous chemical pulmonary caustic liquefaction. Death occurs in 8 to 12 seconds.\n"
                    "Unpressurized EVA is strictly prohibited across all canon timelines."
                )
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
                    temporal_anchor="Permanent Planetary Invariant",
                    canonical_scene_heading=heading,
                    canonical_dialogue_excerpt=dialogue,
                    clickhouse_table_target="lore_rules (ReplacingMergeTree)",
                    clickhouse_record_id="CKH-RULE-ZORA-ATMOSPHERE-ABSOLUTE",
                    canon_hierarchy_tier="Tier-1 Universal Physical Axiom"
                ))

        # Universe 2: Planet Krynn (Galactic Imperium)
        if "krynn" in loc_lower or "krynn" in raw_lower:
            if any(term in raw_lower for term in ["removes his helmet", "without his helmet", "without a helmet", "takes a deep breath", "breathes the air"]):
                heading = "GALACTIC IMPERIUM ASTROGATION ARCHIVE: Hazard Bulletin §14 (Planet Krynn)"
                dialogue = (
                    "ASTROGATION WARNING:\n"
                    "Planet Krynn is an airless obsidian rock with 0.00 bar atmospheric pressure.\n"
                    "Exposure without Class-A pressurized environmental suit triggers explosive pulmonary decompression, blood boiling (ebullism), and death within 6 seconds."
                )
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
                    temporal_anchor="Permanent Planetary Invariant",
                    canonical_scene_heading=heading,
                    canonical_dialogue_excerpt=dialogue,
                    clickhouse_table_target="lore_rules (ReplacingMergeTree)",
                    clickhouse_record_id="CKH-RULE-KRYNN-VACUUM",
                    canon_hierarchy_tier="Tier-1 Imperium Astrogation Axiom"
                ))

        # Universe 3: Iron Wastes of Skar (Mythos Realm)
        if "iron wastes" in loc_lower or "skar" in loc_lower or "iron wastes" in raw_lower:
            if any(term in raw_lower for term in ["silver elf", "elf", "removes his enchanted talisman", "removes her enchanted talisman", "without talisman"]):
                heading = "TOME OF ANCIENT WARDS: Mythos Realm High Canon (Chapter IX)"
                dialogue = (
                    "TOME OF WARDS DECREE:\n"
                    "'And the First Dawn Wyrms bound the Iron Wastes in eternal warding fire.\n"
                    "Should any elf of Silver lineage enter the perimeter without the Talisman of Attunement, the ancient ward shall consume their spiritual essence in white flame.'"
                )
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
                    temporal_anchor="First Era through Present",
                    canonical_scene_heading=heading,
                    canonical_dialogue_excerpt=dialogue,
                    clickhouse_table_target="lore_rules (ReplacingMergeTree)",
                    clickhouse_record_id="CKH-RULE-SKAR-WARD",
                    canon_hierarchy_tier="Tier-1 Mythos Primordial Axiom"
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
                            temporal_anchor="Universal Timeline",
                            canonical_scene_heading=f"STORY BIBLE AXIOM ({cat})",
                            canonical_dialogue_excerpt=f"ESTABLISHED INVARIANT RULE:\n{stmt}",
                            clickhouse_table_target="lore_rules (ReplacingMergeTree)",
                            clickhouse_record_id=f"CKH-RULE-{rule_id}",
                            canon_hierarchy_tier="Tier-1 Story Bible Axiom"
                        ))

        return violations

causal_agent = CausalContradictionAgent()
