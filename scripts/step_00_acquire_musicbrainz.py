# step_00_acquire_musicbrainz.py

import re
import requests
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime
from base_step import BaseStep
from config import MB_RAW_DIR, SEVEN_ZIP_PATH
from tqdm import tqdm

class Step00AcquireMusicbrainz(BaseStep):
    BASE_URL = "https://data.metabrainz.org/pub/musicbrainz/data/fullexport/"
    FILENAME = "mbdump.tar.bz2"
    TSV_WHITELIST = {
        "artist", "artist_credit", "artist_credit_name", "release",
        "release_group", "release_group_secondary_type", "release_group_secondary_type_join"
    }

    def __init__(self, name):
        super().__init__(name)

    def download_with_progress(self, url: str, dest_path: Path):
        response = requests.get(url, stream=True)
        total = int(response.headers.get('content-length', 0))
        with open(dest_path, 'wb') as file, tqdm(
            desc="Downloading dump",
            total=total,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=1024):
                size = file.write(chunk)
                bar.update(size)

    def run(self):
        target_dir = MB_RAW_DIR
        seven_zip = SEVEN_ZIP_PATH
        max_attempts = 10

        target_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info("Checking MusicBrainz fullexport directory...")
        with requests.get(self.BASE_URL) as response:
            soup = BeautifulSoup(response.text, "html.parser")
            folders = sorted(
                [a["href"].strip("/") for a in soup.find_all("a", href=True)
                 if re.match(r"\d{8}-\d{6}", a["href"])],
                reverse=True
            )

        for folder in folders[:max_attempts]:
            url = f"{self.BASE_URL}{folder}/{self.FILENAME}"
            bz2_path = target_dir / self.FILENAME
            try:
                self.logger.info(f"Trying: {url}")
                self.download_with_progress(url, bz2_path)
                self.logger.info(f"Downloaded: {bz2_path}")
                break
            except requests.exceptions.HTTPError:
                self.logger.warning(f"Not found: {url}")
        else:
            self.logger.error("No usable dump found in last 10 attempts.")
            return

        # Step 1: Extract .tar
        tar_path = bz2_path.with_suffix("")  # strip .bz2
        subprocess.run([str(seven_zip), "e", str(bz2_path), f"-o{target_dir}"], check=True)
        self.logger.info(f"Extracted .tar to {tar_path}")

        # Step 2: List tar contents
        result = subprocess.run([str(seven_zip), "l", str(tar_path)],
                                capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines()
        whitelist_paths = [
            line.split()[-1] for line in lines
            if (len(line.split()) >= 6 and Path(line.split()[-1]).name in self.TSV_WHITELIST)
        ]

        # Step 3: Extract only whitelisted files
        for path in self.progress_iter(whitelist_paths, desc="Extracting TSVs"):
            subprocess.run([str(seven_zip), "e", str(tar_path), f"-o{target_dir}", f"-ir!{path}"], check=True)
            self.logger.info(f"Extracted: {path}")

        # Step 4: Cleanup
        for f in [bz2_path, tar_path]:
            try:
                f.unlink()
                self.logger.info(f"Removed: {f}")
            except Exception as e:
                self.logger.warning(f"Cleanup issue with {f}: {e}")

        self.logger.info(f"[OK] Finished extracting {len(whitelist_paths)} files to {target_dir}")
