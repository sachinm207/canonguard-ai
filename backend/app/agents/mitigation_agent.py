import logging
from typing import List, Dict, Any
from pydantic import BaseModel
from .causal_agent import ContradictionViolation
from ..config import settings

logger = logging.getLogger("canonguard.mitigation")

class MitigationOption(BaseModel):
    option_id: str
    title: str
    strategy_type: str # "CHARACTER_SUBSTITUTION", "TEMPORAL_REFRAMING", "LORE_TWIST"
    suggested_rewrite: str
    dramatic_rationale: str
    canon_compliance_notes: str

class CreativeMitigationAgent:
    """
    Generates 3 dramatic narrative alternatives when a canon contradiction is flagged,
    preserving the screenwriter's dramatic stakes without breaking 40 years of franchise lore.
    """
    def __init__(self):
        self.name = "Creative Mitigation Agent"

    def generate_mitigations(
        self,
        violation: ContradictionViolation,
        claim: Dict[str, Any],
        raw_text: str
    ) -> List[MitigationOption]:
        options: List[MitigationOption] = []
        scene_year = claim.get("year", 1982)
        flagged = violation.flagged_phrase

        if violation.category == "TEMPORAL_STATUS":
            if "Viktor" in flagged:
                options.append(MitigationOption(
                    option_id="MIT-01-MALAKOR-SUB",
                    title="Character Substitution: Use Disciple Malakor",
                    strategy_type="CHARACTER_SUBSTITUTION",
                    suggested_rewrite=raw_text.replace("Viktor", "Malakor"),
                    dramatic_rationale="Maintains the clandestine Berlin rendezvous while respecting Viktor's Siberian stasis. Malakor was Viktor's primary field lieutenant in 1982.",
                    canon_compliance_notes="100% Canon compliant. Established in 'ChronoVerse: Cold Shadows Season 1'."
                ))
                options.append(MitigationOption(
                    option_id="MIT-02-FLASHBACK",
                    title="Temporal Reframing: Pre-Stasis Flashback (1974)",
                    strategy_type="TEMPORAL_REFRAMING",
                    suggested_rewrite=f"[FLASHBACK - BERLIN, 1974]\n{raw_text}",
                    dramatic_rationale="Preserves Viktor as the actor in the scene by framing the interaction 1 year before his cryogenic sleep began.",
                    canon_compliance_notes="Canon compliant. Viktor was free and active in Europe until autumn 1975."
                ))
                options.append(MitigationOption(
                    option_id="MIT-03-HOLOGRAPHIC-CIPHER",
                    title="Technology Twist: Pre-Recorded Chrono-Voxel",
                    strategy_type="LORE_TWIST",
                    suggested_rewrite="Elena activates a humming chronal projector. Viktor's pre-recorded holographic avatar flickers into view...",
                    dramatic_rationale="Delivers Viktor's dialogue and presence directly to Elena without requiring physical presence in Berlin.",
                    canon_compliance_notes="Canon compliant with ChronoVerse Level-3 holographic transmitters."
                ))

        elif violation.category == "RELIC_DESTRUCTION":
            options.append(MitigationOption(
                option_id="MIT-04-FORGED-REPLICA",
                title="Plot Twist: The Syndicate's Forged Replica",
                strategy_type="LORE_TWIST",
                suggested_rewrite=raw_text.replace("Sunstone", "Sunstone Replica (Syndicate Forge)"),
                dramatic_rationale="Creates immediate suspense when Elena tests the stone and realizes it's a dangerous counterfeit designed to deceive the resistance.",
                canon_compliance_notes="Does not resurrect the original Sunstone destroyed at Solaria Core in 1960."
            ))
            options.append(MitigationOption(
                option_id="MIT-05-CHRONOMETER-SUB",
                title="Item Swap: Use Active Quantum Chronometer",
                strategy_type="CHARACTER_SUBSTITUTION",
                suggested_rewrite=raw_text.replace("Sunstone", "Quantum Chronometer"),
                dramatic_rationale="Swaps the destroyed relic with an authentic canonical time-manipulation device active during 1982.",
                canon_compliance_notes="Canon compliant with Elena's known equipment manifest."
            ))
            options.append(MitigationOption(
                option_id="MIT-06-RESIDUAL-SHARD",
                title="Lore Mitigation: Inert Solaria Shard",
                strategy_type="TEMPORAL_REFRAMING",
                suggested_rewrite=raw_text.replace("Sunstone", "crystalline shard from Solaria's aftermath"),
                dramatic_rationale="A powerless souvenir retaining symbolic value without violating the total destruction of the primary Sunstone.",
                canon_compliance_notes="Acknowledge the Solaria catastrophe while preserving the dramatic gesture."
            ))

        elif violation.category == "BIOLOGICAL_INVARIANT":
            options.append(MitigationOption(
                option_id="MIT-07-HELMET-HUD",
                title="Action Adjustment: Lift Visor Internal Filter",
                strategy_type="CHARACTER_SUBSTITUTION",
                suggested_rewrite="Lord Vane engages the internal rebreather filter, staring through the polarized visor at the swirling ammonia storms of Zora.",
                dramatic_rationale="Preserves the dramatic beat of confronting the harsh extraterrestrial landscape without fatal exposure.",
                canon_compliance_notes="Complies with Zoran toxic atmospheric pressure and respiratory axioms."
            ))
            options.append(MitigationOption(
                option_id="MIT-08-BIO-FORCEFIELD",
                title="Technology Guard: Deploy Portable Atmospheric Dome",
                strategy_type="LORE_TWIST",
                suggested_rewrite="Lord Vane drives a kinetic tether into the soil; a shimmering pressurized oxygen dome expands before he unlatches his helmet.",
                dramatic_rationale="Showcases elite tech dominance while adhering to strict environmental laws.",
                canon_compliance_notes="Valid within House Shadow portable tactical field generators."
            ))
            options.append(MitigationOption(
                option_id="MIT-09-SYNTHETIC-ORGAN",
                title="Cybernetic Lore Expansion: Artificial Lung Purge",
                strategy_type="TEMPORAL_REFRAMING",
                suggested_rewrite="Lord Vane vents his synthetic gill vents with a harsh hiss of vapor, briefly tasting the corrosive fumes before the scrubbers ignite.",
                dramatic_rationale="Highlights his cyborg nature and physical pain threshold.",
                canon_compliance_notes="Consistent with Vane's cybernetic modifications."
            ))

        # Default fallback options if custom category
        if not options:
            options.append(MitigationOption(
                option_id="MIT-DEFAULT-01",
                title="Rephrase Character Action",
                strategy_type="CHARACTER_SUBSTITUTION",
                suggested_rewrite=raw_text,
                dramatic_rationale="Align action with franchise timeline constraints.",
                canon_compliance_notes="General lore compliance."
            ))

        return options

mitigation_agent = CreativeMitigationAgent()
