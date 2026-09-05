# Persistent Memory: CanonGuard AI

> **Project ID:** `P-CINEMA-HACK-1.3`  
> **Target Track:** ClickHouse Track  
> **Current Phase:** Phase 1 (ClickHouse Lore Schema & Vector Search Engine)

---

## 📌 Brainstorming & Build Progress Tracker

| Phase | Description | Status | Key Artifacts / Notes |
| :--- | :--- | :---: | :--- |
| **Phase 1** | ClickHouse Lore Schema & Vector Search Engine | 🟢 Architecture Approved | Schema DDLs & Sub-20ms design documented in `ARCHITECTURE.md` |
| **Phase 2** | ClickHouse MCP Server Integration | ⚪ Next | `mcp-clickhouse` config, parameterized SQL tool definitions |
| **Phase 3** | Synthetic Franchise Lore Dataset Generation | ⚪ Ready | 20-movie "ChronoVerse" seed script, 3 test contradiction traps |
| **Phase 4** | Web Writing Interface & Real-Time Linting UI | ⚪ Ready | Fountain editor, red squiggly underlines, lore drawer |
| **Phase 5** | 48-Hour Hackathon Build Roadmap & 3-Min Demo Pitch | ⚪ Ready | 3-minute pitch script highlighting 18ms latency |

---

## 📝 Key Design Decisions Log
- **2026-09-05:** Project initiated. Using ClickHouse Cloud with ReplacingMergeTree engine for fast timeline event lookups and vector cosine similarity.
- **2026-09-05:** Adopted official ClickHouse MCP Server to standardize LLM-to-database interaction.
- **2026-09-05:** Published comprehensive system architecture specification in `ARCHITECTURE.md` with multi-agent orchestration sequence, ClickHouse DDLs, and 3 demo traps.

---

## ❓ Open Questions & Decisions
1. *Vector Indexing in ClickHouse:* Use ClickHouse built-in vector distance (`cosineDistance()`) or experimental vector index?
2. *Editor Component:* CodeMirror with custom lint gutter vs. TipTap screenplay extension?
3. *Debounce Window:* 400ms after user stops typing or streaming on every completed sentence punctation?
