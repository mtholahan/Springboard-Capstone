# step_05_filter_soundtracks.py

import csv
from base_step import BaseStep
from config import DATA_DIR, MB_RAW_DIR

class Step05FilterSoundtracks(BaseStep):
    def __init__(self, name):
        super().__init__(name)

    def load_secondary_type_map(self):
        path = MB_RAW_DIR / "release_group_secondary_type_join"
        with open(path, encoding="utf-8") as f:
            reader = csv.reader(f, delimiter='\t')
            header = next(reader)
            soundtrack_ids = {row[0] for row in reader if row[1] == "1"}
        return soundtrack_ids

    def run(self):
        joined_path = DATA_DIR / "joined_release_data.tsv"
        output_path = DATA_DIR / "soundtracks.tsv"

        if not joined_path.exists():
            self.logger.error(f"Missing input file: {joined_path}")
            return

        soundtrack_ids = self.load_secondary_type_map()
        matched = []
        skipped = 0

        with open(joined_path, encoding="utf-8") as fin:
            reader = csv.reader(fin, delimiter='\t')
            for row in self.progress_iter(reader, desc="Filtering Soundtracks"):
                release_group_id = row[4]  # Corrected to use numeric release_group_id
                if release_group_id in soundtrack_ids:
                    matched.append(row)
                else:
                    skipped += 1

        with open(output_path, "w", encoding="utf-8", newline="") as fout:
            writer = csv.writer(fout, delimiter='\t')
            writer.writerows(matched)

        self.logger.info(f"[DONE] Wrote {len(matched):,} soundtracks to {output_path} ({skipped:,} skipped)")

