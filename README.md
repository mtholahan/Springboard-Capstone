# Musical Diversity in Movies

## Overview
This is my Springboard Data Engineering Capstone Project, which analyzes the diversity of musical genres in movie soundtracks over time. By integrating data from MusicBrainz, TMDb, IMDb, Rotten Tomatoes, and Last.fm, this project explores how soundtrack genre diversity correlates with critical and audience reception. It aims to identify trends in soundtrack composition across different decades and assess whether certain genres are more commonly associated with highly-rated films.

📄 **[Read the full project proposal](Docs/Musical_Diversity_in_Movies_Proposal.md)**

## Data Sources
- **MusicBrainz** – Primary music metadata source.
- **IMDb** – Movie metadata, including ratings and genres.
- **Last.fm** – User-generated tags for refining genre classifications.

## Repository Structure
📂 `Docs/` – Contains the full project proposal and research.  
📂 `data/` – Placeholder for datasets (**not included** in the repo due to size limitations).  
📂 `notebooks/` – Jupyter notebooks for data exploration and analysis.  
📂 `scripts/` – Python scripts for data processing and integration.  
📂 `results/` – Final reports, charts, and summary analyses.

## Next Steps
✔ Data acquisition & cleaning  
✔ Exploratory data analysis  
✔ Building & optimizing data pipelines  
✔ Visualizing trends & insights  

---

## ✅ Step 4: Data Exploration & Enrichment

This step focused on verifying data quality, performing enrichment from TMDb, and linking soundtrack releases to movie metadata.

### Key Deliverables:
- 📓 [`Capstone_Step_4_Analysis.ipynb`](notebooks/Capstone_Step_4_Analysis.ipynb): Full column homogeneity checks across 10 tables
- 📘 [`Step_4_wrapup.ipynb`](notebooks/Step_4_wrapup.ipynb): Final Q&A (Questions 1–5), ERD, and storage strategy
- 🧩 [`Step_4_ERD.png`](notebooks/Step_4_ERD.png): Visual entity-relationship diagram for final schema
- 📽️ [`Step_4_Slide_Deck.pptx`](slides/Step_4_Slide_Deck.pptx): Slide deck summarizing Step 4 process
- 🛠 Scripts `02`–`10`: ETL pipeline for soundtrack filtering, TMDb enrichment, and fuzzy matching

### Outcome:
- All columns were verified for homogeneity
- Final PostgreSQL schema supports joinable, genre-enriched soundtrack data
- Project is now ready for SQL-based exploration, modeling, or feature engineering

## Contact
For questions or collaboration opportunities, reach out via **GitHub Issues**.

🚧 **This repository is a work in progress as part of my Data Engineering Bootcamp.** Stay tuned for updates! 🚧

<!-- Last updated: Sat, 12-April-2025 -->
