# Musical Diversity in Movies – Project Proposal

## 🎯 Project Overview

This capstone project explores the relationship between a film's **soundtrack genre diversity** and its **metadata**, including popularity, release year, and genre classification. 

By integrating MusicBrainz (primary soundtrack source) with enriched movie data from **TMDb**, the project analyzes how musical diversity trends align with broader cinematic patterns.

---

## ❓ Problem Statement

Most film studies focus on box office or critic scores — this project examines the **musical fingerprint of movies**. 

Specifically:
- Do popular or critically acclaimed movies exhibit higher soundtrack genre diversity?
- Do genre-rich soundtracks correlate with specific eras or types of films?
- Are certain soundtrack genres overrepresented in particular genres or decades?

---

## ✅ Criteria for Success

- ✔️ Normalize and clean soundtrack data from MusicBrainz.
- ✔️ Enrich each movie with TMDb metadata: genre, popularity, release year, alternative titles.
- ✔️ Calculate genre diversity metrics per movie.
- ✔️ Link soundtracks to movies using manual, substring, and fuzzy matching.
- ✔️ Visualize trends in soundtrack composition across time and genres.

---

## 📦 Datasets

| Dataset       | Description                                    | Usage Status         |
|---------------|------------------------------------------------|----------------------|
| MusicBrainz    | Soundtrack release metadata                    | ✅ Cleaned and joined |
| TMDb           | Movie genres, popularity, release years, alt-titles | ✅ Enriched via API |
| IMDb           | Movie ratings and metadata                     | ❌ Not used (access restricted) |
| Last.fm        | Listener-based genre and tag data              | 🔄 Deferred for future enrichment |

---

## 🧱 Architecture

The end-to-end pipeline includes:

- 🧼 Cleanse `.tsv` dumps from MusicBrainz (`02_mb_cleanse_tsv_files.py`)
- 🔗 Join and filter soundtrack releases (`04_mb_full_join.py`, `05_mb_filter_soundtracks.py`)
- 🌐 Fetch top TMDb titles and metadata (`06` → `08`)
- 🧠 Normalize genres, compute diversity (`09`, `10`)
- 🧮 Store results in PostgreSQL for analysis

---

## 🛠 Technologies

- 🐘 **PostgreSQL** for data modeling and joins
- 🐍 **Python** (pandas, requests, rapidfuzz, psycopg2)
- 📊 **Power BI** (proposed) for final visualizations
- 📓 **Jupyter** for data profiling, EDA, and documentation
- 📎 **Git + GitHub** for versioning and collaboration

---

## 📌 Status

- ✅ Step 1–3: Complete (data audit, schema plan, initial joins)
- ✅ Step 4: Complete (homogeneity checks, enrichment, fuzzy match)
- 🔜 Step 5: Ready for modeling, insights, and visualization

