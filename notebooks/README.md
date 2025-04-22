# 🎬 Capstone – Step 4: Exploratory Data Analysis & Visualization

This notebook supports **Step 4** of my Springboard Capstone project.  
It focuses on analyzing and visualizing static data from the **MusicBrainz** and **TMDb** datasets, with a focus on **movie soundtracks** and how they relate to artist, genre, and release metadata.

---

## 📘 What's Inside

The notebook includes:

- ✅ Cleaned, reloaded MusicBrainz tables (PostgreSQL-based)
- ✅ SQL-driven exploration of the dataset using `sqlalchemy` + `pandas`
- ✅ Visuals powered by `matplotlib` to showcase trends and outliers

### 🔍 MusicBrainz Queries & Charts:
- Artist count by gender ✅
- Top artist areas ✅
- Artist productivity (Top 10 by release count) ✅
- Primary release types (Album, Single, EP) ✅
- Soundtrack release count and % of all releases ✅
- Top soundtrack artists (with label cleanup for visualization) ✅

---

## 🧠 Purpose

This notebook helps evaluate data quality, schema consistency, and soundness of enrichment joins — all to determine whether **movie soundtrack genre/popularity analysis** is viable for the Capstone.

---

## 🔌 PostgreSQL Setup (Local)

Queries run against a local PostgreSQL database (`musicbrainz`) using credentials and constants stored in `config.py`.

- Host: `localhost`
- Port: `5432`
- User: `postgres`
- Schema: `public`

---

## 📎 Assets

- 📓 Notebook: [`Step_4_wrapup_with_visuals.ipynb`](./Step_4_wrapup_with_visuals.ipynb)
- 🧭 ERD Image: [`Step_4_ERD.png`](./Step_4_ERD.png)
- 📊 Visuals embedded directly in the notebook

---

## 🔁 Next Steps

- Extend this notebook to include TMDb enrichment queries
- Explore links between soundtrack genres and movie popularity
- Begin transition into Step 5: Data Pipeline + Modeling

---

*Notebook authored by Mark Holahan – April 2025*  
