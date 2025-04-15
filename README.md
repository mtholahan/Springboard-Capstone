🎵 Musical Diversity in Movies – Springboard Capstone

📌 Project Overview

This capstone project explores the relationship between a film’s soundtrack genre diversity and its movie-level metadata, such as popularity, release year, and genre classification.

By integrating soundtrack data from MusicBrainz with enriched movie data from TMDb, the project builds a normalized dataset that enables querying, visualization, and downstream modeling.

📄 Read the full project proposal

📂 Data Sources

Source

Description

Status

MusicBrainz

Soundtrack metadata (title, artist, release)

✅ Cleaned & loaded

TMDb

Movie metadata (title, popularity, genres)

🔄 API enrichment

IMDb

Movie scores and critic ratings

❌ Not used

Last.fm

Listener-based genre tags

⏸️ Deferred

🗂️ Repository Structure

Folder

Description

Docs/

Proposal and architecture notes

notebooks/

Data exploration, enrichment, and summary work

scripts/

ETL and enrichment pipeline scripts (02–10)

results/

Final exports or joins (optional)

slides/

Slide decks for review and final submission

data/

Raw .tsv and .csv files (excluded from repo)

🧱 Architecture Overview

This project uses a modular, script-driven pipeline supported by Jupyter notebooks for exploratory work:

Pipeline Overview:

Raw TSVs → PostgreSQL → Soundtrack Filtering → TMDb Enrichment → Fuzzy Matching → Final Schema

Python scripts handle data loading, enrichment, and matching

PostgreSQL serves as the central data store

Final schema includes genre-normalized join tables for easy querying

💡 Note on MusicBrainz ingestion:

While the initial ingest of .tsv files is currently manual, I treated it as a simulated batch data lake. The engineering focus was on normalizing the data, resolving entity joins, and enriching it with TMDb metadata through an automated, script-driven API pipeline.

Future automation could include:

Programmatic TSV pull from MusicBrainz FTP

Script-based loader for Postgres using schema introspection

🔍 Step 4: Data Exploration & Enrichment

This step focused on verifying data quality, enriching movies via TMDb, and establishing fuzzy match pipelines to link soundtracks to their corresponding films.

📁 Key Deliverables

Capstone_Step_4_Analysis.ipynb — Column homogeneity checks across 10 tables

Step_4_wrapup.ipynb — Final Q&A, ERD, and storage discussion

Step_4_ERD.png — Visual schema overview (PostgreSQL)

Step_4_Slide_Deck.pptx — Slide walkthrough of enrichment process

✅ Outcome

Clean, validated soundtrack and movie data in PostgreSQL

Genre-normalized structure enables deep exploration

Ready for modeling, visualization, or feature engineering in Step 5

⏭️ Next Steps

Finalize genre diversity scoring strategy

Visualize genre diversity trends by decade

Model correlation between genre diversity and movie popularity

Deploy or publish key insights as part of final deliverable

🤝 Contact

For questions or collaboration, feel free to reach out:

📧 Email: markholahan@proton.me

🔗 LinkedIn: linkedin.com/in/mark-holahan-data-devotee

🧠 This project is part of my Springboard Data Engineering Bootcamp. Stay tuned for updates as it progresses!

