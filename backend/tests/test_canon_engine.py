import pytest
from backend.app.db.seed_chronoverse import seed_chronoverse_data
from backend.app.agents.orchestrator import orchestrator

# Ensure data is seeded
seed_chronoverse_data()

def test_trap_1_cryogenic_stasis_violation():
    """
    Trap 1: Screenwriter places Viktor in Berlin in 1982,
    violating his established 1975-1995 cryogenic stasis in Siberia.
    """
    script_line = "Viktor arrives at the Berlin safehouse in 1982 to meet Elena."
    result = orchestrator.validate_screenplay_stream(
        text=script_line,
        screenplay_title="Cold War Requiem",
        fallback_year=1982,
        fallback_location="Berlin"
    )
    
    assert result.status == "RETCON_DETECTED", "Should detect retcon violation"
    assert len(result.violations) >= 1
    v = result.violations[0]
    assert v.category == "TEMPORAL_STATUS"
    assert "Viktor" in v.flagged_phrase
    assert "cryogenic stasis" in v.explanation.lower()
    assert result.query_latency_ms < 20.0, f"Query latency {result.query_latency_ms}ms exceeded 20ms budget!"
    
    # Check mitigation recommendation
    assert len(result.mitigations) >= 1
    assert any("Malakor" in m.title or "Malakor" in m.suggested_rewrite for m in result.mitigations)
    print(f"✅ Trap 1 Passed! Verified in {result.query_latency_ms}ms (Target < 20ms). Mitigation: {result.mitigations[0].title}")

def test_trap_2_destroyed_relic_violation():
    """
    Trap 2: Screenwriter writes Elena possessing the Sunstone in 1982,
    forgetting it was atomized in the Solaria Core in 1960.
    """
    script_line = "Elena activates the Sunstone to illuminate the dark vault in 1982."
    result = orchestrator.validate_screenplay_stream(
        text=script_line,
        screenplay_title="Shadows Over Berlin",
        fallback_year=1982
    )
    
    assert result.status == "RETCON_DETECTED"
    assert any(v.category == "RELIC_DESTRUCTION" for v in result.violations)
    relic_v = next(v for v in result.violations if v.category == "RELIC_DESTRUCTION")
    assert "Sunstone" in relic_v.flagged_phrase
    assert "destroyed in 1960" in relic_v.explanation.lower()
    assert result.query_latency_ms < 20.0
    print(f"✅ Trap 2 Passed! Verified in {result.query_latency_ms}ms. Relic contradiction caught.")

def test_trap_3_biological_invariant_violation():
    """
    Trap 3: Screenwriter has Lord Vane remove his helmet on Planet Zora,
    violating the established rule that Zora's atmosphere is toxic ammonia.
    """
    script_line = "On Planet Zora, Lord Vane removes his helmet and takes a deep breath of the air."
    result = orchestrator.validate_screenplay_stream(
        text=script_line,
        screenplay_title="Chronicles of Zora",
        fallback_year=1988,
        fallback_location="Planet Zora"
    )
    
    assert result.status == "RETCON_DETECTED"
    assert any(v.category == "BIOLOGICAL_INVARIANT" for v in result.violations)
    bio_v = next(v for v in result.violations if v.category == "BIOLOGICAL_INVARIANT")
    assert "ammonia" in bio_v.explanation.lower()
    assert result.query_latency_ms < 20.0
    print(f"✅ Trap 3 Passed! Verified in {result.query_latency_ms}ms. Lethal atmosphere retcon caught.")

def test_valid_canon_line_passes_instantly():
    """
    Valid Line: Screenwriter uses Malakor (who is active in Berlin 1982).
    Should return CANON_OK in < 20ms with no violations.
    """
    script_line = "Malakor steps into the Berlin safehouse and greets Elena in 1982."
    result = orchestrator.validate_screenplay_stream(
        text=script_line,
        screenplay_title="Cold War Requiem",
        fallback_year=1982
    )
    
    assert result.status == "CANON_OK"
    assert len(result.violations) == 0
    assert result.query_latency_ms < 20.0
    print(f"✅ Valid Canon Line Passed in {result.query_latency_ms}ms with zero false positives.")

if __name__ == "__main__":
    test_trap_1_cryogenic_stasis_violation()
    test_trap_2_destroyed_relic_violation()
    test_trap_3_biological_invariant_violation()
    test_valid_canon_line_passes_instantly()
    print("\n🎉 ALL 4 CANON ENGINE INTEGRATION TESTS PASSED UNDER 20ms!")
