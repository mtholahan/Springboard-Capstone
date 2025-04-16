# 🎵 Musical Diversity in Movies – Springboard Capstone

## 📌 Project Overview

This Springboard capstone explores the relationship between a film’s **soundtrack genre diversity** and its **movie-level metadata** (e.g., popularity, release year, genre).  

By integrating soundtrack data from **MusicBrainz** with enriched movie metadata from **TMDb**, the project creates a queryable dataset for analysis and potential modeling.

📄 [View the full project proposal](Docs/Capstone_Proposal.md)

---

## 📂 Data Sources

| Source        | Description                                   | Status            |
|---------------|-----------------------------------------------|-------------------|
| **MusicBrainz** | Soundtrack metadata (title, artist, release) | ✅ Cleaned & loaded |
| **TMDb**        | Movie metadata (title, popularity, genres)   | 🔄 API enrichment   |
| **IMDb**        | Movie scores and critic ratings              | ❌ Not used         |
| **Last.fm**     | Listener-based genre tags                    | ⏸️ Deferred         |

---

## 🧱 Architecture Overview

The project uses a modular, script-driven pipeline with PostgreSQL and Jupyter notebooks for exploratory analysis.

```text
Raw TSVs → PostgreSQL → Soundtrack Filtering → TMDb Enrichment
         → Fuzzy Matching → Final Schema
```

- Python scripts `02–10` perform ingestion, enrichment, matching, and export
- PostgreSQL stores cleaned and enriched datasets
- TMDb API provides genre/popularity/metadata enrichment
- Final schema includes genre-normalized join tables for easy SQL queries

---

## 🗂 Repository Structure

| Folder       | Description                                          |
|--------------|------------------------------------------------------|
| `Docs/`      | Proposal and architecture notes                      |
| `notebooks/` | EDA, enrichment validation, and visual analysis      |
| `scripts/`   | ETL and enrichment pipeline (parameterized Python)   |
| `results/`   | Final exports or resolved xrefs (optional)           |
| `slides/`    | Slide decks for mentor review and final submission   |
| `data/`      | Local TSV + CSV source files (excluded from Git)     |

---

## ✅ Step 4: Data Exploration & Enrichment

This step focused on:
- Cleaning and validating key columns (homogeneity checks)
- Building a fuzzy matching pipeline to align MusicBrainz + TMDb titles
- Logging and auditing scores and edge cases
- Establishing schema relationships (ERD + PostgreSQL joins)

📁 Deliverables:
- `Capstone_Step_4_Analysis.ipynb`
- `Step_4_wrapup.ipynb`
- `Step_4_ERD.png`
- `Step_4_Slide_Deck.pptx`

✅ Outcome: A working enrichment pipeline, match audit logs, and entity-linked datasets.

---

## 🛠 Local Setup

Make sure Python and Anaconda are on your system `PATH`:

```powershell
C:\ProgramDatanaconda3
C:\ProgramDatanaconda3\Scripts
```

Then verify:
```powershell
python --version
```

---

## ⏭️ Next Steps

- Finish TMDb enrichment for all soundtrack candidates
- Refine fuzzy matching (threshold tuning, RESCUE_MAP, genre filters)
- Build final reporting or analytics views
- Wrap up Step 5 and submit for mentor review

---

📬 **Contact**

- Email: markholahan@proton.me  
- LinkedIn: [linkedin.com/in/mark-holahan-data-devotee](https://linkedin.com/in/mark-holahan-data-devotee)

🧠 This project is part of my Springboard Data Engineering Bootcamp. Stay tuned for updates!
