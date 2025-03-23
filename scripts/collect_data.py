"""
Author: Mark Holahan
Date: 2025-03-23
Script Name: collect_data.py
Purpose: 
    This script initiates Step 3 of the Springboard Capstone Project.
    It connects to the MusicBrainz API to extract music-related metadata 
    (e.g., songs, artists, genres) tied to movie soundtracks.
    The data is saved locally in a structured format for further transformation and analysis.
    
Capstone Project: Musical Diversity in Movies

Notes:
    - This script is the foundation of the data pipeline (ETL Step 1: Extract).
    - It may be extended to pull from TMDb and Last.fm APIs in later iterations.
    - All API keys, if used, are stored in a separate config file or environment variables.

Usage:
    Run this script from the terminal:
        python collect_data.py
"""
