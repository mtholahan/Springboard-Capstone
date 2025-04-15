"""
99_util_clean_title.py

Reusable title normalization utility for fuzzy matching.

Functions:
- clean_title(text): Normalize soundtrack or movie titles for better matching accuracy.
  - Lowercases text
  - Removes punctuation
  - Strips common noise terms like "OST", "Original Soundtrack", "Deluxe Edition", etc.
  - Returns a simplified string for use in fuzzy matching

Used by:
- 10_match_fuzzy_link_soundtracks.py
"""

import re

def clean_title(text):
    """
    Normalize soundtrack or movie titles:
    - Lowercase
    - Remove brackets, OST tags, subtitles
    - Strip noise words like "original soundtrack"
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()

    noise_patterns = [
        r'\(.*?\)',
        r'\[.*?\]',
        r'original motion picture soundtrack',
        r'original soundtrack',
        r'motion picture soundtrack',
        r'complete motion picture score',
        r'deluxe edition',
        r'expanded edition',
        r'\bost\b',
        r'\bsoundtrack\b',
        r'\bscore\b'
    ]

    for pattern in noise_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    text = re.sub(r'[^a-z0-9\s]', '', text)  # remove punctuation
    return re.sub(r'\s+', ' ', text).strip()
