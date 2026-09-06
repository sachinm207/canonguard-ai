# Persistent Memory: CanonGuard AI

> **Project ID:** `P-CINEMA-HACK-1.3`  
> **Target Track:** ClickHouse Track  
> **Current Phase:** Phase 1 (ClickHouse Lore Schema & Vector Search Engine)

---

## 📌 Brainstorming & Build Progress Tracker

| Phase | Description | Status | Key Artifacts / Notes |
| :--- | :--- | :---: | :--- |
| **Phase 1** | ClickHouse Lore Schema & Vector Search Engine | 🟢 Completed | `ReplacingMergeTree` tables, 768-dim vector embeddings, dual-mode client |
| **Phase 2** | ClickHouse MCP Server Integration | 🟢 Completed | `mcp-clickhouse` client tool definitions & dispatch in `app/mcp/client.py` |
| **Phase 3** | Synthetic Franchise Lore Dataset Generation | 🟢 Completed | 20-movie "ChronoVerse" seed script, 3 test contradiction traps verified |
| **Phase 4** | Web Writing Interface & Real-Time Linting UI | 🟢 Completed | Interactive Fountain editor, red squiggly underlines, mitigation drawer |
| **Phase 5** | 48-Hour Hackathon Build Roadmap & 3-Min Demo Pitch | 🟡 In Progress | Live app running at `http://127.0.0.1:8005`, all 4 tests passing in < 1ms |

---

## 📝 Key Design Decisions Log
- **2026-09-05:** Project initiated. Using ClickHouse Cloud with ReplacingMergeTree engine for fast timeline event lookups and vector cosine similarity.
- **2026-09-05:** Adopted official ClickHouse MCP Server to standardize LLM-to-database interaction.
- **2026-09-05:** Published comprehensive system architecture specification in `ARCHITECTURE.md`.
- **2026-09-05:** Implemented hardest components first (ClickHouse DDLs, sub-20ms lore retrieval engine, causal contradiction logic, 3 demo traps).
- **2026-09-05:** Application is 100% runnable out of the box with Dual-Mode architecture (native ClickHouse Cloud + embedded high-performance columnar engine). All 4 integration tests pass in ~0.7ms (< 20ms budget).

---

## ❓ Open Questions & Decisions
1. *Vector Indexing in ClickHouse:* Use ClickHouse built-in vector distance (`cosineDistance()`) or experimental vector index?
2. *Editor Component:* CodeMirror with custom lint gutter vs. TipTap screenplay extension?
3. *Debounce Window:* 400ms after user stops typing or streaming on every completed sentence punctation?
