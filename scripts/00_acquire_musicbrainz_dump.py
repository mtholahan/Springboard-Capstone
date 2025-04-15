"""
00_acquire_musicbrainz_dump.py (7-Zip Selective Extraction)

Downloads the most recent MusicBrainz full dump and uses 7-Zip to extract only whitelisted files.
Avoids unpacking the full archive to disk. Cleans up after itself.
"""

import re
import urllib.request
import urllib.error
import subprocess
import shutil
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

# === Config ===
BASE_URL = "https://data.metabrainz.org/pub/musicbrainz/data/fullexport/"
TARGET_DIR = Path("D:/Capstone_Staging/data/musicbrainz_raw")
DERIVED_FILENAME = "mbdump-derived.tar.bz2"
FALLBACK_FILENAME = "mbdump.tar.bz2"
SEVEN_ZIP = Path("C:/Program Files/7-Zip/7z.exe")
MAX_ATTEMPTS = 10

TSV_WHITELIST = {
    "artist",
    "artist_credit",
    "artist_credit_name",
    "release",
    "release_group",
    "release_group_secondary_type",
    "release_group_secondary_type_join"
}

# === Logging ===
def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# === Main ===
def main():
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    log("\U0001F50D Checking MusicBrainz fullexport directory...")
    with urllib.request.urlopen(BASE_URL) as response:
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        folders = [a["href"].strip("/") for a in soup.find_all("a", href=True)
                   if re.match(r"\d{8}-\d{6}", a["href"])]
        sorted_folders = sorted(folders, reverse=True)

    tarbz2_path = None

    for folder in sorted_folders[:MAX_ATTEMPTS]:
        log(f"\U0001F50E Trying dump from {folder}...")
        log("⚠️ Skipping derived archive. Forcing full dump...")

        fallback_url = f"{BASE_URL}{folder}/{FALLBACK_FILENAME}"
        try:
            tarbz2_path = TARGET_DIR / FALLBACK_FILENAME
            urllib.request.urlretrieve(fallback_url, tarbz2_path)
            log(f"✅ Downloaded fallback: {FALLBACK_FILENAME}")
            break
        except urllib.error.HTTPError:
            log("❌ Fallback full dump also not found.")

    if not tarbz2_path or not tarbz2_path.exists():
        log("❌ Could not find a usable MusicBrainz dump in the last 10 days.")
        return

    # === Step 1: Extract .tar from .bz2 ===
    log("📦 Extracting .tar from .bz2 using 7-Zip...")
    tar_path = TARGET_DIR / FALLBACK_FILENAME.replace(".bz2", "")
    subprocess.run([str(SEVEN_ZIP), "e", str(tarbz2_path), f"-o{TARGET_DIR}"], check=True)

    # === Step 2: Use 7z list to find whitelisted paths inside tar ===
    log("🔍 Listing .tar contents to find whitelist targets...")
    result = subprocess.run([str(SEVEN_ZIP), "l", str(tar_path)], capture_output=True, text=True, check=True)
    lines = result.stdout.splitlines()
    file_paths = []

    for line in lines:
        parts = line.strip().split()
        if len(parts) < 6:
            continue
        filename = parts[-1]
        base = Path(filename).name
        if base in TSV_WHITELIST:
            file_paths.append(filename)

    # === Step 3: Extract only whitelisted files ===
    log("📂 Extracting only whitelisted files from .tar...")
    for f in file_paths:
        subprocess.run([str(SEVEN_ZIP), "e", str(tar_path), f"-o{TARGET_DIR}", f"-ir!{f}"], check=True)
        log(f"🧩 Extracted: {f}")

    # === Step 4: Cleanup ===
    try:
        tar_path.unlink(missing_ok=True)
        tarbz2_path.unlink(missing_ok=True)
        log("🧼 Cleanup complete.")
    except Exception as e:
        log(f"⚠️ Cleanup issue: {e}")

    log(f"✅ Fully extracted {len(file_paths)} whitelisted files to: {TARGET_DIR}")

if __name__ == "__main__":
    main()
