"""Data cleaning and data-quality validation for retail sales data."""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


class DataCleaner:
    """Clean and validate the retail sales dataset."""

    REQUIRED_COLUMNS = {
        "Order ID", "Customer ID", "Product ID", "Category", "Region",
        "Customer Name", "Product Name", "Order Date", "Ship Date",
        "Sales", "Profit", "Quantity", "Discount",
    }

    NUMERIC_COLUMNS = ["Sales", "Profit", "Quantity", "Discount"]
    DATE_COLUMNS = ["Order Date", "Ship Date"]

    def __init__(self, df, output_file):
        self.df = df
        self.output_file = Path(output_file)

    def validate(self, df):
        """Validate schema and critical business-data quality rules."""
        missing_columns = self.REQUIRED_COLUMNS - set(df.columns)
        if missing_columns:
            raise ValueError(
                "Missing required columns: "
                + ", ".join(sorted(missing_columns))
            )

        missing_values = df[list(self.REQUIRED_COLUMNS)].isna().sum()
        missing_values = missing_values[missing_values > 0]
        if not missing_values.empty:
            details = ", ".join(
                f"{column}={count}" for column, count in missing_values.items()
            )
            raise ValueError(f"Missing values in required columns: {details}")

        for column in self.NUMERIC_COLUMNS:
            if not pd.api.types.is_numeric_dtype(df[column]):
                raise ValueError(f"Column '{column}' must be numeric.")

            if not pd.to_numeric(df[column], errors="coerce").notna().all():
                raise ValueError(f"Column '{column}' contains invalid numeric values.")

        invalid_dates = {
            column: int(df[column].isna().sum())
            for column in self.DATE_COLUMNS
        }
        invalid_dates = {k: v for k, v in invalid_dates.items() if v}
        if invalid_dates:
            raise ValueError(f"Invalid dates found: {invalid_dates}")

        if (df["Ship Date"] < df["Order Date"]).any():
            raise ValueError("Ship Date cannot be earlier than Order Date.")

        if (df["Sales"] < 0).any():
            raise ValueError("Sales cannot contain negative values.")

        if (df["Quantity"] <= 0).any():
            raise ValueError("Quantity must be greater than zero.")

        if ((df["Discount"] < 0) | (df["Discount"] > 1)).any():
            raise ValueError("Discount must be between 0 and 1.")


        logger.info("Data-quality validation passed.")

    def run(self):
        df = self.df.copy()
        logger.info("Rows: %d | Columns: %d", *df.shape)

        logger.info("Checking missing values...")
        missing = df.isnull().sum()
        for column, count in missing.items():
            if count > 0:
                logger.info("%s : %d missing value(s)", column, count)

        duplicates = df.duplicated().sum()
        logger.info("Duplicate rows: %d", duplicates)
        if duplicates > 0:
            df = df.drop_duplicates()
            logger.info("Duplicate rows removed.")

        logger.info("Validating data types...")
        for column in self.DATE_COLUMNS:
            df[column] = pd.to_datetime(df[column], errors="coerce")
            logger.info("%s converted to datetime.", column)

        self.validate(df)

        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.output_file, index=False)
        logger.info("Clean dataset exported to %s", self.output_file)
        logger.info("Data cleaning completed successfully.")
        return df
