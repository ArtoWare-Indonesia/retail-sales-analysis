"""
Retail Sales Analysis
Version : v0.1.0
Author  : ArtoWare Indonesia
"""
import logging

from src.loader import load_dataset
from config import APP_NAME, APP_VERSION, DATASET_FILE
from src.loader import load_dataset
from src.utils.logger import setup_logger

def main():
    """Main application entry point."""

    setup_logger()
    logger = logging.getLogger(APP_NAME)
    logger.info("=" * 50)
    logger.info("%s %s", APP_NAME, APP_VERSION)
    logger.info("=" * 50)
    logger.info("Loading dataset...")

    df = load_dataset(DATASET_FILE)

    logger.info("Dataset loaded successfully.")
    logger.info("Rows: %d", len(df))
    logger.info("Columns: %d", len(df.columns))


    logger.info("\nFirst 5 Rows")
    logger.info("-" * 50)
    logger.info(df.head())

    logger.info("\nDataset Information")
    logger.info("-" * 50)
    df.info()

    logger.info("\nDescriptive Statistics")
    logger.info("-" * 50)
    logger.info(df.describe(include="all"))

    logger.info("\nDone.")


if __name__ == "__main__":
    main()