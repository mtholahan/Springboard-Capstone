"""
Author: Mark Holahan
Date: 2025-03-24
Script Name: collect_data.py

Capstone Project: Musical Diversity in Movies

Purpose:
    This script initiates Step 3 of the Springboard Capstone Project.
    It connects to the MusicBrainz API to extract music-related metadata 
    for known composers and performers (e.g., songs, artists, soundtracks).
    The data is saved locally in a structured format for further transformation and analysis.

Usage:
    Run this script from the terminal:
        python collect_data.py
"""

import pandas as pd
import musicbrainzngs as mb
import os

def whosa_knockin():
    """Set the MusicBrainz User-Agent string.

    MusicBrainz requires a valid User-Agent with contact info 
    to identify API clients and prevent abuse.
    """
    mb.set_useragent("SpringboardCapstone", "1.0", "markholahan@proton.me")

def fetch_artist_data(artist_name: str, output_path: str) -> pd.DataFrame:
    """Search for an artist by name using MusicBrainz.

    Performs a fuzzy Lucene-style search with strict name matching,
    returns basic artist metadata, and saves results to CSV.
    """
    result = mb.search_artists(artist=artist_name, strict=True)
    artist_data = [{
        "name": artist["name"],
        "id": artist["id"],
        "type": artist.get("type", "N/A"),
        "country": artist.get("country", "N/A")
    } for artist in result["artist-list"] if artist["name"].lower() == artist_name.lower()]
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = pd.DataFrame(artist_data)
    df.to_csv(output_path, index=False)
    return df

def fetch_artist_by_id(artist_id: str, output_path: str, includes=None) -> pd.DataFrame:
    """Fetch release groups for an artist by MusicBrainz ID.

    Returns a list of soundtrack-type releases with metadata,
    filtered from the artist's full release group list.
    Saves the results to CSV.
    """
    if includes is None:
        includes = ["release-groups"]

    result = mb.get_artist_by_id(artist_id, includes=includes)
    release_groups = result["artist"].get("release-group-list", [])

    data = [{
        "title": rg["title"],
        "primary_type": rg.get("primary-type", "N/A"),
        "secondary_types": ", ".join(rg.get("secondary-type-list", [])),
        "first_release_date": rg.get("first-release-date", "N/A")
    } for rg in release_groups if "Soundtrack" in rg.get("secondary-type-list", [])]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = pd.DataFrame(data)
    if "first_release_date" in df.columns:
        df["release_year"] = df["first_release_date"].str[:4]
        df.sort_values("release_year", ascending=False, inplace=True)
    else:
        print("⚠️  'first_release_date' not found in DataFrame — skipping year normalization.")
    df.to_csv(output_path, index=False)
    return df

# Main
if __name__ == "__main__":
    whosa_knockin()

    df = fetch_artist_data("The Police", "data/raw/The_Police_Artists.csv")
    print(df.head())

    df = fetch_artist_by_id(
        artist_id="9e0e2b01-41db-4008-bd8b-988977d6019a",  # The Police
        output_path="data/raw/The_Police_Soundtracks.csv"
    )
    print(df.head())

    df = fetch_artist_data("Stewart Copeland", "data/raw/StewartCopeland.csv")
    print(df.head())

    df = fetch_artist_by_id(
        artist_id="885ae336-ef63-465d-a0e7-bdc0a5b788e8",  # Stewart Copeland
        output_path="data/raw/Copeland_Soundtracks.csv"
    )
    print(df.head())  
