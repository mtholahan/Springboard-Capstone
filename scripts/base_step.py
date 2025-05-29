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

        try:
            sys.stdout.reconfigure(encoding='utf-8')  # Ensure stdout supports UTF-8
        except AttributeError:
            # Fallback for Python versions < 3.7
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(self.name)
        self.logger.info(f"Initialized step: {self.name}")

    def progress_iter(self, iterable, **kwargs):
        if 'desc' not in kwargs:
            kwargs['desc'] = self.name
        return tqdm(iterable, **kwargs)

    def run(self):
        raise NotImplementedError("Subclasses must implement a run() method.")
