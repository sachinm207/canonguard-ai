# 📖 CanonGuard AI: Studio Guide & Industry Glossary

Welcome to **CanonGuard AI**! This guide explains how the platform works, how major Hollywood entertainment studios manage multi-decade continuity, what each UI element means, and definitions for all industry and technical terms.

---

## 🎬 1. How Franchise Data Works: Previous Lore vs. Current Script

A fundamental question is: **"How is previous franchise data loaded, and what does 'current' mean?"**

### The Hollywood Problem: The Multi-Decade Franchise
Major studios (Marvel Studios, Lucasfilm, DC, Paramount) manage universes spanning **30 to 80 years** of movies, TV shows, comic books, and tie-in novels.
- Over 50 films and hundreds of tie-in stories exist.
- Human **"Lore Keepers"** (such as Leland Chee at Lucasfilm, who oversees the famous *"Holocron"* continuity database) maintain 800-page Franchise Story Bibles to track which character is alive, who owns what weapon, and what planets have toxic atmospheres.

### How Previous Lore is Loaded (Ingestion Pipeline)
1. **The Canonical Archive ("Previous Data"):**
   - In studio pipelines, past finished movie scripts, comic scripts, and production encyclopedias are ingested.
   - Text is parsed into structured entities, temporal lifespans, and relationships:
     - **Characters:** Name, Status (`ALIVE`, `DEAD`, `STASIS`), Birth Year, Death Year.
     - **Relics & Weapons:** Item Name, State (`ACTIVE`, `DESTROYED`), Destruction Year.
     - **Universe Rules (Axioms):** Physics, magic limits, planetary atmospheres.
   - In CanonGuard AI, this is stored in **ClickHouse** (`franchise_characters`, `canon_timeline_events`, `entity_relationships`, `canon_lore_rules`).
   - At system boot, the engine seeds **The ChronoVerse**—a 20-movie cinematic history spanning years 1900 to 2080.

2. **What "Current" Means (The Active Screenplay / Scene):**
   - **"Current"** refers to the **new script or scene currently being drafted** by a screenwriter in the writer's room today.
   - Screenwriters write **scene-by-scene**. For example: *Scene 14 takes place in 1982 in a Berlin safehouse*.
   - As the screenwriter types text for this *current* draft, CanonGuard streams each sentence to ClickHouse to verify:
     > *"Does what is happening in this current 1982 scene contradict anything established in the previous 40 years of movies?"*

---

## 🖥️ 2. Screenplay Studio Interface Breakdown

### What is `Cold War Requiem.fountain`?
- **Screenplay File Title:** In the top metadata bar, `Cold War Requiem.fountain` represents the active script file open in your editor.
- **What is `.fountain`?** 
  - [Fountain](https://fountain.io/) is the universal, open-source plaintext markup format used across the screenwriting industry (like Markdown is for programmers).
  - It allows writers to type standard scene headings, action descriptions, and dialogue in any plain text editor, which screenwriting software (Final Draft, Highland, Fade In) renders into industry-standard formatted script pages.
- **Setting: Berlin Safehouse | Scene Year: 1982:**
  - This is the **Scene Slugline (Heading)**. It tells the canon engine the temporal anchor (**1982**) and geographical location (**Berlin Safehouse**) of the current scene so it can evaluate whether characters or relics are valid for that specific year and place.

---

### What is "Auto-Lint Active (350ms)"?
- **What is a Linter?** In computer programming, a "linter" is a background tool that checks code as you type and draws red squiggly lines under bugs or syntax errors.
- **Auto-Lint Active:** CanonGuard AI is a **"Grammarly for Cinema Canon"**. It continuously monitors the editor.
- **350ms Debounce:** When you are typing, the engine waits 350 milliseconds after your last keystroke before scanning the text. This prevents spamming the database while you are midway through typing a word.
- Once 350ms passes, the system validates the line against ClickHouse in **under 1 millisecond** and injects an inline **red squiggly underline** under any continuity violation.

---

### What are "Demo Traps"?
- In software quality assurance and security, a **"trap"** (or canary test) is an intentionally planted error created to test whether an automated detection system catches it properly.
- The **"Preloaded Demo Traps"** buttons in the header (`Trap 1`, `Trap 2`, `Trap 3`) are 3 pre-configured Hollywood continuity blunders. Clicking any of them instantly loads that scenario into the editor:
  1. **Trap 1 (Stasis Paradox):** 
     - *Script:* `"Viktor arrives at the Berlin safehouse in 1982 to meet Elena."`
     - *Violation:* Viktor was in cryogenic stasis in Siberia from 1975 to 1995. He cannot be in Berlin in 1982!
  2. **Trap 2 (Destroyed Relic):** 
     - *Script:* `"Elena pulls the Sunstone from her coat to open the portal in 1982."`
     - *Violation:* The Sunstone was vaporized in 1960 during the Battle of Solaria (*ChronoVerse II*). It cannot exist in 1982.
  3. **Trap 3 (Biological Invariant):** 
     - *Script:* `"On Planet Zora, Lord Vane removes his helmet and takes a deep breath of the air."`
     - *Violation:* Zoran atmosphere is 85% toxic ammonia (*Lore Rule #4*). Breathing it causes instant death.

---

## 📚 3. Comprehensive Glossary of Keywords

| Term | What It Means | Why It Matters in CanonGuard AI |
| :--- | :--- | :--- |
| **Retcon** | Short for **Retroactive Continuity**. When a new film, book, or episode accidentally changes or contradicts previously established facts. | The primary problem CanonGuard AI prevents. Post-production reshoots to fix retcons cost studios $10M–$30M. |
| **Retcon Diagnostics** | The detailed analysis of why a line breaks canon, including the rule violated, the offending entity, and citations to past movies. | Displayed in the right-hand panel whenever a red squiggly line is flagged. |
| **Franchise Lore** | The collective canon, history, character timelines, and rules of a fictional universe. | Stored in ClickHouse as columnar tables representing characters, timeline events, and physical laws. |
| **Telemetry** | Real-time performance monitoring data (query latency in milliseconds, count of violations caught, audit logs). | Proves that ClickHouse verifies canon in sub-millisecond time (< 1ms vs. < 20ms target). |
| **Creative Mitigation** | AI-generated narrative solutions that preserve the writer's dramatic intention without violating canon. | Instead of just saying "Error!", Gemini suggests 3 story fixes (e.g. swap Viktor with his disciple Malakor). |
| **Auto-Patch** | A 1-click button that automatically replaces the continuity error in your screenplay with the selected AI mitigation. | Allows writers to resolve continuity blunders with zero friction in seconds. |
| **ReplacingMergeTree** | A specialized ClickHouse database table engine that automatically deduplicates records and maintains the latest state of an entity. | Used for `franchise_characters` to track changing character states (e.g., Alive -> Stasis -> Dead). |
| **Causal Graph Triple** | A data structure connecting `Subject -> Predicate -> Object` with temporal validity (e.g., `Sunstone -> Destroyed_In -> 1960`). | Used in `entity_relationships` to catch paradoxes involving destroyed relics or severed alliances. |
| **Vector Embedding (768-dim)** | A mathematical representation of text meaning (768 numbers) used for semantic search. | Stored in ClickHouse to find semantically similar past timeline events even if exact words differ. |
| **Sub-20ms Target** | Completing database verification faster than 20 milliseconds. | 20ms is the threshold where humans perceive an interaction as "instantaneous". CanonGuard operates at **0.3ms to 1.5ms**. |

---

## 🚀 4. How to Use the Screenplay Studio (Step-by-Step)

1. **Launch the Studio:**
   - Run `python3 -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8005` and open `http://127.0.0.1:8005`.
2. **Try a Demo Trap:**
   - Click **Trap 1 (Stasis)** in the top right.
   - Notice the text appears in the editor.
   - Within **0.5ms**, a red squiggly line underlines `"Viktor"`.
3. **Inspect the Retcon Diagnostic:**
   - Look at the right panel under **Retcon Diagnostics**.
   - Read the exact reason: *"Viktor was in cryogenic stasis from 1975 to 1995"*.
   - See the citation: *"ChronoVerse III: The Long Winter"*.
4. **Apply a 1-Click Auto-Patch:**
   - Under the diagnostic card, view the 3 AI Mitigations.
   - Click **Auto-Patch** on *"Character Substitution: Use Disciple Malakor"*.
   - The script updates instantly to Malakor, the red line turns green, and the diagnostic clears to **"Franchise Canon Clean ✨"**!
5. **Write Your Own Scenes:**
   - Type custom action lines or dialogue in Fountain format.
   - Change characters, years, and relics to see real-time verification in action!

---

## 🌌 6. Multi-Canon Universe Selector

Different productions and writers work in distinct universes with unique physical laws, character timelines, and artifacts. CanonGuard AI includes **3 pre-configured cinematic universes** out of the box, with instant switching:

| Universe | Genre & Timeline | Key Figures & Relics | Sample Continuity Rules |
| :--- | :--- | :--- | :--- |
| **ChronoVerse** | Sci-Fi / Time-Travel (1900–2080) | Viktor, Elena, Malakor; The Sunstone | Cryogenic stasis (1975–1995); Sunstone vaporized in 1960; Planet Zora has 85% ammonia atmosphere. |
| **Galactic Imperium** | Space Opera (2100–3200) | Grand Inquisitor Kael, Commander Vesh; Kyber Singularity Core | Inquisitor Kael executed in 2180; Kyber Core shattered in 2150; Planet Krynn has airless vacuum and solar radiation. |
| **Mythos Realm** | High Fantasy (Age of Legends, 1000–1500) | High King Eldor, Prince Theron; The Aethelgard Blade | King Eldor slain in 1450; Aethelgard Blade melted in dragonfire in 1300; Iron Wastes of Skar block all magic. |

### How to Switch Universes:
1. Locate the **Universe selector dropdown** in the studio header (`🌌 Universe: ChronoVerse (1900-2080)`).
2. Select any universe (e.g. `Galactic Imperium`).
3. The editor slugline and preloaded demo traps dynamically refresh with continuity traps specific to that universe!

---

## 📂 7. Screenplay Document Upload & Drag-and-Drop

Writing teams do not have to copy-paste scripts line-by-line. CanonGuard AI provides native file upload and drag-and-drop:

1. **Click `📂 Upload Script` Button:**
   - In the toolbar above the editor, click **`📂 Upload Script`**.
   - Select any `.fountain`, `.txt`, or `.fdx` screenplay from your computer.
   - The file parses automatically, updates the scene slugline, and begins real-time continuity validation immediately.
2. **Drag-and-Drop directly onto the editor:**
   - Drag any `.fountain` or `.txt` file from your desktop or file manager directly onto the text editor.
   - The editor highlights with an active drop border, immediately imports the script text, and triggers continuous linting.

---

## 📥 8. Custom Story Bible & Lore Ingestion

Have your own novel, video game, or TV show universe? You can ingest your own **Story Bible** into CanonGuard AI:

1. Click **`📥 Upload Lore Bible`** in the header.
2. An ingestion dialog appears with:
   - **Quick Sample Templates:** Click `Load CyberCity 2099` or `Load Shadow Realm` to see pre-populated templates.
   - **Universe Details:** Provide a Universe ID and Name (e.g. `dune_expanded_lore`, `Dune Expanded Canon`).
   - **Story Bible Content:** Paste your structured JSON, Markdown, or plaintext lore notes.
3. **Structured JSON Bible Schema:**
```json
{
  "characters": [
    {
      "name": "Alex Mercer",
      "status": "DEAD",
      "death_year": 2045,
      "stasis_start_year": 0,
      "stasis_end_year": 0,
      "faction": "Cyber-Resist",
      "bio": "Legendary netrunner neutralized in the 2045 mainframe collapse."
    }
  ],
  "relics": [
    {
      "name": "Neural Core",
      "status": "DESTROYED",
      "destruction_year": 2040,
      "notes": "Destroyed in the Great Grid Surge of 2040."
    }
  ],
  "rules": [
    {
      "rule_text": "Neural overclocking beyond Level 4 induces fatal synaptic shock.",
      "category": "BIOLOGICAL_INVARIANT",
      "severity": "CRITICAL"
    }
  ]
}
```
4. Click **`⚡ Ingest into ClickHouse`**:
   - The engine parses your entities, indexes them into ClickHouse tables under the new `universe_id`, and immediately activates your custom canon!

---

## 🔬 9. Competitive Landscape & Market Study

For a full breakdown of how CanonGuard AI compares to industry tools like **Final Draft 13**, **World Anvil**, **Campfire**, **Filmustage**, **StoryBirdie**, and **Sudowrite/ChatGPT**, check out our in-depth research:
👉 **[Read COMPETITIVE_ANALYSIS.md](COMPETITIVE_ANALYSIS.md)**

---

## 🧠 10. Architectural Knowledge Base & Q&A Archive

For deep technical insights on:
- What is "Canon"? (Etymology, history & Hollywood tiers)
- Why sub-20ms latency is mathematically essential for writer cognitive flow
- Scalability mathematics for 50+ movies in ClickHouse (only ~25 MB; $0.0006/month)
- Multi-universe partitioning architecture and custom ingestion pipelines
- Complete Q&A archive of all architectural decisions

👉 **[Read KNOWLEDGE_BASE.md](KNOWLEDGE_BASE.md)**


