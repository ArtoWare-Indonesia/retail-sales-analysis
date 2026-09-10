"""Interactive visualization for the Retail Sales Analysis project."""

import logging
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

logger = logging.getLogger(__name__)


class InteractiveVisualizer:
    """Generate interactive Plotly charts and an HTML analysis dashboard."""

    def __init__(self, df: pd.DataFrame, output_dir="output/interactive"):
        self.df = df.copy()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _kpi_figure(self, kpis):
        labels = ["Sales", "Profit", "Margin", "Orders", "Customers", "Products"]
        values = [
            f"${kpis['total_sales']:,.0f}",
            f"${kpis['total_profit']:,.0f}",
            f"{kpis['profit_margin']:.2f}%",
            f"{kpis['total_orders']:,}",
            f"{kpis['total_customers']:,}",
            f"{kpis['total_products']:,}",
        ]
        fig = go.Figure()
        fig.add_trace(go.Table(
            header=dict(values=labels),
            cells=dict(values=[values[i] for i in range(len(values))]),
        ))
        fig.update_layout(title="Key Business Metrics", height=170)
        return fig

    def category_chart(self):
        data = self.df.groupby("Category", as_index=False).agg(
            Sales=("Sales", "sum"), Profit=("Profit", "sum")
        )
        return px.bar(data, x="Category", y="Sales", hover_data=["Profit"],
                      title="Interactive Sales by Category")

    def region_chart(self):
        data = self.df.groupby("Region", as_index=False).agg(
            Sales=("Sales", "sum"), Profit=("Profit", "sum")
        )
        return px.bar(data, x="Region", y="Sales", hover_data=["Profit"],
                      title="Interactive Sales by Region")

    def monthly_chart(self):
        data = self.df.copy()
        data["Month"] = data["Order Date"].dt.to_period("M").dt.to_timestamp()
        data = data.groupby("Month", as_index=False)["Sales"].sum()
        return px.line(data, x="Month", y="Sales", markers=True,
                       title="Interactive Monthly Sales Trend")

    def discount_profit_chart(self):
        return px.scatter(
            self.df,
            x="Discount",
            y="Profit",
            color="Category",
            hover_data=["Sales", "Product Name"],
            title="Interactive Discount vs Profit",
        )

    def run(self, kpis=None):
        """Generate the interactive HTML dashboard."""
        if kpis is None:
            from src.business_metrics import BusinessMetrics
            kpis = BusinessMetrics(self.df).run()

        figures = [
            self._kpi_figure(kpis),
            self.category_chart(),
            self.region_chart(),
            self.monthly_chart(),
            self.discount_profit_chart(),
        ]

        output_file = self.output_dir / "interactive_dashboard.html"
        html_parts = [
            "<!doctype html><html><head><meta charset='utf-8'>",
            "<title>Retail Sales Analysis — Interactive Dashboard</title>",
            "<style>body{font-family:Arial,sans-serif;max-width:1400px;margin:auto;padding:20px}" 
            ".chart{margin-bottom:30px}</style></head><body>",
            "<h1>Retail Sales Analysis — Interactive Dashboard</h1>",
            "<p>v0.6.0 interactive analysis generated from the cleaned dataset.</p>",
        ]
        for index, figure in enumerate(figures):
            html_parts.append(
                figure.to_html(
                    full_html=False,
                    include_plotlyjs="cdn" if index == 0 else False,
                    config={"displaylogo": False, "responsive": True},
                )
            )
            html_parts.append("<hr class='chart'>")
        html_parts.append("</body></html>")

        output_file.write_text("\n".join(html_parts), encoding="utf-8")
        logger.info("Interactive dashboard saved: %s", output_file)
        return output_file
