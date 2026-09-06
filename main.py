"""
Retail Sales Analysis
Version : v0.5.0
Author  : ArtoWare Indonesia
"""
import logging

from config import (APP_NAME, APP_VERSION, DATASET_FILE, )
from src.utils.logger import setup_logger
from src.loader import load_dataset
from src.cleaning import DataCleaner
from src.insights import BusinessInsights
from src.visualization import Visualizer


def main():
    """Main application entry point."""

    setup_logger()
    logger = logging.getLogger(APP_NAME)

    logger.info("=" * 50)
    logger.info("%s %s", APP_NAME, APP_VERSION)
    logger.info("=" * 50)

    try:
        # Load the dataset
        logger.info("Loading raw dataset...")
        df = load_dataset(DATASET_FILE)

        logger.info(
            "Dataset loaded successfully. "
            "Rows: %d, Columns: %d",
            len(df),
            len(df.columns)
        )

        # Data Cleaning
        logger.info("Starting data cleaning...")

        cleaner = DataCleaner(
            df,
            "data/processed/superstore_clean.csv"
        )

        cleaned_df = cleaner.run()

        # Business Insights
        #logger.info("Starting business insights analysis...")

        insights = BusinessInsights(cleaned_df)
        results = insights.run()

        #logger.info("Business insights analysis completed successfully."

        # Visualization
        #logger.info("Starting visualization...")

        visualizer = Visualizer(
            cleaned_df,
            output_dir="images",
        )

        visualizer.run()

        #logger.info("Visualization completed successfully.")

        logger.info("=" * 50) 
        logger.info("Retail Sales Analysis completed successfully.")
        logger.info("=" * 50)

        return results

    except Exception:
        logger.exception(
            "Retail Sales Analysis pipeline failed."
        )
        raise 

if __name__ == "__main__":
    main()