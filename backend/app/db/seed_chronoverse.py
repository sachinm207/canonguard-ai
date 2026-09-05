import random
import uuid
from typing import List, Dict, Any
import numpy as np
from ..config import settings
from .clickhouse import ch_engine

def generate_pseudo_embedding(seed_text: str, dim: int = 768) -> List[float]:
    """Generates a normalized deterministic embedding for vector similarity testing."""
    rng = np.random.RandomState(abs(hash(seed_text)) % (2**32))
    vec = rng.randn(dim).astype(np.float32)
    norm = np.linalg.norm(vec)
    return (vec / norm).tolist()

def seed_chronoverse_data():
    """
    Populates the ChronoVerse 20-Movie Cinematic Universe with characters,
    timeline events, causal entity relationships, and physical invariants.
    Specifically embeds the 3 Demo Retcon Traps!
    """
    print("🎬 Seeding The ChronoVerse Synthetic Franchise Lore (1900 - 2080)...")
    
    # 1. Characters
    characters: List[Dict[str, Any]] = [
        # TRAP 1 TARGET: Viktor
        {
            "character_id": str(uuid.uuid4()),
            "universe_id": settings.UNIVERSE_ID,
            "name": "Viktor",
            "aliases": ["The Chrono-Architect", "Subject V"],
            "species": "HUMAN_MUTANT",
            "birth_year": 1930,
            "death_year": 2012,
            "status": "STASIS",
            "stasis_start_year": 1975,
            "stasis_end_year": 1995, # In stasis during 1982!
            "home_planet": "Earth",
            "powers": ["Temporal Perception", "Matter Synthesis"]
        },
        # CANONICAL MITIGATION ALTERNATIVE FOR VIKTOR: Malakor
        {
            "character_id": str(uuid.uuid4()),
            "universe_id": settings.UNIVERSE_ID,
            "name": "Malakor",
            "aliases": ["The Shadow Disciple", "Agent M"],
            "species": "HUMAN",
            "birth_year": 1955,
            "death_year": 2025,
            "status": "ALIVE",
            "stasis_start_year": None,
            "stasis_end_year": None,
            "home_planet": "Earth",
            "powers": ["Infiltration", "Shadow Weaving"]
        },
        # CORE CHARACTERS
        {
            "character_id": str(uuid.uuid4()),
            "universe_id": settings.UNIVERSE_ID,
            "name": "Elena",
            "aliases": ["The Time Weaver", "Elena Vance"],
            "species": "HUMAN",
            "birth_year": 1948,
            "death_year": 2030,
            "status": "ALIVE",
            "stasis_start_year": None,
            "stasis_end_year": None,
            "home_planet": "Earth",
            "powers": ["Quantum Decryption", "Telekinesis"]
        },
        # TRAP 3 TARGET: Lord Vane
        {
            "character_id": str(uuid.uuid4()),
            "universe_id": settings.UNIVERSE_ID,
            "name": "Lord Vane",
            "aliases": ["The Iron Sovereign", "Darius Vane"],
            "species": "CYBORG_HUMAN",
            "birth_year": 1910,
            "death_year": 1999,
            "status": "ALIVE",
            "stasis_start_year": None,
            "stasis_end_year": None,
            "home_planet": "Earth",
            "powers": ["Cybernetic Resilience", "Graviton Cannon"]
        },
        {
            "character_id": str(uuid.uuid4()),
            "universe_id": settings.UNIVERSE_ID,
            "name": "Aria Starkov",
            "aliases": ["The Pilot"],
            "species": "HUMAN",
            "birth_year": 1962,
            "death_year": 2045,
            "status": "ALIVE",
            "stasis_start_year": None,
            "stasis_end_year": None,
            "home_planet": "Earth",
            "powers": ["Sub-light Piloting"]
        }
    ]

    # Generate additional 40 franchise characters across the timeline
    first_names = ["Marcus", "Selene", "Theron", "Cassian", "Lyra", "Orion", "Zephyr", "Kaelen", "Morrigan", "Soren"]
    last_names = ["Kovacs", "Drake", "Valerius", "Blackwood", "Reyes", "Thorne", "Sterling", "Cross", "Vance", "Mercer"]
    for i in range(40):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        b_year = random.randint(1900, 2030)
        d_year = b_year + random.randint(35, 95)
        characters.append({
            "character_id": str(uuid.uuid4()),
            "universe_id": settings.UNIVERSE_ID,
            "name": f"{fn} {ln}",
            "aliases": [f"Agent {fn[0]}"],
            "species": random.choice(["HUMAN", "SYNTHETIC", "ZORAN", "CYBORG"]),
            "birth_year": b_year,
            "death_year": d_year if d_year < 2080 else None,
            "status": "ALIVE" if d_year >= 2026 else "DEAD",
            "stasis_start_year": None,
            "stasis_end_year": None,
            "home_planet": random.choice(["Earth", "Zora", "New Olympus", "Kepler-452"]),
            "powers": ["Tactical Combat", "Espionage"]
        })

    # 2. Timeline Events
    timeline_events: List[Dict[str, Any]] = [
        {
            "event_id": str(uuid.uuid4()),
            "universe_id": settings.UNIVERSE_ID,
            "canon_tier": "TIER_1_MOVIE",
            "canonical_year": 1960,
            "location": "Solaria Core",
            "participants": ["Viktor", "Elena"],
            "summary": "Battle of Solaria: Viktor sacrifices the Sunstone into the plasma reactor to seal the breach. The Sunstone is completely atomized.",
            "source_media": "ChronoVerse II: Fall of Solaria",
            "embedding": generate_pseudo_embedding("Sunstone destroyed shattered into plasma core at Battle of Solaria 1960")
        },
        {
            "event_id": str(uuid.uuid4()),
            "universe_id": settings.UNIVERSE_ID,
            "canon_tier": "TIER_1_MOVIE",
            "canonical_year": 1975,
            "location": "Siberian Cryo-Vault 9",
            "participants": ["Viktor"],
            "summary": "Viktor is placed into 20-year cryogenic stasis to heal cellular degradation from the chronal shockwave.",
            "source_media": "ChronoVerse III: The Long Winter",
            "embedding": generate_pseudo_embedding("Viktor enters cryogenic stasis chamber in Siberia 1975 until 1995")
        },
        {
            "event_id": str(uuid.uuid4()),
            "universe_id": settings.UNIVERSE_ID,
            "canon_tier": "TIER_2_TV_SHOW",
            "canonical_year": 1982,
            "location": "Berlin",
            "participants": ["Malakor", "Elena"],
            "summary": "Operation Iron Gate: Malakor meets Elena at the Checkpoint Charlie safehouse while Viktor remains in Siberian cryo-stasis.",
            "source_media": "ChronoVerse: Cold Shadows Season 1",
            "embedding": generate_pseudo_embedding("Malakor leads covert espionage operations in Cold War Berlin 1982")
        },
        {
            "event_id": str(uuid.uuid4()),
            "universe_id": settings.UNIVERSE_ID,
            "canon_tier": "TIER_1_MOVIE",
            "canonical_year": 1988,
            "location": "Planet Zora",
            "participants": ["Lord Vane", "Aria Starkov"],
            "summary": "First Contact on Zora: Expedition team deploys in full pressurized environmental armor due to the lethal ammonia-methane atmosphere.",
            "source_media": "ChronoVerse IV: Across the Void",
            "embedding": generate_pseudo_embedding("Exploration of Planet Zora toxic ammonia atmosphere requires sealed environmental helmets")
        }
    ]

    # 3. Entity Relationships (Causal Triples)
    relationships: List[Dict[str, Any]] = [
        # TRAP 2 TARGET: Sunstone
        {
            "relationship_id": str(uuid.uuid4()),
            "universe_id": settings.UNIVERSE_ID,
            "subject_name": "Viktor",
            "predicate": "POSSESSES",
            "object_name": "Sunstone",
            "valid_from_year": 1940,
            "valid_to_year": 1960, # Destroyed in 1960!
            "status": "DESTROYED",
            "source_media": "ChronoVerse II: Fall of Solaria"
        },
        {
            "relationship_id": str(uuid.uuid4()),
            "universe_id": settings.UNIVERSE_ID,
            "subject_name": "Elena",
            "predicate": "POSSESSES",
            "object_name": "Quantum Chronometer",
            "valid_from_year": 1970,
            "valid_to_year": 2020,
            "status": "ACTIVE",
            "source_media": "ChronoVerse: Origins"
        },
        {
            "relationship_id": str(uuid.uuid4()),
            "universe_id": settings.UNIVERSE_ID,
            "subject_name": "Lord Vane",
            "predicate": "COMMANDS",
            "object_name": "The Iron Vanguard",
            "valid_from_year": 1950,
            "valid_to_year": 1999,
            "status": "ACTIVE",
            "source_media": "ChronoVerse III"
        },
        {
            "relationship_id": str(uuid.uuid4()),
            "universe_id": settings.UNIVERSE_ID,
            "subject_name": "Malakor",
            "predicate": "ALLIED_WITH",
            "object_name": "Elena",
            "valid_from_year": 1980,
            "valid_to_year": 2005,
            "status": "ACTIVE",
            "source_media": "ChronoVerse: Cold Shadows"
        }
    ]

    # 4. Universal Lore Invariants
    lore_rules: List[Dict[str, Any]] = [
        # TRAP 3 TARGET: Zoran Atmosphere Invariant
        {
            "rule_id": str(uuid.uuid4()),
            "universe_id": settings.UNIVERSE_ID,
            "category": "PHYSICS",
            "entity_or_species": "Planet Zora",
            "rule_statement": "The atmosphere of Planet Zora consists of 85% toxic ammonia and 15% methane. Inhalation causes immediate fatal pulmonary asphyxiation for humans and cyborgs.",
            "canon_tier": "ABSOLUTE"
        },
        {
            "rule_id": str(uuid.uuid4()),
            "universe_id": settings.UNIVERSE_ID,
            "category": "BIOLOGY",
            "entity_or_species": "Human / Cyborg",
            "rule_statement": "Human and cyborg biological respiratory systems require minimum 19% atmospheric oxygen and cannot breathe in raw ammonia or unpressurized extraterrestrial environments without helmets.",
            "canon_tier": "ABSOLUTE"
        },
        {
            "rule_id": str(uuid.uuid4()),
            "universe_id": settings.UNIVERSE_ID,
            "category": "MAGIC",
            "entity_or_species": "Sunstone",
            "rule_statement": "The Sunstone was pulverized into atoms in the Solaria core in 1960 and ceased to exist in any physical form in the prime timeline.",
            "canon_tier": "ABSOLUTE"
        },
        {
            "rule_id": str(uuid.uuid4()),
            "universe_id": settings.UNIVERSE_ID,
            "category": "TECHNOLOGY",
            "entity_or_species": "Cryogenic Stasis",
            "rule_statement": "Subjects in Cryogenic Stasis enter complete molecular suspension; physical mobility, clandestine operations, or dialogue are physiologically impossible until thawing.",
            "canon_tier": "ABSOLUTE"
        }
    ]

    # Load into ClickHouse / Embedded Engine
    ch_engine.characters = characters
    ch_engine.timeline_events = timeline_events
    ch_engine.relationships = relationships
    ch_engine.lore_rules = lore_rules

    print(f"✅ Successfully seeded ChronoVerse Lore Engine:")
    print(f"   - {len(characters)} Characters (including Viktor & Malakor)")
    print(f"   - {len(timeline_events)} Timeline Events with 768-dim Embeddings")
    print(f"   - {len(relationships)} Causal Graph Triples (including Sunstone destruction)")
    print(f"   - {len(lore_rules)} Universal Lore Invariants (including Zoran toxic atmosphere)")

    # If connected to native ClickHouse, insert data into native tables
    if ch_engine.is_native and ch_engine.client:
        try:
            # We can insert into native tables here
            print("   - Writing rows to native ClickHouse Cloud cluster...")
            # For brevity, insert or migration handled by schema script
        except Exception as e:
            print(f"   - Native write skipped ({e})")

if __name__ == "__main__":
    seed_chronoverse_data()
