# step_04_mb_full_join.py

import csv
from pathlib import Path
from base_step import BaseStep
from config import MB_CLEANSED_DIR, DATA_DIR, TSV_WHITELIST

class Step04MBFullJoin(BaseStep):
    def __init__(self, name="Step 04 MB Full Join"):
        super().__init__(name)
        self.data = {}

    def load_file(self, name):
        import csv
        csv.field_size_limit(1_000_000)
        path = MB_CLEANSED_DIR / name
        with open(path, encoding="utf-8") as f:
            reader = csv.reader(f, delimiter='\t')
            header = next(reader)
            rows = [row for row in reader]
        return header, rows


    def run(self):
        required_files = ["release", "release_group", "artist_credit"]
        for fname in required_files:
            if fname not in TSV_WHITELIST:
                self.logger.error(f"Required file {fname} missing from whitelist")
                return

        # Load key files
        headers = {}
        for name in required_files:
            headers[name], self.data[name] = self.load_file(name)
            self.logger.info(f"Loaded {name}: {len(self.data[name]):,} rows")

        # Build ID maps
        release_group_map = {row[0]: row for row in self.data["release_group"]}
        artist_credit_map = {row[0]: row for row in self.data["artist_credit"]}

        # Join release with release_group and artist_credit
        release_header = headers["release"]
        joined = []

        for row in self.progress_iter(self.data["release"], desc="Joining Releases"):
            release_group_id = row[1]  # assuming this is the FK
            artist_credit_id = row[3]  # assuming this is the FK
            rg = release_group_map.get(release_group_id, [])
            ac = artist_credit_map.get(artist_credit_id, [])
            joined.append(row + rg + ac)

        output_path = DATA_DIR / "joined_release_data.tsv"
        with open(output_path, "w", encoding="utf-8", newline="") as fout:
            writer = csv.writer(fout, delimiter='\t')
            writer.writerows(joined)

        self.logger.info(f"[DONE] Wrote joined dataset to {output_path} ({len(joined):,} rows)")
