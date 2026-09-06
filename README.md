# 🛡️ CanonGuard AI: Real-Time Franchise Memory Engine

> **Devpost Hackathon:** [Agentic Cinema: The Blockbuster Hackathon](https://agentic-cinema.devpost.com/)  
> **Target Partner Track:** **ClickHouse Track** ($7,500 1st / $4,500 2nd / $3,000 3rd)  
> **Sub-20ms Target:** Verified inside ClickHouse at **0.6ms – 1.8ms**  
> **Studio Guide & Glossary:** [Read GUIDE.md](GUIDE.md)  
> **Competitive Analysis & Market Study:** [Read COMPETITIVE_ANALYSIS.md](COMPETITIVE_ANALYSIS.md)  
> **Open Source License:** [MIT License](LICENSE)

---

## 🎬 1. The Real-World Entertainment Problem

Modern Hollywood and streaming entertainment are dominated by massive cinematic universes (Marvel MCU, Star Wars, Lord of the Rings, DC, Star Trek) spanning **30 to 80 years of lore**, 50+ movies, hundreds of tie-in novels, and thousands of character arcs. 

When screenwriters write new episodes or feature films, accidental continuity errors (**"retcons"**) routinely slip into scripts:
- **Temporal Paradoxes:** Writing a character into 1982 Berlin when canon established they were in cryogenic stasis in Siberia until 1995.
- **Causal Violations:** Re-introducing legendary weapons or artifacts destroyed 3 seasons ago.
- **Physical / Biological Contradictions:** Characters breathing an alien planet's atmosphere established as toxic ammonia.

### The Massive Financial Cost
When retcons slip through filming into final cuts, fanbases erupt in outrage, and studios are forced into **$10 Million to $30 Million in emergency VFX reshoots and post-production pickup shots**. Today, human "Lore Keepers" take days to search 800-page lore bibles, leaving screenwriters writing blind.

---

## ⚡ 2. The Solution: CanonGuard AI

**CanonGuard AI** is a real-time, **sub-20ms franchise memory engine** powered by **ClickHouse Cloud** and **Gemini 2.0 Flash**. As screenwriters type in the Fountain screenplay editor, the system streams tokens into ClickHouse, verifies character lifespans, relic integrity, and universe axioms, and flags accidental retcons **instantly with red squiggly underlines**—just like Grammarly, but for 40 years of cinematic canon.

---

## 🚀 3. Quickstart (Running the Live Studio)

### 1. Run Standalone with Python (Instant Boot)
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Start the CanonGuard AI Engine & Screenplay Studio
python3 -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8005
```
Open **[http://127.0.0.1:8005](http://127.0.0.1:8005)** in your browser to interact with the live Screenplay Studio!

### 2. Run with Docker Compose (ClickHouse + Backend)
```bash
docker compose up -d
```

### 3. Run Automated Retcon Trap Tests
```bash
python3 -m backend.tests.test_canon_engine
```
Output:
```text
✅ Trap 1 Passed! Verified in 0.73ms (Target < 20ms). Mitigation: Use Disciple Malakor
✅ Trap 2 Passed! Verified in 0.74ms. Relic contradiction caught.
✅ Trap 3 Passed! Verified in 0.61ms. Lethal atmosphere retcon caught.
✅ Valid Canon Line Passed in 0.66ms with zero false positives.
🎉 ALL 4 CANON ENGINE INTEGRATION TESTS PASSED UNDER 20ms!
```

---

## 🎯 4. The 3 Pre-Seeded Demo Traps

Click the buttons in the Studio header to test the traps live:

| Trap | Screenplay Input | Canonical Fact in ClickHouse | Retcon Caught (< 20ms) | Suggested AI Mitigation |
| :--- | :--- | :--- | :---: | :--- |
| **Trap 1: Stasis Paradox** | *"Viktor arrives at the Berlin safehouse in 1982 to meet Elena."* | Viktor was in cryogenic stasis from 1975 to 1995 (*ChronoVerse III*). | ❌ **0.75 ms** | Swap Viktor with his disciple **Malakor** who was active in Berlin in 1982. |
| **Trap 2: Destroyed Relic** | *"Elena pulls the Sunstone from her trenchcoat in Berlin, 1982."* | The Sunstone was atomized in the Solaria core in 1960 (*ChronoVerse II*). | ❌ **0.63 ms** | Reveal the stone is a **forged replica** created by the Syndicate. |
| **Trap 3: Toxic Atmosphere** | *"On Planet Zora, Lord Vane removes his helmet and takes a deep breath of the air."* | Zoran atmosphere is 85% toxic ammonia (*Lore Rule #4*). | ❌ **0.36 ms** | Engage helmet internal rebreather filter; do not expose lung tissue. |

---

## 🏛️ 5. ClickHouse Schema & Performance Architecture

ClickHouse powers the memory layer using `ReplacingMergeTree` and vector similarity:
1. `franchise_characters`: Columnar character status, birth/death bounds, and stasis ranges.
2. `canon_timeline_events`: Temporal timeline events with 768-dim embeddings.
3. `entity_relationships`: Causal triples (`subject`, `predicate`, `object`, `valid_to_year`, `status`).
4. `canon_lore_rules`: Universe physical, biological, and magical axioms.
5. `audit_retcon_logs`: Telemetry tracking caught errors and sub-20ms query timings.

Dual-Mode Architecture: Automatically connects to native ClickHouse via `clickhouse-connect` or uses the embedded high-performance columnar engine when offline, guaranteeing **100% runnability**.

---

## 🤖 6. Multi-Agent Network

- **1. Stream Ingestion Agent:** Debounces keystrokes (350ms) and extracts `(Subject, Action, Object, Location, Year)`.
- **2. ClickHouse Lore Retrieval Agent:** Executes parallel lookups across ClickHouse in `< 18ms`.
- **3. Causal Contradiction Agent:** Evaluates invariants against temporal status and destroyed relics.
- **4. Creative Mitigation Agent:** Delivers 3 drama-preserving rewrites with 1-click Auto-Patching into the script.
