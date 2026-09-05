import time
import logging
from typing import Dict, Any, List
from pydantic import BaseModel

from .ingestion_agent import ingestion_agent
from .retrieval_agent import retrieval_agent
from .causal_agent import causal_agent, ContradictionViolation
from .mitigation_agent import mitigation_agent, MitigationOption
from ..db.clickhouse import ch_engine

logger = logging.getLogger("canonguard.orchestrator")

class ValidationResponse(BaseModel):
    status: str # "CANON_OK" | "RETCON_DETECTED"
    scene_year: int
    location: str
    query_latency_ms: float
    violations: List[ContradictionViolation]
    mitigations: List[MitigationOption]
    claim_details: Dict[str, Any]

class CanonGuardOrchestrator:
    """
    Master Multi-Agent Orchestrator for CanonGuard AI.
    Executes the 4-agent verification loop under 20ms:
    1. Ingestion Agent: Extracts claim & embedding from screenplay text.
    2. Retrieval Agent: Sub-20ms hybrid query into ClickHouse.
    3. Causal Agent: Analytical invariant & contradiction reasoning.
    4. Mitigation Agent: Generates 3 canon-compliant narrative solutions.
    """
    def __init__(self):
        self.name = "CanonGuard Master Orchestrator"

    def validate_screenplay_stream(
        self,
        text: str,
        screenplay_title: str = "Untitled Script",
        fallback_year: int = 1982,
        fallback_location: str = "Berlin"
    ) -> ValidationResponse:
        overall_start = time.perf_counter()

        # Step 1: Ingestion
        claim = ingestion_agent.parse_screenplay_line(
            text=text,
            fallback_year=fallback_year,
            fallback_location=fallback_location
        )

        # Step 2: ClickHouse Lore Retrieval (< 18ms)
        canon_context = retrieval_agent.retrieve_canon_context(claim)

        # Step 3: Causal Contradiction Evaluation
        violations = causal_agent.evaluate(
            claim=claim,
            char_status=canon_context["character_status"],
            relic_status=canon_context["relic_status"],
            lore_rules=canon_context["lore_rules"],
            raw_text=text
        )

        # Step 4: Creative Mitigation (if contradiction flagged)
        mitigations: List[MitigationOption] = []
        if violations:
            for v in violations:
                m_list = mitigation_agent.generate_mitigations(v, claim, text)
                mitigations.extend(m_list)

        total_latency_ms = (time.perf_counter() - overall_start) * 1000.0

        # Step 5: Log Telemetry to ClickHouse Audit Log
        if violations:
            for v in violations:
                ch_engine.record_audit_log(
                    screenplay_title=screenplay_title,
                    flagged_line=text,
                    violation_type=v.category,
                    mitigation=mitigations[0].title if mitigations else "None",
                    latency_ms=total_latency_ms
                )

        return ValidationResponse(
            status="RETCON_DETECTED" if violations else "CANON_OK",
            scene_year=claim["year"],
            location=claim["location"],
            query_latency_ms=round(canon_context["query_latency_ms"], 2),
            violations=violations,
            mitigations=mitigations,
            claim_details={
                "characters": claim["characters"],
                "objects": claim["objects"],
                "action": claim["action"]
            }
        )

orchestrator = CanonGuardOrchestrator()
