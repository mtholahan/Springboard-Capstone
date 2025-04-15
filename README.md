# 🎶 Musical Diversity in Movies – Springboard Capstone

## 📌 Project Overview
This capstone project explores the relationship between a film’s soundtrack genre diversity and its movie-level metadata, such as popularity, release year, and genre classification.

By integrating soundtrack data from MusicBrainz with enriched movie data from TMDb, the project builds a normalized dataset that enables querying, visualization, and downstream modeling.

📄 [Read the full project proposal](Docs/Capstone_Proposal.md)

---

## 📂 Data Sources
| Source     | Description                                 | Status             |
|------------|---------------------------------------------|--------------------|
| **MusicBrainz** | Soundtrack metadata (title, artist, release) | ✅ Cleaned & loaded |
| **TMDb**        | Movie metadata (title, popularity, genres)   | 📘 API enrichment   |
| **IMDb**        | Movie scores and critic ratings              | ❌ Not used         |
| **Last.fm**     | Listener-based genre tags                    | 🧊 Deferred         |

---

## 🗂 Repository Structure
| Folder       | Description                                        |
|--------------|----------------------------------------------------|
| `Docs/`      | Proposal and architecture notes                    |
| `notebooks/` | Data exploration, enrichment, and summary work     |
| `scripts/`   | ETL and enrichment pipeline scripts (02–10)        |
| `results/`   | (Optional) Final exports or joins                  |
| `slides/`    | Slide decks for review and final submission        |
| `data/`      | Raw `.tsv` and `.csv` files (excluded from repo)   |

---

## 🧠 Architecture Overview

This project uses a modular, script-driven pipeline supported by Jupyter notebooks for exploratory work:
```
Raw TSVs → PostgreSQL → Soundtrack Filtering → TMDb Enrichment
          → Fuzzy Matching → Final Schema
```
- Python scripts (02–10) handle data loading, enrichment, and matching
- PostgreSQL serves as the central data store
- Final schema includes genre-normalized join tables for easy querying

---

## 💡 Note on MusicBrainz Ingestion
MusicBrainz `.tsv` file ingestion is manual but scripted like a real-world data lake load. Future improvements might include:
- Programmatic TSV pulls from FTP
- Schema-based Postgres loaders

These were deferred in favor of enriching with TMDb and creating reproducible joins.

---

## ✅ Step 4: Data Exploration & Enrichment
This step focused on verifying data quality, enriching movies via TMDb, and establishing fuzzy match pipelines to link soundtracks to their corresponding films.

Key Deliverables:
- `Capstone_Step_4_Analysis.ipynb` — Column homogeneity checks across 10 tables
- `Step_4_wrapup.ipynb` — Final Q&A, ERD, and storage discussion
- `Step_4_ERD.png` — Visual schema overview (PostgreSQL)
- `Step_4_Slide_Deck.pptx` — Slide walkthrough of enrichment process

---

## 🔧 Developer Setup (API Key + Python)

### 1. Set Your API Key (PowerShell)
```powershell
$env:TMDB_API_KEY = "your_actual_tmdb_api_key"
```
This key lasts only for the current terminal session.

✅ Instead of typing it manually, run:
```powershell
.\setup_env.ps1
```
This script lives in your project root and securely sets the API key.

🧪 To verify:
```powershell
echo $env:TMDB_API_KEY
```

### 2. Add Python to Your System Path (One-Time Setup)
Make sure these paths are in your system `PATH` variable:
```
C:\ProgramData\anaconda3
C:\ProgramData\anaconda3\Scripts
```
After adding them, **restart PowerShell** to apply changes.

🧪 Then test:
```powershell
python --version
```
You should see something like `Python 3.11.7`.

---

## 🎯 Next Steps
- Finalize genre diversity scoring strategy
- Visualize genre diversity trends by decade
- Model correlation between genre diversity and movie popularity
- Deploy or publish key insights as part of final deliverable

---

## 🤝 Contact
For questions or collaboration, please reach out to Mark Holahan:

📧 Email: markholahan@proton.me  
🔗 LinkedIn: linkedin.com/in/mark-holahan-data-devotee

---

🧠 _This project is part of my Springboard Data Engineering Bootcamp. Stay tuned for updates as it progresses!_ 🚀
