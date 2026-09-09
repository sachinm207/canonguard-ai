import uuid
import random
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

def seed_all_universes(force_reset: bool = False):
    """
    Seeds multiple distinct franchise universes into ClickHouse:
    1. The ChronoVerse (1900–2080) - Sci-Fi Time Travel & Espionage
    2. Galactic Imperium (2100–3200) - Space Opera & Dreadnought War
    3. Mythos Realm (Age of Legends) - High Fantasy & Ancient Relics
    """
    print("🎬 Seeding All Franchise Canons into CanonGuard Engine...")
    
    # -------------------------------------------------------------
    # UNIVERSE 1: THE CHRONOVERSE (1900-2080)
    # -------------------------------------------------------------
    univ_chrono = {
        "id": "CHRONOVERSE",
        "name": "The ChronoVerse (1900–2080)",
        "genre": "Sci-Fi / Time Travel & Espionage",
        "era": "1900–2080",
        "description": "Cold War espionage, cryogenic stasis vaults, and temporal paradoxes.",
        "default_year": 1982,
        "default_location": "Berlin Safehouse",
        "default_title": "Cold War Requiem.fountain",
        "demo_traps": [
            {
                "id": 1,
                "title": "Trap 1 (Stasis)",
                "year": 1982,
                "location": "Berlin Safehouse",
                "script": "Viktor arrives at the Berlin safehouse in 1982 to meet Elena."
            },
            {
                "id": 2,
                "title": "Trap 2 (Relic)",
                "year": 1982,
                "location": "Berlin Safehouse",
                "script": "Elena pulls the Sunstone from her coat to open the portal in 1982."
            },
            {
                "id": 3,
                "title": "Trap 3 (Bio)",
                "year": 1988,
                "location": "Planet Zora",
                "script": "On Planet Zora, Lord Vane removes his helmet and takes a deep breath of the air."
            }
        ],
        "source_scripts": [
            {
                "filename": "The_Solaria_Core_1960.fountain",
                "title": "Episode 4: The Solaria Core (1960)",
                "content": """Title: THE QUANTUM HORIZON - EPISODE 4: THE SOLARIA CORE
Credit: Written by Screenplay Vault
Author: CanonGuard Archives
Draft date: 1960 A.D.

EXT. SOLARIA CORE REACTOR - NIGHT - 1960

Liquid magma surges through subterranean fissures. Alarm sirens wail in descending minor thirds.

KARA (30) clutches the radiant golden SUNSTONE in both blistered palms at the core precipice.

VIKTOR (30) steps out from the access gantry, arm outstretched.

VIKTOR
Kara! Do not drop the stone! The thermal pressure will atomize the crystal matrix forever!

KARA
The overload cannot be reversed, Viktor! If we do not atomize the stone, the planetary crust will shatter!

Kara drops the Sunstone into the fissure. White-hot plasma engulfs it, reducing the artifact to subatomic vapor.

KARA (CONT'D)
It is gone. Forever."""
            },
            {
                "filename": "Bunker_42_Cryo_Vault_1989.fountain",
                "title": "Episode 7: Cold Protocol 42 (1989)",
                "content": """Title: THE QUANTUM HORIZON - EPISODE 7: COLD PROTOCOL 42
Credit: Written by Screenplay Vault
Author: CanonGuard Archives
Draft date: 1989 A.D.

INT. SIBERIAN RESEARCH BUNKER 42 - CRYOGENIC VAULT - NIGHT - 1989

Frost crystals coat the reinforced plexiglass portals. Sub-zero nitrogen mist rolls across the grating.

VIKTOR (59) climbs into Stasis Pod 04, his temporal mutant engrams pulsing blue.

HEAD SCIENTIST
Cryogenic freezing cycle confirmed. Stasis window locked from 1975 to 1995.

VIKTOR
Make sure the locks hold. If I awaken before 1995, the temporal paradox will collapse our timeline.

The hydraulic seal hisses shut. Nitrogen mist blankets the pod. Viktor's eyes freeze into motionless stasis."""
            },
            {
                "filename": "The_Geneva_Collider_1994.fountain",
                "title": "Episode 9: The Geneva Collapse (1994)",
                "content": """Title: THE QUANTUM HORIZON - EPISODE 9: THE GENEVA COLLAPSE
Credit: Written by Screenplay Vault
Author: CanonGuard Archives
Draft date: 1994 A.D.

INT. GENEVA COLLIDER COMPLEX - LAB THREE - NIGHT - 1994

Sparks shower from the magnetic containment housing. The experimental QUANTUM DRIVE hums with deafening oscillation.

DR. SARAH
The primary harmonic field is rupturing! The Quantum Drive cannot maintain structural stability!

LEAD RESEARCHER
Emergency jettison is unresponsive!

A blinding sphere of cerulean plasma erupts from the casing. The Quantum Drive shatters into billions of glowing subatomic ions, completely disintegrating the containment cradle.

DR. SARAH (CONT'D)
It's vaporized! The Quantum Drive was completely destroyed! Zero recoverable fragments!"""
            }
        ]
    }

    chrono_chars = [
        {
            "character_id": str(uuid.uuid4()),
            "universe_id": "CHRONOVERSE",
            "name": "Viktor",
            "aliases": ["The Chrono-Architect", "Subject V"],
            "species": "HUMAN_MUTANT",
            "birth_year": 1930,
            "death_year": 2012,
            "status": "STASIS",
            "stasis_start_year": 1975,
            "stasis_end_year": 1995,
            "home_planet": "Earth",
            "powers": ["Temporal Perception"]
        },
        {
            "character_id": str(uuid.uuid4()),
            "universe_id": "CHRONOVERSE",
            "name": "Malakor",
            "aliases": ["The Shadow Disciple"],
            "species": "HUMAN",
            "birth_year": 1955,
            "death_year": 2025,
            "status": "ALIVE",
            "stasis_start_year": None,
            "stasis_end_year": None,
            "home_planet": "Earth",
            "powers": ["Infiltration"]
        },
        {
            "character_id": str(uuid.uuid4()),
            "universe_id": "CHRONOVERSE",
            "name": "Elena",
            "aliases": ["The Time Weaver", "Elena Vance"],
            "species": "HUMAN",
            "birth_year": 1948,
            "death_year": 2030,
            "status": "ALIVE",
            "stasis_start_year": None,
            "stasis_end_year": None,
            "home_planet": "Earth",
            "powers": ["Quantum Decryption"]
        },
        {
            "character_id": str(uuid.uuid4()),
            "universe_id": "CHRONOVERSE",
            "name": "Lord Vane",
            "aliases": ["The Iron Sovereign", "Darius Vane"],
            "species": "CYBORG_HUMAN",
            "birth_year": 1910,
            "death_year": 1999,
            "status": "ALIVE",
            "stasis_start_year": None,
            "stasis_end_year": None,
            "home_planet": "Earth",
            "powers": ["Graviton Cannon"]
        },
        {
            "character_id": str(uuid.uuid4()),
            "universe_id": "CHRONOVERSE",
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

    first_names = ["Marcus", "Selene", "Theron", "Cassian", "Lyra", "Orion", "Zephyr", "Kaelen", "Morrigan", "Soren"]
    last_names = ["Kovacs", "Drake", "Valerius", "Blackwood", "Reyes", "Thorne", "Sterling", "Cross", "Vance", "Mercer"]
    for i in range(40):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        b_year = random.randint(1900, 2030)
        d_year = b_year + random.randint(35, 95)
        chrono_chars.append({
            "character_id": str(uuid.uuid4()),
            "universe_id": "CHRONOVERSE",
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

    chrono_events = [
        {
            "event_id": str(uuid.uuid4()),
            "universe_id": "CHRONOVERSE",
            "canon_tier": "TIER_1_MOVIE",
            "canonical_year": 1960,
            "location": "Solaria Core",
            "participants": ["Viktor", "Elena"],
            "summary": "Battle of Solaria: Viktor sacrifices the Sunstone into the plasma reactor. The Sunstone is completely atomized.",
            "source_media": "ChronoVerse II: Fall of Solaria",
            "embedding": generate_pseudo_embedding("Sunstone destroyed shattered into plasma core 1960")
        }
    ]

    chrono_relationships = [
        {
            "relationship_id": str(uuid.uuid4()),
            "universe_id": "CHRONOVERSE",
            "subject_name": "Elena",
            "predicate": "POSSESSES",
            "object_name": "Sunstone",
            "valid_from_year": 1952,
            "valid_to_year": 1960,
            "status": "DESTROYED",
            "source_media": "ChronoVerse II"
        }
    ]

    chrono_rules = [
        {
            "rule_id": str(uuid.uuid4()),
            "universe_id": "CHRONOVERSE",
            "category": "PHYSICS",
            "entity_or_species": "Planet Zora",
            "rule_statement": "The atmosphere of Planet Zora consists of 85% toxic ammonia. Inhalation causes immediate fatal pulmonary asphyxiation for humans and cyborgs.",
            "canon_tier": "ABSOLUTE"
        },
        {
            "rule_id": str(uuid.uuid4()),
            "universe_id": "CHRONOVERSE",
            "category": "BIOLOGY",
            "entity_or_species": "Human / Cyborg",
            "rule_statement": "Human respiratory systems require minimum 19% oxygen and cannot breathe raw ammonia without pressurized helmets.",
            "canon_tier": "ABSOLUTE"
        }
    ]

    # -------------------------------------------------------------
    # UNIVERSE 2: GALACTIC IMPERIUM (2100-3200)
    # -------------------------------------------------------------
    univ_galactic = {
        "id": "GALACTIC_IMPERIUM",
        "name": "Galactic Imperium (2100–3200)",
        "genre": "Space Opera / Galactic War",
        "era": "2100–3200",
        "description": "Star battles, dreadnought fleets, singularity cores, and alien hostile worlds.",
        "default_year": 2190,
        "default_location": "Valos Prime Orbit",
        "default_title": "Siege_of_Valos.fountain",
        "demo_traps": [
            {
                "id": 1,
                "title": "Trap 1 (Fallen Commander)",
                "year": 2190,
                "location": "Valos Prime",
                "script": "Grand Inquisitor Kael lands on Valos Prime in 2190 to rally the armada."
            },
            {
                "id": 2,
                "title": "Trap 2 (Shattered Core)",
                "year": 2190,
                "location": "Flagship Eclipse",
                "script": "Lady Seraphina activates the Kyber Singularity Core to power the dreadnought in 2190."
            },
            {
                "id": 3,
                "title": "Trap 3 (Krynn Vacuum)",
                "year": 2190,
                "location": "Planet Krynn",
                "script": "On Planet Krynn, pilot Jarek steps onto the surface and takes a deep breath of the air without his helmet."
            }
        ],
        "source_scripts": [
            {
                "filename": "Imperial_Armada_Valos_2140.fountain",
                "title": "Chapter 1: The Valos Conquest (2140 A.D.)",
                "content": """Title: GALACTIC IMPERIUM - CHAPTER 1: THE VALOS CONQUEST
Credit: Imperial Archives
Draft date: 2140 A.D.

EXT. VALOS PRIME ORBIT - 2140

Ten thousand dreadnoughts blot out the binary suns.

GRAND INQUISITOR KAEL (32) stands upon the command bridge, overlooking the captured orbital shipyards.

GRAND INQUISITOR KAEL
From this day forth, the Valos shipyards belong solely to the Imperium. Inquisitor rule is absolute across the sector."""
            },
            {
                "filename": "Kyber_Singularity_Meltdown_2175.fountain",
                "title": "Chapter 8: The Singularity Fall (2175 A.D.)",
                "content": """Title: GALACTIC IMPERIUM - CHAPTER 8: THE SINGULARITY FALL
Credit: Imperial Archives
Draft date: 2175 A.D.

INT. IMPERIAL DREADNOUGHT - CORE CHAMBER - 2175

The KYBER SINGULARITY CORE flares uncontrollable violet radiation across the containment catwalks.

LADY SERAPHINA
The singularity is uncontained! It is consuming its own housing!

SERAPHINA
Eject the core into the black hole!

The Kyber Singularity Core collapses inward under gravity shear, vanishing into the event horizon, destroyed permanently in 2175."""
            }
        ]
    }

    galactic_chars = [
        {
            "character_id": str(uuid.uuid4()),
            "universe_id": "GALACTIC_IMPERIUM",
            "name": "Grand Inquisitor Kael",
            "aliases": ["Inquisitor Kael", "Kael"],
            "species": "IMPERIAL_CYBORG",
            "birth_year": 2120,
            "death_year": 2180, # Died 10 years before 2190!
            "status": "DEAD",
            "stasis_start_year": None,
            "stasis_end_year": None,
            "home_planet": "Aethel Prime",
            "powers": ["Singularity Telekinesis"]
        },
        {
            "character_id": str(uuid.uuid4()),
            "universe_id": "GALACTIC_IMPERIUM",
            "name": "Commander Vesh",
            "aliases": ["Vesh", "Fleet Admiral Vesh"],
            "species": "HUMAN",
            "birth_year": 2150,
            "death_year": 2220,
            "status": "ALIVE",
            "stasis_start_year": None,
            "stasis_end_year": None,
            "home_planet": "Valos Minor",
            "powers": ["Armada Tactics"]
        },
        {
            "character_id": str(uuid.uuid4()),
            "universe_id": "GALACTIC_IMPERIUM",
            "name": "Lady Seraphina",
            "aliases": ["Seraphina"],
            "species": "HUMAN",
            "birth_year": 2160,
            "death_year": 2235,
            "status": "ALIVE",
            "stasis_start_year": None,
            "stasis_end_year": None,
            "home_planet": "Corvus VII",
            "powers": ["Singularity Engineering"]
        },
        {
            "character_id": str(uuid.uuid4()),
            "universe_id": "GALACTIC_IMPERIUM",
            "name": "Pilot Jarek",
            "aliases": ["Jarek"],
            "species": "HUMAN",
            "birth_year": 2165,
            "death_year": 2230,
            "status": "ALIVE",
            "stasis_start_year": None,
            "stasis_end_year": None,
            "home_planet": "Terra Nova",
            "powers": ["Starfighter Navigation"]
        }
    ]

    galactic_events = [
        {
            "event_id": str(uuid.uuid4()),
            "universe_id": "GALACTIC_IMPERIUM",
            "canon_tier": "TIER_1_MOVIE",
            "canonical_year": 2150,
            "location": "Orion Nebula",
            "participants": ["Lady Seraphina", "Empress Xylar"],
            "summary": "The Great Nova of 2150: The Kyber Singularity Core overloaded and fractured into subatomic dust to prevent a hyper-void tear.",
            "source_media": "Galactic Imperium: Genesis Episode IV",
            "embedding": generate_pseudo_embedding("Kyber Singularity Core shattered in Great Nova 2150")
        }
    ]

    galactic_relationships = [
        {
            "relationship_id": str(uuid.uuid4()),
            "universe_id": "GALACTIC_IMPERIUM",
            "subject_name": "Lady Seraphina",
            "predicate": "POSSESSES",
            "object_name": "Kyber Singularity Core",
            "valid_from_year": 2130,
            "valid_to_year": 2150,
            "status": "DESTROYED",
            "source_media": "Galactic Imperium Chronicles"
        }
    ]

    galactic_rules = [
        {
            "rule_id": str(uuid.uuid4()),
            "universe_id": "GALACTIC_IMPERIUM",
            "category": "PHYSICS",
            "entity_or_species": "Planet Krynn",
            "rule_statement": "Planet Krynn is a hard-vacuum airless obsidian planet with 0% atmospheric oxygen and severe cosmic radiation. Breathing without a pressurized Class-4 EVA helmet causes instant death.",
            "canon_tier": "ABSOLUTE"
        }
    ]

    # -------------------------------------------------------------
    # UNIVERSE 3: MYTHOS REALM (AGE OF LEGENDS)
    # -------------------------------------------------------------
    univ_mythos = {
        "id": "MYTHOS_REALM",
        "name": "Mythos Realm (Age of Legends)",
        "genre": "High Fantasy / Epic Lore",
        "era": "Year 1000–1600",
        "description": "Ancient elven dynasties, melted legendary blades, and forbidden corrupted wastelands.",
        "default_year": 1480,
        "default_location": "Silver Citadel",
        "default_title": "Song_of_Aethelgard.fountain",
        "demo_traps": [
            {
                "id": 1,
                "title": "Trap 1 (Dead High King)",
                "year": 1480,
                "location": "Silver Citadel",
                "script": "High King Eldor enters the Silver Citadel in Year 1480 to claim the throne."
            },
            {
                "id": 2,
                "title": "Trap 2 (Melted Blade)",
                "year": 1480,
                "location": "Throne Room",
                "script": "Queen Morwen draws the Aethelgard Blade from its scabbard in Year 1480 to challenge the beast."
            },
            {
                "id": 3,
                "title": "Trap 3 (Ward of Skar)",
                "year": 1480,
                "location": "Iron Wastes of Skar",
                "script": "A Silver Elf scout marches into the Iron Wastes of Skar and removes his enchanted talisman."
            }
        ],
        "source_scripts": [
            {
                "filename": "Blood_Ridge_Cataclysm_1285.fountain",
                "title": "Scroll 3: The Blood Ridge Cataclysm (1285 A.D.)",
                "content": """Title: MYTHOS REALM - SCROLL 3: BLOOD RIDGE
Credit: Royal Annals of Eldor
Draft date: 1285 A.D.

EXT. BLOOD RIDGE GORGE - 1285

Dragonfire rains from the dark sky. The AETHELGARD BLADE is struck by ancient wyrmfire, shattering into thousands of molten shards across the volcanic stone.

QUEEN MORWEN
The ancient blade is broken! The steel of Eldor is no more!"""
            }
        ]
    }

    mythos_chars = [
        {
            "character_id": str(uuid.uuid4()),
            "universe_id": "MYTHOS_REALM",
            "name": "High King Eldor",
            "aliases": ["Eldor", "The Sun King"],
            "species": "HUMAN_ROYAL",
            "birth_year": 1380,
            "death_year": 1450, # Died in 1450, 30 years before 1480!
            "status": "DEAD",
            "stasis_start_year": None,
            "stasis_end_year": None,
            "home_planet": "Mythos",
            "powers": ["Solar Magic"]
        },
        {
            "character_id": str(uuid.uuid4()),
            "universe_id": "MYTHOS_REALM",
            "name": "Prince Theron",
            "aliases": ["Theron", "The Dawn Prince"],
            "species": "HUMAN_ROYAL",
            "birth_year": 1430,
            "death_year": 1510,
            "status": "ALIVE",
            "stasis_start_year": None,
            "stasis_end_year": None,
            "home_planet": "Mythos",
            "powers": ["Swordsmanship"]
        },
        {
            "character_id": str(uuid.uuid4()),
            "universe_id": "MYTHOS_REALM",
            "name": "Queen Morwen",
            "aliases": ["Morwen", "The Moon Queen"],
            "species": "ELVEN_NOBLE",
            "birth_year": 1350,
            "death_year": 1550,
            "status": "ALIVE",
            "stasis_start_year": None,
            "stasis_end_year": None,
            "home_planet": "Mythos",
            "powers": ["Lunar Divination"]
        }
    ]

    mythos_events = [
        {
            "event_id": str(uuid.uuid4()),
            "universe_id": "MYTHOS_REALM",
            "canon_tier": "TIER_1_MOVIE",
            "canonical_year": 1300,
            "location": "Mount Solstice",
            "participants": ["High King Eldor"],
            "summary": "The Primordial Forge: The Aethelgard Blade was melted down in the Dragon Caldera in Year 1300.",
            "source_media": "Chronicles of the Silver Throne",
            "embedding": generate_pseudo_embedding("Aethelgard Blade melted in dragon caldera 1300")
        }
    ]

    mythos_relationships = [
        {
            "relationship_id": str(uuid.uuid4()),
            "universe_id": "MYTHOS_REALM",
            "subject_name": "Queen Morwen",
            "predicate": "POSSESSES",
            "object_name": "Aethelgard Blade",
            "valid_from_year": 1200,
            "valid_to_year": 1300,
            "status": "DESTROYED",
            "source_media": "Legend of Eldor"
        }
    ]

    mythos_rules = [
        {
            "rule_id": str(uuid.uuid4()),
            "universe_id": "MYTHOS_REALM",
            "category": "MAGIC",
            "entity_or_species": "Iron Wastes of Skar",
            "rule_statement": "The Iron Wastes of Skar are sealed with the Ancient Ward. Silver Elves cannot enter or remove their enchanted talisman without suffering spontaneous soul combustion and total loss of magic.",
            "canon_tier": "ABSOLUTE"
        }
    ]

    # Register Universes into ClickHouse Engine
    ch_engine.universes = {
        "CHRONOVERSE": univ_chrono,
        "GALACTIC_IMPERIUM": univ_galactic,
        "MYTHOS_REALM": univ_mythos
    }

    # Aggregate and populate
    all_chars = chrono_chars + galactic_chars + mythos_chars
    all_events = chrono_events + galactic_events + mythos_events
    all_rels = chrono_relationships + galactic_relationships + mythos_relationships
    all_rules = chrono_rules + galactic_rules + mythos_rules

    ch_engine.characters = all_chars
    ch_engine.timeline_events = all_events
    ch_engine.relationships = all_rels
    ch_engine.lore_rules = all_rules

    # Re-hydrate any user custom universes stored on disk
    if not force_reset:
        ch_engine._load_custom_universes_from_disk()

    deleted_builtins = getattr(ch_engine, 'deleted_builtins', set())
    archived_universes = getattr(ch_engine, 'archived_universes', {})

    # Ensure sample studio franchises Aethelgard and Hyperion exist if not deleted or archived
    if "CUSTOM_AETHELGARD" not in ch_engine.universes and "CUSTOM_AETHELGARD" not in deleted_builtins and "CUSTOM_AETHELGARD" not in archived_universes:
        import os
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "sample_data"))
        aeth_scripts_dir = os.path.join(base_dir, "example_1_aethelgard", "method_b_scripts")
        aeth_scripts = []
        if os.path.exists(aeth_scripts_dir):
            for f in sorted(os.listdir(aeth_scripts_dir)):
                if f.endswith('.fountain'):
                    try:
                        with open(os.path.join(aeth_scripts_dir, f), 'r', encoding='utf-8') as sf:
                            aeth_scripts.append({'filename': f, 'title': f.replace('.fountain', '').replace('_', ' '), 'content': sf.read()})
                    except Exception:
                        pass
        aeth_doc = ""
        aeth_doc_path = os.path.join(base_dir, "example_1_aethelgard", "method_a_story_bible.md")
        if os.path.exists(aeth_doc_path):
            try:
                with open(aeth_doc_path, 'r', encoding='utf-8') as df:
                    aeth_doc = df.read()
            except Exception:
                pass

        ch_engine.ingest_custom_universe(
            universe_id="CUSTOM_AETHELGARD",
            name="Aethelgard: The Broken Crowns",
            genre="Grimdark Fantasy / High Magic",
            era="1240–1325 (Aethelgard High Annals)",
            description="Feuding royal houses, blood sorcery curses, shattered ancestral blades, and amber stasis tombs.",
            characters=[
                {"name": "High King Valerius IV", "species": "HUMAN", "birth_year": 1242, "death_year": 1298, "status": "DEAD", "stasis_start_year": None, "stasis_end_year": None},
                {"name": "Lady Morwen of House Karst", "species": "HUMAN", "birth_year": 1265, "death_year": 1340, "status": "ALIVE", "stasis_start_year": None, "stasis_end_year": None},
                {"name": "Lord Commander Branok", "species": "HUMAN", "birth_year": 1250, "death_year": 1294, "status": "DEAD", "stasis_start_year": None, "stasis_end_year": None},
                {"name": "Prince Kaelen the Frozen", "species": "HUMAN", "birth_year": 1270, "death_year": None, "status": "STASIS", "stasis_start_year": 1292, "stasis_end_year": 1320},
                {"name": "Seraphina the Blind Prophet", "species": "HUMAN", "birth_year": 1220, "death_year": 1289, "status": "DEAD", "stasis_start_year": None, "stasis_end_year": None},
                {"name": "Grand Inquisitor Malakor", "species": "HUMAN", "birth_year": 1258, "death_year": 1318, "status": "ALIVE", "stasis_start_year": None, "stasis_end_year": None}
            ],
            timeline_events=[],
            relationships=[
                {"subject_name": "High Kings", "predicate": "POSSESSES", "object_name": "Sun-Forged Blade of Eldor", "valid_from_year": 1180, "valid_to_year": 1285, "status": "DESTROYED"},
                {"subject_name": "House Karst", "predicate": "POSSESSES", "object_name": "Crown of the Seven Wyrms", "valid_from_year": 1210, "valid_to_year": 1299, "status": "DESTROYED"},
                {"subject_name": "Lord Branok", "predicate": "POSSESSES", "object_name": "Eye of the Void Orb", "valid_from_year": 1235, "valid_to_year": 1294, "status": "DESTROYED"},
                {"subject_name": "Archon Order", "predicate": "POSSESSES", "object_name": "Amulet of the First Archon", "valid_from_year": 1150, "valid_to_year": 1400, "status": "ACTIVE"}
            ],
            lore_rules=[
                {"category": "MAGIC", "entity_or_species": "Blood Sorcery", "rule_statement": "Any spellcaster channeling raw blood sorcery without an inscribed silver ward ring suffers instantaneous arterial combustion."},
                {"category": "BIOLOGY", "entity_or_species": "Frost Drakes", "rule_statement": "Frost Drakes cannot breathe combustion flame and perish within three minutes if exposed to desert heat exceeding 40 degrees Celsius."},
                {"category": "PHYSICS", "entity_or_species": "Iron Sept Scepter", "rule_statement": "No sovereign bearing the Curse of the Weeping Mark may touch the Iron Sept scepter without disintegrating into obsidian ash."}
            ],
            default_year=1310,
            default_location="Oakhaven Throne Room",
            demo_traps=[],
            source_scripts=aeth_scripts,
            raw_document=aeth_doc
        )

    if "CUSTOM_PROJECT_HYPERION" not in ch_engine.universes and "CUSTOM_PROJECT_HYPERION" not in deleted_builtins and "CUSTOM_PROJECT_HYPERION" not in archived_universes:
        import os
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "sample_data"))
        hyp_scripts_dir = os.path.join(base_dir, "example_2_hyperion", "method_b_scripts")
        hyp_scripts = []
        if os.path.exists(hyp_scripts_dir):
            for f in sorted(os.listdir(hyp_scripts_dir)):
                if f.endswith('.fountain'):
                    try:
                        with open(os.path.join(hyp_scripts_dir, f), 'r', encoding='utf-8') as sf:
                            hyp_scripts.append({'filename': f, 'title': f.replace('.fountain', '').replace('_', ' '), 'content': sf.read()})
                    except Exception:
                        pass
        hyp_doc = ""
        hyp_doc_path = os.path.join(base_dir, "example_2_hyperion", "method_a_story_bible.md")
        if os.path.exists(hyp_doc_path):
            try:
                with open(hyp_doc_path, 'r', encoding='utf-8') as df:
                    hyp_doc = df.read()
            except Exception:
                pass

        ch_engine.ingest_custom_universe(
            universe_id="CUSTOM_PROJECT_HYPERION",
            name="Project Hyperion: 2180",
            genre="Hard Sci-Fi / Cyberpunk",
            era="2140–2195 (Sol Planetary Wars)",
            description="Outer rim orbital war, quantum neural ciphers, dark-matter warp engines, and cryogenic sleeper pods.",
            characters=[
                {"name": "Admiral Teresa Cruz", "species": "HUMAN", "birth_year": 2125, "death_year": 2172, "status": "DEAD", "stasis_start_year": None, "stasis_end_year": None},
                {"name": "Chief Engineer Marcus Vance", "species": "HUMAN", "birth_year": 2138, "death_year": 2205, "status": "ALIVE", "stasis_start_year": None, "stasis_end_year": None},
                {"name": "Special Agent Gabriel Cross", "species": "HUMAN", "birth_year": 2145, "death_year": None, "status": "STASIS", "stasis_start_year": 2165, "stasis_end_year": 2190},
                {"name": "Dr. Aris Thorne", "species": "HUMAN", "birth_year": 2150, "death_year": 2210, "status": "ALIVE", "stasis_start_year": None, "stasis_end_year": None},
                {"name": "Commander David Sterling", "species": "HUMAN", "birth_year": 2130, "death_year": 2168, "status": "DEAD", "stasis_start_year": None, "stasis_end_year": None}
            ],
            timeline_events=[],
            relationships=[
                {"subject_name": "United Sol Fleet", "predicate": "POSSESSES", "object_name": "Hyperion Dark-Matter Drive", "valid_from_year": 2155, "valid_to_year": 2175, "status": "DESTROYED"},
                {"subject_name": "Military Intelligence", "predicate": "POSSESSES", "object_name": "Quantum Neural Cipher", "valid_from_year": 2160, "valid_to_year": 2172, "status": "DESTROYED"},
                {"subject_name": "Rogue Syndicate", "predicate": "POSSESSES", "object_name": "Titanium AI Core Theta", "valid_from_year": 2152, "valid_to_year": 2169, "status": "DESTROYED"},
                {"subject_name": "Sol Marines", "predicate": "POSSESSES", "object_name": "Mark-IV Exosuit Rig", "valid_from_year": 2162, "valid_to_year": 2200, "status": "ACTIVE"}
            ],
            lore_rules=[
                {"category": "PHYSICS", "entity_or_species": "Titan Surface", "rule_statement": "Unpressurized exposure to Titan liquid methane surface causes cellular flash-freezing in less than four seconds without thermal EVA insulation."},
                {"category": "PHYSICS", "entity_or_species": "Hyper-Drive", "rule_statement": "Direct neural interface with unshielded hyper-drives causes permanent cortical synapse meltdown."},
                {"category": "PHYSICS", "entity_or_species": "Demilitarized Arc", "rule_statement": "Armed orbital bombardment vessels are strictly prohibited within the Martian Demilitarized Lunar Arc under the Sol Defense Treaty."}
            ],
            default_year=2182,
            default_location="USC Vanguard",
            demo_traps=[],
            source_scripts=hyp_scripts,
            raw_document=hyp_doc
        )

    # Ensure sample custom universe CyberCity 2099 exists if not deleted or archived
    if "CUSTOM_CYBERCITY_2099" not in ch_engine.universes and "CUSTOM_CYBERCITY_2099" not in deleted_builtins and "CUSTOM_CYBERCITY_2099" not in archived_universes:
        ch_engine.ingest_custom_universe(
            universe_id="CUSTOM_CYBERCITY_2099",
            name="CyberCity 2099",
            genre="Cyberpunk / Dystopian",
            era="2090-2105",
            description="High-tech low-life megacorp war with cybernetic neural engrams.",
            characters=[
                {"name": "Jax Vance", "species": "CYBORG", "birth_year": 2040, "death_year": 2085, "status": "DEAD", "stasis_start_year": None, "stasis_end_year": None},
                {"name": "Nyx Shadow", "species": "HUMAN", "birth_year": 2065, "death_year": 2120, "status": "ALIVE", "stasis_start_year": None, "stasis_end_year": None}
            ],
            timeline_events=[],
            relationships=[
                {"subject_name": "Jax Vance", "predicate": "POSSESSES", "object_name": "Neon Pulse Rifle", "valid_from_year": 2060, "valid_to_year": 2075, "status": "DESTROYED"}
            ],
            lore_rules=[
                {"category": "BIOLOGY", "entity_or_species": "Sector 4", "rule_statement": "Sector 4 is bathed in lethal neurotoxin gas without cybernetic respirators."}
            ],
            default_year=2095
        )

    print(f"✅ Loaded {len(ch_engine.universes)} Franchise Canons into ClickHouse Engine:")
    print(f"   1. {univ_chrono['name']} ({len(chrono_chars)} chars)")
    print(f"   2. {univ_galactic['name']} ({len(galactic_chars)} chars)")
    print(f"   3. {univ_mythos['name']} ({len(mythos_chars)} chars)")
    print(f"   Total memory: {len(all_chars)} characters, {len(all_events)} events, {len(all_rels)} relationships, {len(all_rules)} rules.")
    
    # Sync all seeded canon facts to native ClickHouse tables if connected
    ch_engine.sync_to_native()

if __name__ == "__main__":
    seed_all_universes()
