"""
Visualization module for Retail Sales Analysis.

Version : v0.4.0
Author  : ArtoWare Indonesia
"""

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.utils.logger import setup_logger


logger = logging.getLogger(__name__)


class Visualizer:
    """Generate charts for retail sales analysis."""

    def __init__(self, input_file, output_dir="images"):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def load_data(self):
        """Load the cleaned dataset."""

        logger.info(
            "Loading cleaned dataset: %s",
            self.input_file,
        )

        df = pd.read_csv(self.input_file)

        if "Order Date" in df.columns:
            df["Order Date"] = pd.to_datetime(
                df["Order Date"],
                errors="coerce",
            )

        logger.info(
            "Dataset loaded successfully. Rows: %d | Columns: %d",
            len(df),
            len(df.columns),
        )

        return df

    def save_plot(self, filename):
        """Save the current matplotlib figure."""

        filepath = self.output_dir / filename

        plt.tight_layout()
        plt.savefig(
            filepath,
            dpi=300,
            bbox_inches="tight",
        )
        plt.close()

        logger.info(
            "Chart saved: %s",
            filepath,
        )

    @staticmethod
    def format_axis_values(ax):
        """Format Y-axis values with thousands separators."""

        ax.ticklabel_format(
            style="plain",
            axis="y",
            useOffset=False,
        )

        ax.get_yaxis().set_major_formatter(
            lambda value, position: f"{value:,.0f}"
        )

    def top_customers(self, df):
        """Generate Top 10 Customers chart."""

        if "Customer Name" not in df.columns:
            logger.warning(
                "Customer Name column not found."
            )
            return

        logger.info(
            "Generating Top 10 Customers chart..."
        )

        customers = (
            df.groupby("Customer Name")["Sales"]
            .sum()
            .nlargest(10)
        )

        fig, ax = plt.subplots(
            figsize=(9, 6)
        )

        customers.sort_values().plot(
            kind="barh",
            ax=ax,
        )

        ax.set_title(
            "Top 10 Customers by Sales"
        )
        ax.set_xlabel("Sales")
        ax.set_ylabel("Customer")

        ax.xaxis.set_major_formatter(
            lambda value, position: f"{value:,.0f}"
        )

        ax.grid(
            axis="x",
            linestyle="--",
            alpha=0.3,
        )

        self.save_plot(
            "top_10_customers.png"
        )

    def top_bottom_products(self, df):
        """Generate Top 10 and Bottom 10 Products charts."""

        if "Product Name" not in df.columns:
            logger.warning(
                "Product Name column not found."
            )
            return

        logger.info(
            "Generating Product Sales charts..."
        )

        product_sales = (
            df.groupby("Product Name")["Sales"]
            .sum()
        )

        top_products = product_sales.nlargest(10)
        bottom_products = product_sales.nsmallest(10)

        # Top 10 Products
        fig, ax = plt.subplots(
            figsize=(9, 6)
        )

        top_products.sort_values().plot(
            kind="barh",
            ax=ax,
        )

        ax.set_title(
            "Top 10 Products by Sales"
        )
        ax.set_xlabel("Sales")
        ax.set_ylabel("Product")

        ax.xaxis.set_major_formatter(
            lambda value, position: f"{value:,.0f}"
        )

        ax.grid(
            axis="x",
            linestyle="--",
            alpha=0.3,
        )

        self.save_plot(
            "top_products.png"
        )

        # Bottom 10 Products
        fig, ax = plt.subplots(
            figsize=(9, 6)
        )

        bottom_products.sort_values().plot(
            kind="barh",
            ax=ax,
        )

        ax.set_title(
            "Bottom 10 Products by Sales"
        )
        ax.set_xlabel("Sales")
        ax.set_ylabel("Product")

        ax.xaxis.set_major_formatter(
            lambda value, position: f"{value:,.0f}"
        )

        ax.grid(
            axis="x",
            linestyle="--",
            alpha=0.3,
        )

        self.save_plot(
            "bottom_products.png"
        )

    def sales_by_category(self, df):
        """Generate Sales by Category chart."""

        logger.info(
            "Generating Sales by Category chart..."
        )

        sales = (
            df.groupby("Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(8, 5))

        sales.plot(
            kind="bar",
            ax=ax,
        )

        ax.set_title("Sales by Category")
        ax.set_xlabel("Category")
        ax.set_ylabel("Sales")

        self.format_axis_values(ax)

        self.save_plot(
            "sales_by_category.png"
        )

    def sales_by_region(self, df):
        """Generate Sales by Region chart."""

        logger.info(
            "Generating Sales by Region chart..."
        )

        sales = (
            df.groupby("Region")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(8, 5))

        sales.plot(
            kind="bar",
            ax=ax,
        )

        ax.set_title("Sales by Region")
        ax.set_xlabel("Region")
        ax.set_ylabel("Sales")

        self.format_axis_values(ax)

        self.save_plot(
            "sales_by_region.png"
        )

    def monthly_sales_trend(self, df):
        """Generate polished monthly sales trend chart."""

        logger.info("Generating Monthly Sales Trend chart...")

        monthly = (
            df.groupby(
                df["Order Date"].dt.to_period("M")
            )["Sales"]
            .sum()
            .sort_index()
        )

        # Convert PeriodIndex to datetime for proper time-series plotting
        monthly.index = monthly.index.to_timestamp()

        highest_month = monthly.idxmax()
        highest_value = monthly.max()

        lowest_month = monthly.idxmin()
        lowest_value = monthly.min()

        fig, ax = plt.subplots(figsize=(12, 6))

        # Main line
        ax.plot(
            monthly.index,
            monthly.values,
            marker="o",
            linewidth=2.2,
            markersize=5,
        )

        # Highlight highest point
        ax.scatter(
            highest_month,
            highest_value,
            s=120,
            zorder=5,
        )

        ax.annotate(
            f"Highest\n{highest_value:,.0f}",
            xy=(highest_month, highest_value),
            xytext=(0, 22),
            textcoords="offset points",
            ha="center",
            fontsize=10,
            fontweight="bold",
        )

        # Highlight lowest point
        ax.scatter(
            lowest_month,
            lowest_value,
            s=120,
            zorder=5,
        )

        ax.annotate(
            f"Lowest\n{lowest_value:,.0f}",
            xy=(lowest_month, lowest_value),
            xytext=(0, -42),
            textcoords="offset points",
            ha="center",
            fontsize=10,
            fontweight="bold",
        )

        # Title and labels
        ax.set_title(
            "Monthly Sales Trend",
            fontsize=18,
            pad=15,
        )

        ax.set_xlabel(
            "Month",
            fontsize=11,
        )

        ax.set_ylabel(
            "Sales",
            fontsize=11,
        )

        # Format Y-axis
        ax.yaxis.set_major_formatter(
            lambda value, position: f"{value / 1000:.0f}K"
        )

        # Show every 6 months on X-axis
        ax.set_xticks(
            monthly.index[::6]
        )

        ax.set_xticklabels(
            monthly.index[::6].strftime("%Y-%m"),
            rotation=45,
            ha="right",
        )

        # Subtle horizontal grid
        ax.grid(
            axis="y",
            linestyle="--",
            alpha=0.25,
        )

        # Remove unnecessary top/right borders
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        self.save_plot(
            "monthly_sales_trend.png"
        )

    def profit_analysis(self, df):
        """Generate Profit by Category chart."""

        logger.info(
            "Generating Profit by Category chart..."
        )

        profit = (
            df.groupby("Category")["Profit"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(8, 5))

        profit.plot(
            kind="bar",
            ax=ax,
        )

        ax.set_title(
            "Profit by Category"
        )
        ax.set_xlabel("Category")
        ax.set_ylabel("Profit")

        self.format_axis_values(ax)

        self.save_plot(
            "profit_by_category.png"
        )

    def sales_vs_profit(self, df):
        """Generate Sales vs Profit scatter plot by category."""

        logger.info(
            "Generating Sales vs Profit chart..."
        )

        required_columns = [
            "Sales",
            "Profit",
            "Category",
        ]

        if not all(
            column in df.columns
            for column in required_columns
        ):
            logger.warning(
                "Required columns for Sales vs Profit "
                "chart are not available."
            )
            return

        fig, ax = plt.subplots(figsize=(10, 6))

        categories = df["Category"].dropna().unique()

        for category in categories:
            category_data = df[
                df["Category"] == category
            ]

            ax.scatter(
                category_data["Sales"],
                category_data["Profit"],
                alpha=0.5,
                label=category,
            )

        ax.axhline(
            y=0,
            linestyle="--",
            linewidth=1,
        )

        ax.set_title(
            "Sales vs Profit by Category"
        )
        ax.set_xlabel("Sales")
        ax.set_ylabel("Profit")

        ax.legend(
            title="Category"
        )

        self.save_plot(
            "sales_vs_profit.png"
        )

    def profit_margin_by_category(self, df):
        """Generate Profit Margin by Category chart."""

        logger.info(
            "Generating Profit Margin by Category chart..."
        )

        required_columns = [
            "Category",
            "Sales",
            "Profit",
        ]

        if not all(
            column in df.columns
            for column in required_columns
        ):
            logger.warning(
                "Required columns for Profit Margin "
                "chart are not available."
            )
            return

        category_summary = (
            df.groupby("Category")[["Sales", "Profit"]]
            .sum()
        )

        category_summary["Profit Margin"] = (
            category_summary["Profit"]
            / category_summary["Sales"]
            * 100
        )

        margin = (
            category_summary["Profit Margin"]
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(8, 5))

        bars = ax.bar(
            margin.index,
            margin.values,
        )

        ax.set_title(
            "Profit Margin by Category"
        )
        ax.set_xlabel("Category")
        ax.set_ylabel("Profit Margin (%)")

        ax.bar_label(
            bars,
            labels=[
                f"{value:.1f}%"
                for value in margin.values
            ],
            padding=3,
        )

        self.save_plot(
            "profit_margin_by_category.png"
        )

    def sales_profit_by_region(self, df):
        """Generate Sales and Profit by Region combo chart."""

        logger.info(
            "Generating Sales & Profit by Region combo chart..."
        )

        required_columns = [
            "Region",
            "Sales",
            "Profit",
        ]

        if not all(
            column in df.columns
            for column in required_columns
        ):
            logger.warning(
                "Required columns for Sales & Profit "
                "by Region chart are not available."
            )
            return

        region_summary = (
            df.groupby("Region")[["Sales", "Profit"]]
            .sum()
            .sort_values("Sales", ascending=False)
        )

        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Sales bar chart
        bars = ax1.bar(
            region_summary.index,
            region_summary["Sales"],
            label="Sales",
        )

        ax1.set_xlabel("Region")
        ax1.set_ylabel("Sales")

        ax1.tick_params(
            axis="x",
            rotation=0,
        )

        ax1.yaxis.set_major_formatter(
            lambda value, position: f"{value:,.0f}"
        )

        # Profit line chart
        ax2 = ax1.twinx()

        ax2.plot(
            region_summary.index,
            region_summary["Profit"],
            marker="o",
            linewidth=2,
            label="Profit",
        )

        ax2.set_ylabel("Profit")

        ax2.yaxis.set_major_formatter(
            lambda value, position: f"{value:,.0f}"
        )

        # Add Sales labels
        for bar in bars:
            height = bar.get_height()

            ax1.annotate(
                f"{height:,.0f}",
                xy=(
                    bar.get_x() + bar.get_width() / 2,
                    height,
                ),
                xytext=(0, 5),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=9,
            )

        # Add Profit labels
        for x, profit in zip(
            region_summary.index,
            region_summary["Profit"],
        ):
            ax2.annotate(
                f"{profit:,.0f}",
                xy=(x, profit),
                xytext=(0, 8),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=9,
            )

        ax1.set_title(
            "Sales & Profit by Region"
        )

        # Combined legend
        handles1, labels1 = ax1.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()

        ax1.legend(
            handles1 + handles2,
            labels1 + labels2,
            loc="upper right",
        )

        self.save_plot(
            "sales_profit_by_region.png"
        )

    def run(self):
        """Generate all visualization charts."""

        logger.info(
            "Starting visualization pipeline..."
        )

        df = self.load_data()

        self.sales_by_category(df)
        self.sales_by_region(df)

        if "Order Date" in df.columns:
            self.monthly_sales_trend(df)

        self.top_customers(df)
        self.top_bottom_products(df)
        self.profit_analysis(df)

        self.sales_vs_profit(df)
        self.profit_margin_by_category(df)
        self.sales_profit_by_region(df)

        logger.info(
            "Visualization completed successfully."
        )


if __name__ == "__main__":
    setup_logger()

    visualizer = Visualizer(
        input_file="data/processed/superstore_clean.csv",
        output_dir="images",
    )

    visualizer.run()