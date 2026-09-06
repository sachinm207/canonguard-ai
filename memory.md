# Persistent Memory: CanonGuard AI

> **Project ID:** `P-CINEMA-HACK-1.3`  
> **Target Track:** ClickHouse Partner Track — *Agentic Cinema: The Blockbuster Hackathon*  
> **Current Phase:** Phase 5 (Production Polish, Comprehensive Knowledge Base & Pitch Readiness)

---

## 📌 Brainstorming & Build Progress Tracker

| Phase | Description | Status | Key Artifacts / Notes |
| :--- | :--- | :---: | :--- |
| **Phase 1** | ClickHouse Lore Schema & Vector Search Engine | 🟢 Completed | `ReplacingMergeTree` tables, 768-dim vector embeddings, dual-mode client |
| **Phase 2** | ClickHouse MCP Server Integration | 🟢 Completed | `mcp-clickhouse` client tool definitions & dispatch in `app/mcp/client.py` |
| **Phase 3** | Synthetic Franchise Lore Dataset Generation | 🟢 Completed | 20-movie "ChronoVerse" seed script, 3 test contradiction traps verified |
| **Phase 4** | Web Writing Interface & Real-Time Linting UI | 🟢 Completed | Interactive Fountain editor, red squiggly underlines, mitigation drawer, in-app Guide modal |
| **Phase 5** | Studio Guide, Competitive Analysis & Q&A Knowledge Base | 🟢 Completed | `GUIDE.md`, `COMPETITIVE_ANALYSIS.md`, `KNOWLEDGE_BASE.md`, all tests passing in < 0.3ms |
| **Phase 6** | Multi-Canon Universes, Script Upload & Lore Ingestion | 🟢 Completed | 3 pre-seeded canons (ChronoVerse, Galactic Imperium, Mythos Realm), screenplay upload/drop, custom story bible ingestion dialog, 7/7 tests passing |

---

## 📝 Key Design Decisions & Documentation Log

- **2026-09-05:** Project initiated. Selected ClickHouse Cloud with `ReplacingMergeTree` engine for sub-millisecond timeline lookups and vector cosine similarity.
- **2026-09-05:** Adopted official ClickHouse MCP Server (`mcp-clickhouse`) to standardize LLM-to-database interaction.
- **2026-09-05:** Published comprehensive system architecture specification in `ARCHITECTURE.md`.
- **2026-09-05:** Built Dual-Mode client architecture ensuring 100% runnability out of the box (native ClickHouse Cloud + embedded high-performance columnar engine). All integration tests pass in ~0.3ms (< 20ms budget).
- **2026-09-06:** Added comprehensive Studio Guide & Glossary in `GUIDE.md` and integrated an interactive "📖 Studio Guide & Glossary" modal in `frontend/index.html`.
- **2026-09-06:** Researched 5 existing software categories (Final Draft 13, World Anvil, Filmustage, ScriptE, Sudowrite) and compiled full market study in `COMPETITIVE_ANALYSIS.md`.
- **2026-09-06:** Published `KNOWLEDGE_BASE.md` capturing in-depth analyses on:
  1. Historical definition and industry canon tiers.
  2. Cognitive flow state and mathematical justification for sub-20ms latency.
  3. Data volume, capacity, and cost models for 50+ movies in ClickHouse (only ~25 MB compressed; $0.0006/mo storage, $0.12 one-time embedding cost).
  4. Real-world franchise ingestion workflows vs. real-time active scene drafting.
- **2026-09-06:** Added Multi-Universe partitioning in ClickHouse with 3 pre-seeded canons (ChronoVerse, Galactic Imperium, Mythos Realm). Added screenplay file upload (`.fountain`, `.txt`, `.fdx`) and drag-and-drop. Added custom story bible ingestion dialog supporting JSON/Markdown world bibles. Expanded integration tests to 7/7 passing in < 0.4ms.
- **2026-09-06:** Committed and pushed all source code and documentation to `https://github.com/sachinm207/canonguard-ai.git`.

---

## ❓ Open Questions & Resolved Decisions

1. *Vector Indexing in ClickHouse:* ✅ Resolved. Using ClickHouse built-in vector distance (`cosineDistance()`) on normalized 768-dim float arrays with temporal min-max partition filtering.
2. *Editor Component:* ✅ Resolved. Fountain screenplay workspace with inline visual lint preview and red squiggly underlines.
3. *Debounce Window:* ✅ Resolved. 350ms after user stops typing strikes the ideal balance between keystroke responsiveness and server efficiency.
4. *Franchise Capacity:* ✅ Resolved. ClickHouse easily stores 50+ movies in under 25 MB with sub-millisecond query execution.
5. *Multi-Universe Scalability:* ✅ Resolved. Primary key partitioning on `universe_id` ensures zero cross-contamination and 0-byte scan overhead across distinct franchises.
