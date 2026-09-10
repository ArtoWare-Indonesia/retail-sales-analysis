"""Business metrics for retail sales analysis."""

import logging

import pandas as pd

logger = logging.getLogger(__name__)


class BusinessMetrics:
    """Calculate key business metrics from a retail sales DataFrame."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def calculate_kpis(self, df: pd.DataFrame | None = None):
        """Calculate key business performance indicators."""
        data = self.df if df is None else df

        total_sales = data["Sales"].sum()
        total_profit = data["Profit"].sum()
        profit_margin = (
            total_profit / total_sales * 100
            if total_sales != 0
            else 0
        )

        return {
            "total_sales": total_sales,
            "total_profit": total_profit,
            "profit_margin": profit_margin,
            "total_orders": data["Order ID"].nunique()
            if "Order ID" in data.columns else 0,
            "total_customers": data["Customer ID"].nunique()
            if "Customer ID" in data.columns else 0,
            "total_products": data["Product ID"].nunique()
            if "Product ID" in data.columns else 0,
        }

    def run(self):
        """Run business metrics calculation on the supplied DataFrame."""
        logger.info("Starting business metrics calculation...")
        kpis = self.calculate_kpis()
        logger.info("Business metrics calculated successfully.")
        return kpis


if __name__ == "__main__":
    from src.loader import load_dataset

    df = load_dataset("data/processed/superstore_clean.csv")
    kpis = BusinessMetrics(df).run()

    print("\nBusiness Metrics")
    print("=" * 50)
    print(f"Total Sales     : {kpis['total_sales']:,.2f}")
    print(f"Total Profit    : {kpis['total_profit']:,.2f}")
    print(f"Profit Margin   : {kpis['profit_margin']:.2f}%")
    print(f"Total Orders    : {kpis['total_orders']:,}")
    print(f"Total Customers : {kpis['total_customers']:,}")
    print(f"Total Products  : {kpis['total_products']:,}")
