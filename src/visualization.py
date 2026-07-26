import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


class Visualizer:
    """Generate charts for retail sales analysis."""

    def __init__(self, input_file, output_dir):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_data(self):
        logger.info("Loading cleaned dataset...")
        df = pd.read_csv(self.input_file)

        if "Order Date" in df.columns:
            df["Order Date"] = pd.to_datetime(df["Order Date"])

        return df

    def save_plot(self, filename):
        filepath = self.output_dir / filename
        plt.tight_layout()
        plt.savefig(filepath, dpi=300)
        plt.close()
        logger.info("Chart saved: %s", filepath)

    def sales_by_category(self, df):
        logger.info("Generating Sales by Category chart...")

        sales = (
            df.groupby("Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        plt.figure(figsize=(8, 5))
        sales.plot(kind="bar")
        plt.title("Sales by Category")
        plt.xlabel("Category")
        plt.ylabel("Sales")

        self.save_plot("sales_by_category.png")

    def sales_by_region(self, df):
        logger.info("Generating Sales by Region chart...")

        sales = (
            df.groupby("Region")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        plt.figure(figsize=(8, 5))
        sales.plot(kind="bar")
        plt.title("Sales by Region")
        plt.xlabel("Region")
        plt.ylabel("Sales")

        self.save_plot("sales_by_region.png")

    def monthly_sales_trend(self, df):
        logger.info("Generating Monthly Sales Trend chart...")

        monthly = (
            df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
            .sum()
        )

        monthly.index = monthly.index.astype(str)

        plt.figure(figsize=(10, 5))
        monthly.plot(kind="line", marker="o")
        plt.title("Monthly Sales Trend")
        plt.xlabel("Month")
        plt.ylabel("Sales")
        plt.xticks(rotation=45)

        self.save_plot("monthly_sales_trend.png")

    def top_customers(self, df):
        if "Customer Name" not in df.columns:
            logger.warning("Customer Name column not found.")
            return

        logger.info("Generating Top 10 Customers chart...")

        customers = (
            df.groupby("Customer Name")["Sales"]
            .sum()
            .nlargest(10)
        )

        plt.figure(figsize=(8, 6))
        customers.sort_values().plot(kind="barh")
        plt.title("Top 10 Customers")
        plt.xlabel("Sales")

        self.save_plot("top_10_customers.png")

    def top_bottom_products(self, df):
        if "Product Name" not in df.columns:
            logger.warning("Product Name column not found.")
            return

        logger.info("Generating Product charts...")

        sales = (
            df.groupby("Product Name")["Sales"]
            .sum()
        )

        top = sales.nlargest(10)
        bottom = sales.nsmallest(10)

        plt.figure(figsize=(8, 6))
        top.sort_values().plot(kind="barh")
        plt.title("Top 10 Products")
        plt.xlabel("Sales")
        self.save_plot("top_products.png")

        plt.figure(figsize=(8, 6))
        bottom.sort_values().plot(kind="barh")
        plt.title("Bottom 10 Products")
        plt.xlabel("Sales")
        self.save_plot("bottom_products.png")

    def profit_analysis(self, df):
        logger.info("Generating Profit Analysis chart...")

        profit = (
            df.groupby("Category")["Profit"]
            .sum()
            .sort_values(ascending=False)
        )

        plt.figure(figsize=(8, 5))
        profit.plot(kind="bar")
        plt.title("Profit by Category")
        plt.xlabel("Category")
        plt.ylabel("Profit")

        self.save_plot("profit_by_category.png")

    def run(self):
        df = self.load_data()

        self.sales_by_category(df)
        self.sales_by_region(df)

        if "Order Date" in df.columns:
            self.monthly_sales_trend(df)

        self.top_customers(df)
        self.top_bottom_products(df)
        self.profit_analysis(df)

        logger.info("Visualization completed successfully.")


if __name__ == "__main__":
    visualizer = Visualizer(
        input_file="data/processed/superstore_clean.csv",
        output_dir="output/charts",
    )

    visualizer.run()