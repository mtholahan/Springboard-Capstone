"""
10_write_junk_title_list.py

Creates or overwrites the official junk title list used by fuzzy match scripts.
"""

from config import JUNK_TITLE_LIST
from pathlib import Path

# --- Master list of known problematic titles ---
PROBLEM_TITLES = [
    "pure jerry merriweather post pavilion september 1 2 1989",
    # Add more here as needed
]

# --- Write to file ---
JUNK_TITLE_LIST.parent.mkdir(parents=True, exist_ok=True)

with open(JUNK_TITLE_LIST, "w", encoding="utf-8") as f:
    for title in PROBLEM_TITLES:
        f.write(title.strip().lower() + "\n")

print(f"✅ Wrote {len(PROBLEM_TITLES)} problem title(s) to: {JUNK_TITLE_LIST}")
