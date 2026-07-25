import logging
from pathlib import Path

import pandas as pd


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


class DataCleaner:
    """Clean and validate retail sales dataset."""

    def __init__(self, input_file, output_file):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)

    def run(self):
        logger.info("Loading dataset: %s", self.input_file)

        df = pd.read_csv(self.input_file)

        logger.info("Rows: %d | Columns: %d", *df.shape)

        # Missing values
        logger.info("Checking missing values...")
        missing = df.isnull().sum()

        for column, count in missing.items():
            if count > 0:
                logger.info("%s : %d missing value(s)", column, count)

        # Duplicate rows
        duplicates = df.duplicated().sum()
        logger.info("Duplicate rows: %d", duplicates)

        if duplicates > 0:
            df = df.drop_duplicates()
            logger.info("Duplicate rows removed.")

        # Data type validation
        logger.info("Validating data types...")

        date_columns = ["Order Date", "Ship Date"]

        for column in date_columns:
            if column in df.columns:
                df[column] = pd.to_datetime(
                    df[column],
                    errors="coerce",
                )
                logger.info("%s converted to datetime.", column)

        logger.info("Current data types:")
        logger.info("\n%s", df.dtypes)

        # Export cleaned dataset
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(self.output_file, index=False)

        logger.info("Clean dataset exported to %s", self.output_file)
        logger.info("Data cleaning completed successfully.")

        return df


if __name__ == "__main__":
    cleaner = DataCleaner(
        input_file="data/raw/superstore.csv",
        output_file="data/processed/superstore_clean.csv",
    )

    cleaner.run()