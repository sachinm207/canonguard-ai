import pytest
from backend.app.db.seed_chronoverse import seed_chronoverse_data
from backend.app.db.clickhouse import ch_engine
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

def test_galactic_imperium_canon():
    """
    Verify switching to Galactic Imperium universe and catching dead commander retcon.
    """
    from backend.app.db.clickhouse import ch_engine
    ch_engine.switch_universe("GALACTIC_IMPERIUM")
    
    script_line = "Grand Inquisitor Kael lands on Valos Prime in 2190 to rally the armada."
    result = orchestrator.validate_screenplay_stream(
        text=script_line,
        screenplay_title="Siege of Valos",
        fallback_year=2190,
        fallback_location="Valos Prime"
    )
    assert result.status == "RETCON_DETECTED"
    assert any("Kael" in v.flagged_phrase for v in result.violations)
    assert any("Vesh" in m.title or "Vesh" in m.suggested_rewrite for m in result.mitigations)
    print(f"✅ Galactic Imperium Canon Verified in {result.query_latency_ms}ms. Kael death caught, Commander Vesh suggested.")

def test_mythos_realm_canon():
    """
    Verify switching to Mythos Realm universe and catching melted relic retcon.
    """
    from backend.app.db.clickhouse import ch_engine
    ch_engine.switch_universe("MYTHOS_REALM")
    
    script_line = "Queen Morwen draws the Aethelgard Blade in Year 1480 to challenge the beast."
    result = orchestrator.validate_screenplay_stream(
        text=script_line,
        screenplay_title="Song of Aethelgard",
        fallback_year=1480,
        fallback_location="Throne Room"
    )
    assert result.status == "RETCON_DETECTED"
    assert any("Aethelgard" in v.flagged_phrase for v in result.violations)
    assert any("Reforged" in m.title or "Dagger" in m.suggested_rewrite for m in result.mitigations)
    print(f"✅ Mythos Realm Canon Verified in {result.query_latency_ms}ms. Melted Aethelgard Blade caught.")
    
    # Switch back to ChronoVerse
    ch_engine.switch_universe("CHRONOVERSE")

def test_custom_lore_document_ingestion():
    """
    Verify uploading and ingesting a custom Story Bible into ClickHouse.
    """
    from backend.app.db.clickhouse import ch_engine
    custom_bible = """
    # Franchise: CyberCity 2099
    Character: Jax Vance (Born: 2040, Died: 2085)
    Relic: Neon Pulse Rifle (Destroyed in 2075)
    Rule: Sector 4 is bathed in lethal neurotoxin gas without cybernetic filters.
    """
    ch_engine.ingest_custom_universe(
        universe_id="CUSTOM_CYBERCITY",
        name="CyberCity 2099",
        genre="Cyberpunk",
        era="2090-2100",
        description="Dystopian neon city under megacorp siege.",
        characters=[{
            "name": "Jax Vance",
            "species": "CYBORG",
            "birth_year": 2040,
            "death_year": 2085,
            "status": "DEAD",
            "stasis_start_year": None,
            "stasis_end_year": None
        }],
        timeline_events=[],
        relationships=[{
            "subject_name": "Jax",
            "predicate": "POSSESSES",
            "object_name": "Neon Pulse Rifle",
            "valid_from_year": 2060,
            "valid_to_year": 2075,
            "status": "DESTROYED"
        }],
        lore_rules=[{
            "category": "BIOLOGY",
            "entity_or_species": "Sector 4",
            "rule_statement": "Sector 4 is bathed in lethal neurotoxin gas without cybernetic filters."
        }],
        default_year=2095
    )

    res = orchestrator.validate_screenplay_stream(
        text="Jax Vance walks into Sector 4 in 2095 holding the Neon Pulse Rifle.",
        screenplay_title="Neon Shadows",
        fallback_year=2095
    )
    assert res.status == "RETCON_DETECTED"
    print(f"✅ Custom Ingested Lore Document Verified in {res.query_latency_ms}ms. Jax death & Neon Pulse Rifle caught!")
    
    # Restore ChronoVerse
    ch_engine.switch_universe("CHRONOVERSE")

def test_custom_universe_deletion_and_protection():
    """
    Verify deleting custom universes works and core universes are protected.
    """
    from backend.app.db.clickhouse import ch_engine
    
    # 1. Ingest a temporary test universe
    ch_engine.ingest_custom_universe(
        universe_id="CUSTOM_TEMP_UNIVERSE",
        name="Temporary Universe",
        genre="Testing",
        era="2026",
        description="For deletion verification.",
        characters=[{"name": "TempBot", "species": "AI", "birth_year": 2020, "death_year": 2025, "status": "DEAD", "stasis_start_year": None, "stasis_end_year": None}],
        timeline_events=[],
        relationships=[],
        lore_rules=[]
    )
    assert "CUSTOM_TEMP_UNIVERSE" in ch_engine.universes
    assert ch_engine.active_universe_id == "CUSTOM_TEMP_UNIVERSE"

    # 2. Delete custom universe (must succeed)
    deleted = ch_engine.delete_universe("CUSTOM_TEMP_UNIVERSE")
    assert deleted is True
    assert "CUSTOM_TEMP_UNIVERSE" not in ch_engine.universes

    # 3. Can delete any universe (e.g. Galactic Imperium)
    assert ch_engine.delete_universe("GALACTIC_IMPERIUM") is True
    assert "GALACTIC_IMPERIUM" not in ch_engine.universes

    # 4. reset_defaults restores all universes including built-ins and CyberCity 2099
    ch_engine.reset_defaults()
    assert "CHRONOVERSE" in ch_engine.universes
    assert "GALACTIC_IMPERIUM" in ch_engine.universes
    assert "MYTHOS_REALM" in ch_engine.universes
    assert "CUSTOM_CYBERCITY_2099" in ch_engine.universes
    print("✅ Any universe deletion & restore lifecycle verified.")

def test_archive_and_restore_lifecycle():
    """
    Verify archiving a universe moves it to cold storage, preserves its lore details,
    and restoring it rehydrates all characters, rules, and relics back into active ClickHouse memory.
    """
    from backend.app.db.clickhouse import ch_engine

    # Ensure clean state
    ch_engine.reset_defaults()
    assert "CUSTOM_CYBERCITY_2099" in ch_engine.universes
    
    # 1. Archive CyberCity 2099
    success = ch_engine.archive_universe("CUSTOM_CYBERCITY_2099")
    assert success is True
    assert "CUSTOM_CYBERCITY_2099" not in ch_engine.universes

    # 2. Inspect archived universes
    archived_list = ch_engine.get_archived_universes()
    archived_ids = [a["id"] for a in archived_list]
    assert "CUSTOM_CYBERCITY_2099" in archived_ids

    # Find the archived entry and check full lore details
    target_archived = next(a for a in archived_list if a["id"] == "CUSTOM_CYBERCITY_2099")
    assert target_archived["name"] == "CyberCity 2099"
    assert target_archived["characters_count"] >= 2
    assert target_archived["rules_count"] >= 1
    assert any(c["name"] == "Jax Vance" for c in target_archived["characters_full"])

    # 3. Restore back to active memory
    restored = ch_engine.restore_archived_universe("CUSTOM_CYBERCITY_2099")
    assert restored is True
    assert "CUSTOM_CYBERCITY_2099" in ch_engine.universes
    assert ch_engine.active_universe_id == "CUSTOM_CYBERCITY_2099"

    # Verify characters are back in active memory
    active_chars = [c for c in ch_engine.characters if c.get("universe_id") == "CUSTOM_CYBERCITY_2099"]
    assert len(active_chars) >= 2
    assert any(c["name"] == "Jax Vance" for c in active_chars)

    # 4. Verify validation works with restored universe
    from backend.app.agents.orchestrator import orchestrator
    res = orchestrator.validate_screenplay_stream(
        text="Jax Vance walks into Sector 4 in 2095 holding the Neon Pulse Rifle.",
        screenplay_title="Neon Shadows",
        fallback_year=2095
    )
    assert res.status == "RETCON_DETECTED"
    print(f"✅ Archive, Inspect & Restore Lifecycle Verified! Caught retcon in {res.query_latency_ms}ms after restore.")

    # Revert to ChronoVerse
    ch_engine.switch_universe("CHRONOVERSE")

def test_batch_screenplay_ai_ingestion_method_b():
    """
    Method B Test: Verifies batch screenplay AI parsing extracts characters,
    stasis, and destroyed relics to create an active ClickHouse franchise.
    """
    from backend.app.agents.ingestion_agent import ingestion_agent
    scripts = [
        {
            "filename": "Pilot_1982.fountain",
            "content": "INT. ORBITAL LAB - 1982\nCommander Ryan activates the Quantum Core. Dr. Sarah observes."
        },
        {
            "filename": "Finale_1994.fountain",
            "content": "INT. RUINS - 1994\nSarah inspects the rubble. The Quantum Core was destroyed during the explosion. Ryan entered stasis."
        }
    ]
    extracted = ingestion_agent.extract_canon_from_screenplay_batch(
        scripts=scripts,
        franchise_name="Quantum Horizon"
    )
    assert "characters" in extracted
    assert len(extracted["characters"]) >= 1
    assert "relics" in extracted
    assert len(extracted["relics"]) >= 1
    print(f"✅ Method B Batch Screenplay Extraction Verified! Extracted {len(extracted['characters'])} chars, {len(extracted['relics'])} relics.")

def test_universe_script_saving_and_deletion():
    """Verifies that screenplays can be saved and deleted directly from a universe's source_scripts."""
    universe_id = "CHRONOVERSE"
    scripts = ch_engine.save_script_to_universe(
        universe_id=universe_id,
        filename="Chronoverse_Test_Scene.fountain",
        content="INT. BERLIN SAFEHOUSE - NIGHT - 1982\nElena waits in the shadows.",
        title="Chronoverse Test Scene"
    )
    assert any(s["filename"] == "Chronoverse_Test_Scene.fountain" for s in scripts)
    
    # Save an update to the same script
    scripts = ch_engine.save_script_to_universe(
        universe_id=universe_id,
        filename="Chronoverse_Test_Scene.fountain",
        content="INT. BERLIN SAFEHOUSE - NIGHT - 1982\nElena checks her chronograph.",
        title="Chronoverse Test Scene (Revised)"
    )
    matching = next(s for s in scripts if s["filename"] == "Chronoverse_Test_Scene.fountain")
    assert matching["title"] == "Chronoverse Test Scene (Revised)"
    assert "chronograph" in matching["content"]
    
    # Delete script
    scripts = ch_engine.delete_script_from_universe(universe_id, "Chronoverse_Test_Scene.fountain")
    assert not any(s["filename"] == "Chronoverse_Test_Scene.fountain" for s in scripts)
    print("✅ Universe Script Saving and Deletion Verified!")

if __name__ == "__main__":
    test_trap_1_cryogenic_stasis_violation()
    test_trap_2_destroyed_relic_violation()
    test_trap_3_biological_invariant_violation()
    test_valid_canon_line_passes_instantly()
    test_galactic_imperium_canon()
    test_mythos_realm_canon()
    test_custom_lore_document_ingestion()
    test_custom_universe_deletion_and_protection()
    test_archive_and_restore_lifecycle()
    test_batch_screenplay_ai_ingestion_method_b()
    test_universe_script_saving_and_deletion()
    print("\n🎉 ALL 11 MULTI-UNIVERSE, ARCHIVE, METHOD A, METHOD B & SCRIPT MANAGEMENT TESTS PASSED!")
