# CanonGuard AI — Production-Grade Sample Datasets & Screenplay Test Suite

This directory contains real-world, cinematic production datasets for creating active studio story bibles using both **Method A (Direct Story Bible Ingestion)** and **Method B (Batch Screenplay Catalog Ingestion with Gemini AI)**, along with test screenplay scenes to run inside the **Screenplay Scene Editor**.

---

## Quick Overview of Examples

| Universe Example | Genre & Setting | Era | Ingestion Supported | Test Scenes Included |
| :--- | :--- | :--- | :--- | :--- |
| **Example 1: Aethelgard: The Broken Crowns** | Grimdark High Fantasy / Blood Magic | 1240–1325 A.D. | **Method A** (`.json`, `.md`) & **Method B** (`.fountain`) | 1 Retcon Error Scene (1310 A.D.)<br>1 Clean Scene (1310 A.D.) |
| **Example 2: Project Hyperion: 2180** | Hard Sci-Fi / Cyberpunk Space Opera | 2140–2195 A.D. | **Method A** (`.json`, `.md`) & **Method B** (`.fountain`) | 1 Multi-Retcon Scene (2182 A.D.)<br>1 Clean Scene (2182 A.D.) |

---

## Directory Layout

```
sample_data/
├── example_1_aethelgard/
│   ├── README.md                                      # Step-by-step instructions for Example 1
│   ├── method_a_story_bible.json                     # Method A: Full JSON Story Bible
│   ├── method_a_story_bible.md                       # Method A: Markdown / Tagged Prose Story Bible
│   ├── method_b_scripts/
│   │   ├── Aethelgard_Ep1_The_Cataclysm_1285.fountain # Method B: Ep. 1 Screenplay (Relic destroyed)
│   │   └── Aethelgard_Ep2_The_Frost_Tomb_1294.fountain # Method B: Ep. 2 Screenplay (Cryo-stasis & character deaths)
│   ├── test_scene_with_errors.fountain               # Test script: Contains intentional critical retcons (1310 A.D.)
│   └── test_scene_clean.fountain                     # Test script: 100% canon-compliant scene (1310 A.D.)
│
└── example_2_hyperion/
    ├── README.md                                      # Step-by-step instructions for Example 2
    ├── method_a_story_bible.json                     # Method A: Full JSON Story Bible
    ├── method_a_story_bible.md                       # Method A: Markdown / Tagged Prose Story Bible
    ├── method_b_scripts/
    │   ├── Hyperion_Ep1_The_Ganymede_Breach_2175.fountain # Method B: Ep. 1 Screenplay (Warp core destroyed)
    │   └── Hyperion_Ep2_Cold_Sleep_Transit_2178.fountain   # Method B: Ep. 2 Screenplay (Deep cryo stasis)
    ├── test_scene_with_errors.fountain               # Test script: Contains 3 intentional critical retcons (2182 A.D.)
    └── test_scene_clean.fountain                     # Test script: 100% canon-compliant scene (2182 A.D.)
```

---

## How to Test in the CanonGuard Web App

### 1. Ingesting via Method A (Direct Story Bible)
1. Open the CanonGuard web interface (`http://127.0.0.1:8005`).
2. Click **"⚡ Change Franchise (Lore Bible)"** in the top header.
3. In the Franchise Hub modal, click **"➕ Create New Universe"**.
4. Keep the default tab on **"📖 Method A: Direct Story Bible"**.
5. Click **"📁 Select File (.txt, .md, .json)"** and choose:
   - `sample_data/example_1_aethelgard/method_a_story_bible.json` OR
   - `sample_data/example_2_hyperion/method_a_story_bible.json`
   *(Or click "⚡ CyberCity 2099" / "🔮 Shadow Realm" quick templates, or paste the content directly into the text box).*
6. Click **"⚡ Save & Ingest Universe into ClickHouse"**.
7. CanonGuard immediately registers all characters, relics, and rules into ClickHouse columnar memory.

### 2. Ingesting via Method B (Batch Screenplay Catalog with Gemini AI)
1. In the Franchise Hub modal, click **"➕ Create New Universe"**.
2. Switch to the tab **"🎬 Method B: Batch Screenplay Catalog (Gemini AI)"**.
3. Fill in:
   - **Franchise Universe Name:** e.g. `Aethelgard: Chronicles` or `Project Hyperion Batch`
   - **Genre:** `Grimdark Fantasy` or `Hard Sci-Fi`
   - **Era:** `1240–1325` or `2140–2195`
4. Click **"📂 Select Multiple Script Files"** and select both files from `method_b_scripts/` (e.g. `Ep1` and `Ep2`).
5. Click **"🤖 Ingest Screenplay Batch (Gemini AI)"**.
6. Gemini 2.5 Flash and CanonGuard's Causal Ingestion Agent analyze the screenplays, sort temporal causality, detect character lifespans, cryogenic suspensions, and relic destructions, and seed the lore bible into ClickHouse.

### 3. Testing Real-Time Checking in the Screenplay Editor
1. In the top header bar, ensure your newly ingested franchise is selected in the **Franchise Universe** dropdown.
2. In the **Screenplay Scene Editor** (`#script-input`), copy-paste the contents of:
   - `test_scene_with_errors.fountain`:
     - **Watch the bottom feedback box:** Instantly highlights the offending words in **wavy red underline** (e.g. `High King Valerius IV` or `Hyperion Dark-Matter Drive`).
     - **Story Check Panel:** Shows the exact causal violation and 1-click suggested rewrites.
     - **Click the red word or "View Movie Proof":** Opens the **Movie Proof** modal displaying the authentic historical scene proving why it is an error!
   - `test_scene_clean.fountain`:
     - **Watch the bottom feedback box:** Instantly confirms clean canon with **🟢 Ready / Canon Compliant**!
