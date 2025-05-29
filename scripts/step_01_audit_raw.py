# step_01_audit_raw.py

from pathlib import Path
import csv
from base_step import BaseStep
from config import MB_RAW_DIR, TSV_WHITELIST

class Step01AuditRaw(BaseStep):

    def __init__(self, name="Step 01 Audit Raw"):
        super().__init__(name)

    def run(self):
        raw_files = sorted([
            f for f in MB_RAW_DIR.iterdir()
            if f.name in self.TSV_WHITELIST
        ])

        if not raw_files:
            self.logger.warning(f"No whitelisted files found in {MB_RAW_DIR}")
            return

        self.logger.info(f"Auditing {len(raw_files)} files in: {MB_RAW_DIR}")

        csv.field_size_limit(1_000_000)
        for tsv_path in self.progress_iter(raw_files, desc="Auditing TSVs"):
            try:
                with open(tsv_path, encoding="utf-8") as f:
                    reader = csv.reader(f, delimiter='\t')
                    headers = next(reader)
                    row_count = sum(1 for _ in reader)

                self.logger.info(f"{tsv_path.name}: {row_count:,} rows, {len(headers)} columns")
            except Exception as e:
                self.logger.error(f"Error reading {tsv_path.name}: {e}")

        self.logger.info(f"[DONE] Audited {len(raw_files)} TSV files.")
