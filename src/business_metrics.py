"""
Business metrics for retail sales analysis.
"""

import logging
from pathlib import Path

import pandas as pd

from src.utils.logger import setup_logger

logger = logging.getLogger(__name__)


class BusinessMetrics:
    """Calculate key business metrics from cleaned retail data."""

    def __init__(self, input_file):
        self.input_file = Path(input_file)

    def load_data(self):
        """Load cleaned dataset."""

        logger.info(
            "Loading cleaned dataset: %s",
            self.input_file,
        )

        df = pd.read_csv(self.input_file)

        logger.info(
            "Dataset loaded successfully. Rows: %d | Columns: %d",
            len(df),
            len(df.columns),
        )

        return df

    def calculate_kpis(self, df):
        """Calculate key business performance indicators."""

        total_sales = df["Sales"].sum()
        total_profit = df["Profit"].sum()

        profit_margin = (
            total_profit / total_sales * 100
            if total_sales != 0
            else 0
        )

        total_orders = (
            df["Order ID"].nunique()
            if "Order ID" in df.columns
            else 0
        )

        total_customers = (
            df["Customer ID"].nunique()
            if "Customer ID" in df.columns
            else 0
        )

        total_products = (
            df["Product ID"].nunique()
            if "Product ID" in df.columns
            else 0
        )

        return {
            "total_sales": total_sales,
            "total_profit": total_profit,
            "profit_margin": profit_margin,
            "total_orders": total_orders,
            "total_customers": total_customers,
            "total_products": total_products,
        }

    def run(self):
        """Run business metrics calculation."""

        setup_logger()

        logger.info(
            "Starting business metrics calculation..."
        )

        df = self.load_data()

        kpis = self.calculate_kpis(df)

        logger.info(
            "Business metrics calculated successfully."
        )

        return kpis


if __name__ == "__main__":

    metrics = BusinessMetrics(
        input_file="data/processed/superstore_clean.csv"
    )

    kpis = metrics.run()

    print("\nBusiness Metrics")
    print("=" * 50)

    print(
        f"Total Sales     : {kpis['total_sales']:,.2f}"
    )

    print(
        f"Total Profit    : {kpis['total_profit']:,.2f}"
    )

    print(
        f"Profit Margin   : {kpis['profit_margin']:.2f}%"
    )

    print(
        f"Total Orders    : {kpis['total_orders']:,}"
    )

    print(
        f"Total Customers : {kpis['total_customers']:,}"
    )

    print(
        f"Total Products  : {kpis['total_products']:,}"
    )