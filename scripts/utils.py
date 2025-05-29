# utils.py

import re
import pandas as pd

def normalize_title(title):
    """
    Normalize a string: lowercase, remove punctuation, collapse spaces, strip.
    """
    if pd.isna(title):
        return ""
    title = title.lower()
    title = re.sub(r"[^a-z0-9\s]", "", title)   # remove non-alphanumerics
    title = re.sub(r"\s+", " ", title)          # normalize multiple spaces
    return title.strip()

def is_mostly_digits(s, threshold=0.7):
    digits = sum(c.isdigit() for c in s)
    return digits / max(len(s), 1) > threshold
