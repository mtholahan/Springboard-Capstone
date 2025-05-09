# base_step.py

import logging
from pathlib import Path
import datetime
import sys
from tqdm import tqdm

class BaseStep:
    def __init__(self, name: str, config: dict = None):
        self.name = name
        self.config = config or {}
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.setup_logger()

    def setup_logger(self):
        log_dir = Path(self.config.get("log_dir", "./logs"))
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"{self.name}.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(self.name)
        self.logger.info(f"Initialized step: {self.name}")

    def progress_iter(self, iterable, desc=None):
        return tqdm(iterable, desc=desc or self.name)

    def run(self):
        raise NotImplementedError("Subclasses must implement a run() method.")

