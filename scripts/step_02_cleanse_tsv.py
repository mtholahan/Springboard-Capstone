# step_02_cleanse_tsv.py

from pathlib import Path
import csv
from base_step import BaseStep
from config import MB_RAW_DIR, MB_CLEANSED_DIR, TSV_WHITELIST

class Step02CleanseTSV(BaseStep):
    def __init__(self, name="Step 02 Cleanse TSV"):
        super().__init__(name)

    def run(self):
        MB_CLEANSED_DIR.mkdir(parents=True, exist_ok=True)
        raw_files = sorted([
            f for f in MB_RAW_DIR.iterdir()
            if f.name in TSV_WHITELIST
        ])

        if not raw_files:
            self.logger.warning("No files found to clean.")
            return

        csv.field_size_limit(1_000_000)
        for infile in self.progress_iter(raw_files, desc="Cleansing TSVs"):
            outfile = MB_CLEANSED_DIR / infile.name
            try:
                with open(infile, mode='r', encoding='utf-8', errors='replace') as fin, \
                     open(outfile, mode='w', encoding='utf-8', newline='') as fout:
                    reader = csv.reader(fin, delimiter='\t')
                    writer = csv.writer(fout, delimiter='\t')

                    row_count = 0
                    skipped = 0
                    headers = next(reader)
                    writer.writerow([cell.strip() for cell in headers])

                    for row in reader:
                        if len(row) != len(headers):
                            skipped += 1
                            continue
                        writer.writerow([cell.strip() for cell in row])
                        row_count += 1

                self.logger.info(f"Cleaned: {infile.name} -> {outfile.name} ({row_count:,} rows, {skipped} skipped)")
            except Exception as e:
                self.logger.error(f"Error processing {infile.name}: {e}")

        self.logger.info(f"[DONE] Cleansed {len(raw_files)} TSV files.")
