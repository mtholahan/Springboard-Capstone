# step_03_check_structure.py

import csv
from collections import Counter
from pathlib import Path
from base_step import BaseStep
from config import MB_CLEANSED_DIR, TSV_WHITELIST

class Step03CheckStructure(BaseStep):
    def __init__(self, name):
        super().__init__(name)

    def run(self):
        input_files = sorted([
            f for f in MB_CLEANSED_DIR.iterdir()
            if f.name in TSV_WHITELIST
        ])

        if not input_files:
            self.logger.warning("No cleansed files found for structure check.")
            return

        csv.field_size_limit(1_000_000)
        for fpath in self.progress_iter(input_files, desc="Checking TSV Structure"):
            try:
                with open(fpath, encoding="utf-8") as f:
                    reader = csv.reader(f, delimiter='\t')
                    header_len = len(next(reader))
                    col_counts = Counter(len(row) for row in reader)

                issues = {k: v for k, v in col_counts.items() if k != header_len}
                if issues:
                    self.logger.warning(f"{fpath.name}: Column mismatch! Expected {header_len}, Found: {issues}")
                else:
                    self.logger.info(f"{fpath.name}: Structure OK ({header_len} columns)")

            except Exception as e:
                self.logger.error(f"Error processing {fpath.name}: {e}")
