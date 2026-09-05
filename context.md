# Project Context: CanonGuard AI (`P-CINEMA-HACK-1.3`)

> **Challenge:** [Devpost Agentic Cinema: The Blockbuster Hackathon](https://agentic-cinema.devpost.com/)  
> **Official Resources:** [https://agentic-cinema.devpost.com/resources](https://agentic-cinema.devpost.com/resources)  
> **Official Rules:** [https://agentic-cinema.devpost.com/rules](https://agentic-cinema.devpost.com/rules)  
> **Submission Deadline:** **September 9, 2026 @ 2:00 PM PDT**  
> **Target Partner Track:** **ClickHouse Track** ($7,500 1st / $4,500 2nd / $3,000 3rd)  
> **Portfolio Parent Context:** [`../context.md`](file:///home/sachinm/development/agentic-cinema-devpost/context.md) | Master Memory: [`../memory.md`](file:///home/sachinm/development/agentic-cinema-devpost/memory.md)

---

## 🏆 Devpost Hackathon Master Context & Requirements

### The Core Challenge
Build a functional, production-ready AI agent or multi-agent network—powered by **Gemini and Google Cloud Agent Builder / Vertex AI / Python GenAI SDK**—that integrates a Partner Entity's product or MCP server to solve critical bottlenecks across the entertainment and media value chain.

### Mandatory Devpost Submission Checklist
1. **Hosted Application URL:** A working, live-hosted project that judges can access and test.
2. **The 3-Minute Trailer (Demo Video):**
   - Public YouTube or Vimeo video (under 3 minutes).
   - Demonstrates the live functioning agent as built (actual product workflow).
   - English audio or English subtitles.
3. **Open-Source Code Repository:**
   - Public GitHub, GitLab, or Bitbucket repository.
   - **Crucial Rule:** Must demonstrate **actual runtime use** of Google Cloud (Gemini / ADK) AND ClickHouse Cloud / `mcp-clickhouse` (imported and executed in code, not just named in README).
   - Must include an OSI-approved open-source license file visible at the top of the repository.
4. **Devpost Track Selection:** Select **ClickHouse Track** on the submission form.

### Official Judging Criteria (Equal Weight)
- **Technological Implementation:** How well is the project built, and how effectively does it use Google Cloud and ClickHouse as part of the solution?
- **Design:** Does the project deliver a complete, coherent product experience—not just a technical proof of concept?
- **Potential Impact:** Does the project solve a real problem for a real audience with credible cost/time savings?
- **Quality of the Idea:** Creative, non-obvious use of Google Cloud and Partner services with genuine understanding of the entertainment problem space.

---

## 🎬 1. The Core Vision & Film Industry Problem
- **User Persona:** Showrunners, Head Screenwriters, Story Editors, Franchise Executives at major studios (Disney/Marvel, Warner Bros/DC, Lucasfilm, Netflix, Amazon MGM).
- **The Real-World Film Problem:** Modern entertainment is dominated by massive cinematic universes spanning **30 to 80 years of lore**, 50+ movies, hundreds of comic books, and thousands of character biographies. Screenwriters working on a new episode or movie routinely introduce accidental continuity errors and timeline contradictions (**"retcons"**):
  - *Example 1 (Timeline Paradox):* A scene where Character A meets Character B in Berlin in 1982, forgetting that in a spin-off comic 15 years ago, Character B was in cryogenic stasis in Siberia until 1995.
  - *Example 2 (Causal Violation):* A character suddenly uses a magical weapon destroyed in Season 2 Episode 4.
  - *Example 3 (Relationship / Lore Contradiction):* An alien species breathes oxygen when canon states their atmosphere is toxic nitrogen.
- **The Massive Financial Risk:** When a continuity violation slips through to the final film, it enrages fanbases, damages franchise credibility, and often requires **$10 Million to $30 Million in emergency VFX reshoots** in post-production. Today, studios employ human "Lore Keepers" who manually search 800-page lore bibles, taking days per draft.
- **The Solution:** **CanonGuard AI** is a real-time, sub-20ms franchise memory engine powered by **ClickHouse Cloud**. As a screenwriter types dialogue or action in an online screenplay editor, the system streams tokens into ClickHouse, queries millions of historical lore facts and causal dependencies using vector + graph queries, and flags accidental retcons **instantly with red squiggly underlines**—just like Grammarly, but for 40 years of cinematic canon.

---

## ⚡ 2. Technical Performance Budget & Stack
- **Target Performance Budget:** Full lore validation query loop: **< 20 milliseconds** inside ClickHouse.
- **Core Technology Stack:**
  - **Database:** ClickHouse Cloud (Columnar store for lore facts, timeline events, and causal triples `[Subject, Predicate, Object, Timestamp, Universe_ID, Status]`).
  - **Tool Integration:** Official ClickHouse MCP Server (`mcp-clickhouse`) connecting AI agents directly to ClickHouse.
  - **Reasoning Engine:** Gemini 2.0 Flash / Google Cloud ADK for entity extraction and semantic contradiction validation.
  - **Frontend:** Screenplay writing interface (like Final Draft / Fountain web editor) with real-time linting markers and lore side-panel.

---

## 🤖 3. Multi-Agent Orchestration Architecture
1. **Screenplay Stream Ingestion Agent:** Monitors keystrokes in the web editor, debounces sentences, extracts causal claims (`Subject -> Action -> Object -> Setting -> Year`), and constructs query vectors.
2. **ClickHouse High-Speed Lore Retrieval Agent:** Uses the ClickHouse MCP server to execute sub-20ms hybrid vector + relational graph lookups across the franchise history tables.
3. **Causal Logic & Contradiction Reasoning Agent:** Evaluates whether the proposed scene contradicts retrieved historical facts.
4. **Creative Mitigation & Alternative Suggester Agent:** Generates 3 creative solutions that preserve the writer's dramatic intent without breaking canon.
