"""Interactive visualization for the Retail Sales Analysis project."""

import logging
from pathlib import Path

import pandas as pd
import plotly.express as px

logger = logging.getLogger(__name__)


class InteractiveVisualizer:
    """Generate interactive Plotly charts and a portfolio-ready HTML dashboard."""

    def __init__(self, df: pd.DataFrame, output_dir="output/interactive"):
        self.df = df.copy()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _format_kpis(kpis):
        """Return presentation-ready KPI values."""
        return [
            ("Sales", f"${kpis['total_sales']:,.0f}"),
            ("Profit", f"${kpis['total_profit']:,.0f}"),
            ("Profit Margin", f"{kpis['profit_margin']:.2f}%"),
            ("Orders", f"{kpis['total_orders']:,}"),
            ("Customers", f"{kpis['total_customers']:,}"),
            ("Products", f"{kpis['total_products']:,}"),
        ]

    @staticmethod
    def _style_chart(fig, title):
        """Apply a consistent presentation style to interactive charts."""
        fig.update_layout(
            title=dict(text=title, x=0.02, xanchor="left"),
            template="plotly_white",
            font=dict(family="Arial, sans-serif", size=13),
            margin=dict(l=55, r=30, t=65, b=50),
            hoverlabel=dict(font_size=12),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(gridcolor="#E5E7EB", zeroline=False)
        return fig

    def category_chart(self):
        data = self.df.groupby("Category", as_index=False).agg(
            Sales=("Sales", "sum"), Profit=("Profit", "sum")
        )
        fig = px.bar(
            data,
            x="Category",
            y="Sales",
            hover_data={"Profit": ":,.0f", "Sales": ":,.0f"},
            labels={"Sales": "Sales", "Category": ""},
        )
        return self._style_chart(fig, "Sales by Category")

    def region_chart(self):
        data = self.df.groupby("Region", as_index=False).agg(
            Sales=("Sales", "sum"), Profit=("Profit", "sum")
        )
        fig = px.bar(
            data,
            x="Region",
            y="Sales",
            hover_data={"Profit": ":,.0f", "Sales": ":,.0f"},
            labels={"Sales": "Sales", "Region": ""},
        )
        return self._style_chart(fig, "Sales by Region")

    def monthly_chart(self):
        data = self.df.copy()
        data["Month"] = data["Order Date"].dt.to_period("M").dt.to_timestamp()
        data = data.groupby("Month", as_index=False)["Sales"].sum()
        fig = px.line(
            data,
            x="Month",
            y="Sales",
            markers=True,
            labels={"Sales": "Sales", "Month": ""},
        )
        fig.update_traces(line=dict(width=3), marker=dict(size=7))
        return self._style_chart(fig, "Monthly Sales Trend")

    def discount_profit_chart(self):
        fig = px.scatter(
            self.df,
            x="Discount",
            y="Profit",
            color="Category",
            hover_data={"Sales": ":,.0f", "Product Name": True},
            labels={"Discount": "Discount", "Profit": "Profit"},
        )
        return self._style_chart(fig, "Discount vs Profit")

    def _kpi_cards_html(self, kpis):
        """Build lightweight HTML KPI cards instead of a Plotly table."""
        cards = []
        for label, value in self._format_kpis(kpis):
            cards.append(
                f"<div class='kpi-card'>"
                f"<div class='kpi-label'>{label}</div>"
                f"<div class='kpi-value'>{value}</div>"
                f"</div>"
            )
        return "\n".join(cards)

    def run(self, kpis=None):
        """Generate the interactive HTML dashboard."""
        if kpis is None:
            from src.business_metrics import BusinessMetrics
            kpis = BusinessMetrics(self.df).run()

        charts = [
            ("wide", self.monthly_chart()),
            ("half", self.category_chart()),
            ("half", self.region_chart()),
            ("wide", self.discount_profit_chart()),
        ]

        output_file = self.output_dir / "interactive_dashboard.html"
        html_parts = [
            "<!doctype html>",
            "<html lang='en'>",
            "<head>",
            "<meta charset='utf-8'>",
            "<meta name='viewport' content='width=device-width, initial-scale=1'>",
            "<title>Retail Sales Analysis — Interactive Dashboard</title>",
            """<style>
            :root {
                --page: #f5f7fa;
                --surface: #ffffff;
                --text: #172033;
                --muted: #667085;
                --border: #e4e7ec;
                --accent: #2563eb;
            }
            * { box-sizing: border-box; }
            body { margin: 0; background: var(--page); color: var(--text); font-family: Arial, sans-serif; }
            .dashboard { max-width: 1440px; margin: 0 auto; padding: 32px 24px 48px; }
            .hero { margin-bottom: 24px; }
            .eyebrow { color: var(--accent); font-size: 12px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; margin-bottom: 8px; }
            h1 { margin: 0 0 8px; font-size: clamp(28px, 4vw, 42px); line-height: 1.1; }
            .subtitle { margin: 0; color: var(--muted); font-size: 15px; }
            .kpi-grid { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 14px; margin-bottom: 20px; }
            .kpi-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 18px; box-shadow: 0 2px 8px rgba(16, 24, 40, .04); }
            .kpi-label { color: var(--muted); font-size: 12px; font-weight: 600; margin-bottom: 8px; }
            .kpi-value { font-size: clamp(20px, 2vw, 28px); font-weight: 700; line-height: 1.15; }
            .chart-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; }
            .chart-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 8px 10px 2px; box-shadow: 0 2px 8px rgba(16, 24, 40, .04); overflow: hidden; }
            .chart-card.wide { grid-column: 1 / -1; }
            .footer { color: var(--muted); font-size: 12px; text-align: center; margin-top: 28px; }
            @media (max-width: 1050px) { .kpi-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
            @media (max-width: 720px) {
                .dashboard { padding: 24px 14px 36px; }
                .kpi-grid, .chart-grid { grid-template-columns: 1fr; }
                .chart-card.wide { grid-column: auto; }
            }
            </style>""",
            "</head>",
            "<body>",
            "<main class='dashboard'>",
            "<section class='hero'>",
            "<div class='eyebrow'>Business Intelligence Portfolio</div>",
            "<h1>Retail Sales Analysis</h1>",
            "<p class='subtitle'>Interactive overview of sales performance, profitability, trends, and discount impact.</p>",
            "</section>",
            f"<section class='kpi-grid'>{self._kpi_cards_html(kpis)}</section>",
            "<section class='chart-grid'>",
        ]

        for index, (size, figure) in enumerate(charts):
            html_parts.append(f"<div class='chart-card {size}'>")
            html_parts.append(
                figure.to_html(
                    full_html=False,
                    include_plotlyjs="cdn" if index == 0 else False,
                    config={
                        "displaylogo": False,
                        "responsive": True,
                        "modeBarButtonsToRemove": ["lasso2d", "select2d"],
                    },
                )
            )
            html_parts.append("</div>")

        html_parts.extend(
            [
                "</section>",
                "<div class='footer'>Generated from the cleaned Superstore dataset · Interactive analysis engine v0.6.0</div>",
                "</main>",
                "</body>",
                "</html>",
            ]
        )

        output_file.write_text("\n".join(html_parts), encoding="utf-8")
        logger.info("Interactive dashboard saved: %s", output_file)
        return output_file
