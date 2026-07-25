"""
Application configuration.
"""

from pathlib import Path

# Application
APP_NAME = "Retail Sales Analysis"
APP_VERSION = "v0.1.0"

# Directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
OUTPUT_DIR = BASE_DIR / "output"

# Dataset
DATASET_FILE = RAW_DATA_DIR / "superstore.csv"

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)