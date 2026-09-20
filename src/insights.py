"""
Business insights for retail sales analysis.
"""

import logging

import pandas as pd


logger = logging.getLogger(__name__)


REQUIRED_COLUMNS = {
    "Category",
    "Region",
    "Customer Name",
    "Product Name",
    "Order Date",
    "Sales",
    "Profit",
}


class BusinessInsights:
    """Generate business insights from retail sales data."""

    def __init__(self, df):
        self.df = df.copy()
        self._validate_schema()

    def _validate_schema(self):
        """Validate the minimum dataframe schema required by this module."""
        missing = REQUIRED_COLUMNS - set(self.df.columns)

        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

    @staticmethod
    def _add_profit_margin(summary):
        """Add profit margin calculated from aggregated sales and profit."""
        summary = summary.copy()
        summary["Profit Margin"] = (
            summary["Profit"]
            .div(summary["Sales"])
            .mul(100)
            .where(summary["Sales"] != 0, 0)
        )
        return summary

    def _performance_summary(self, df, dimension):
        """Aggregate sales, profit, and margin for a business dimension."""
        summary = (
            df.groupby(dimension)
            .agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum"),
            )
        )
        return self._add_profit_margin(summary)

    @staticmethod
    def _product_summary(df):
        """Aggregate sales and profit by product."""
        return (
            df.groupby("Product Name")
            .agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum"),
            )
        )

    @staticmethod
    def _customer_sales(df):
        """Aggregate and sort sales by customer."""
        return (
            df.groupby("Customer Name")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

    @staticmethod
    def _safe_contribution(value, total):
        """Return percentage contribution without division-by-zero errors."""
        if total == 0:
            return 0
        return value / total * 100

    def category_insights(self, df):
        """Generate category-level insights."""

        logger.info(
            "Analyzing category performance..."
        )

        summary = self._performance_summary(df, "Category")

        best_sales = summary["Sales"].idxmax()
        best_profit = summary["Profit"].idxmax()
        best_margin = summary["Profit Margin"].idxmax()

        return {
            "summary": summary,
            "highest_sales_category": best_sales,
            "highest_profit_category": best_profit,
            "highest_margin_category": best_margin,
        }

    def region_insights(self, df):
        """Generate region-level insights."""

        logger.info(
            "Analyzing regional performance..."
        )

        summary = self._performance_summary(df, "Region")

        best_sales = summary["Sales"].idxmax()
        best_profit = summary["Profit"].idxmax()
        best_margin = summary["Profit Margin"].idxmax()

        return {
            "summary": summary,
            "highest_sales_region": best_sales,
            "highest_profit_region": best_profit,
            "highest_margin_region": best_margin,
        }

    def monthly_insights(self, df):
        """Generate monthly sales insights."""

        logger.info(
            "Analyzing monthly sales performance..."
        )

        df = df.copy()

        df["Order Date"] = pd.to_datetime(
            df["Order Date"],
            errors="coerce",
        )

        monthly = (
            df.groupby(
                df["Order Date"].dt.to_period("M")
            )["Sales"]
            .sum()
        )

        highest_month = monthly.idxmax()
        lowest_month = monthly.idxmin()

        return {
            "monthly_sales": monthly,
            "highest_sales_month": highest_month,
            "highest_sales_value": monthly.max(),
            "lowest_sales_month": lowest_month,
            "lowest_sales_value": monthly.min(),
        }

    def customer_insights(self, df):
        """Generate customer-level insights."""

        logger.info(
            "Analyzing customer performance..."
        )

        customers = self._customer_sales(df)

        top_customer = customers.idxmax()

        return {
            "top_customer": top_customer,
            "top_customer_sales": customers.max(),
            "top_10_customers": customers.nlargest(10),
        }

    def product_insights(self, df):
        """Generate product-level insights."""

        logger.info(
            "Analyzing product performance..."
        )

        products = self._product_summary(df)

        top_sales_product = products["Sales"].idxmax()
        top_profit_product = products["Profit"].idxmax()

        return {
            "products": products,
            "top_sales_product": top_sales_product,
            "top_sales_value": products.loc[
                top_sales_product,
                "Sales",
            ],
            "top_profit_product": top_profit_product,
            "top_profit_value": products.loc[
                top_profit_product,
                "Profit",
            ],
        }

    def contribution_analysis(self, df):
        """Analyze sales and profit contribution."""

        logger.info(
            "Analyzing sales and profit contribution..."
        )

        total_sales = df["Sales"].sum()
        total_profit = df["Profit"].sum()

        # Category contribution
        category = self._performance_summary(df, "Category")
        category["Sales Contribution"] = category["Sales"].apply(
            self._safe_contribution,
            total=total_sales,
        )
        category["Profit Contribution"] = category["Profit"].apply(
            self._safe_contribution,
            total=total_profit,
        )

        # Region contribution
        region = self._performance_summary(df, "Region")
        region["Sales Contribution"] = region["Sales"].apply(
            self._safe_contribution,
            total=total_sales,
        )
        region["Profit Contribution"] = region["Profit"].apply(
            self._safe_contribution,
            total=total_profit,
        )

        # Customer concentration
        customers = self._customer_sales(df)
        top_customer_sales = customers.iloc[0]
        top_10_customer_sales = customers.head(10).sum()

        # Product concentration
        products = self._product_summary(df)
        top_product_sales = products["Sales"].max()
        top_product_profit = products["Profit"].max()

        return {
            "category": category,
            "region": region,
            "top_customer_contribution": (
                top_customer_contribution
            ),
            "top_10_customer_contribution": (
                top_10_customer_contribution
            ),
            "top_product_sales_contribution": (
                top_product_sales_contribution
            ),
            "top_product_profit_contribution": (
                top_product_profit_contribution
            ),
        }

    def profitability_analysis(self, df):
        """Analyze profitability risks."""

        logger.info(
            "Analyzing profitability risks..."
        )

        # Category
        category = (
            df.groupby("Category")
            .agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum"),
            )
        )

        category["Profit Margin"] = (
            category["Profit"]
            / category["Sales"]
            * 100
        )

        # Region
        region = (
            df.groupby("Region")
            .agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum"),
            )
        )

        region["Profit Margin"] = (
            region["Profit"]
            / region["Sales"]
            * 100
        )

        # Products
        products = (
            df.groupby("Product Name")
            .agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum"),
            )
        )

        loss_making_products = (
            products[products["Profit"] < 0]
        )
        total_loss = loss_making_products["Profit"].sum()

        return {
            "category": category,
            "region": region,
            "lowest_margin_category": (
                category["Profit Margin"].idxmin()
            ),
            "lowest_margin_region": (
                region["Profit Margin"].idxmin()
            ),
            "loss_making_products": loss_making_products,
            "loss_making_product_count": (
                len(loss_making_products)
            ),
            "total_loss": total_loss,
        }

    def generate_narrative(self, results):
        """Generate business narratives from analysis results."""

        category = results["category"]
        region = results["region"]
        monthly = results["monthly"]
        customer = results["customer"]
        product = results["product"]

        narratives = []

        # Category narrative
        category_message = (
            f"{category['highest_sales_category']} leads in sales, "
            f"{category['highest_profit_category']} leads in profit, and "
            f"{category['highest_margin_category']} leads in profit margin."
        )
        narratives.append((
            "Category Performance",
            category_message + " This separates scale from profitability performance."
        ))

        # Region narrative
        region_message = (
            f"{region['highest_sales_region']} leads in sales, "
            f"{region['highest_profit_region']} leads in profit, and "
            f"{region['highest_margin_region']} leads in profit margin."
        )
        narratives.append((
            "Regional Performance",
            region_message + " This separates regional scale from profitability."
        ))

        # Monthly narrative
        narratives.append(
            (
                "Monthly Performance",
                (
                    f"The highest monthly sales occurred in "
                    f"{monthly['highest_sales_month']} with sales of "
                    f"${monthly['highest_sales_value']:,.2f}."
                ),
            )
        )

        narratives.append(
            (
                "Monthly Low Point",
                (
                    f"The lowest monthly sales occurred in "
                    f"{monthly['lowest_sales_month']} with sales of "
                    f"${monthly['lowest_sales_value']:,.2f}. "
                    f"This period represents the lowest observed monthly "
                    f"sales performance in the dataset."
                ),
            )
        )

        # Customer narrative
        narratives.append(
            (
                "Customer Performance",
                (
                    f"{customer['top_customer']} is the top customer by "
                    f"sales, generating ${customer['top_customer_sales']:,.2f} "
                    f"in total sales."
                ),
            )
        )

        # Product narrative
        product_message = (
            f"{product['top_sales_product']} leads in sales at "
            f"${product['top_sales_value']:,.2f}, while "
            f"{product['top_profit_product']} leads in profit at "
            f"${product['top_profit_value']:,.2f}."
        )
        narratives.append(("Product Performance", product_message))

        return narratives

    def generate_contribution_narrative(self, results):
        """Generate narratives from contribution analysis."""

        contribution = results["contribution"]
        profitability = results["profitability"]

        category = contribution["category"]
        region = contribution["region"]

        best_category = category["Sales"].idxmax()
        best_region = region["Sales"].idxmax()

        narratives = []

        narratives.append(
            (
                "Category Contribution",
                (
                    f"{best_category} contributes "
                    f"{category.loc[best_category, 'Sales Contribution']:.2f}% "
                    f"of total sales and "
                    f"{category.loc[best_category, 'Profit Contribution']:.2f}% "
                    f"of total profit, with a profit margin of "
                    f"{category.loc[best_category, 'Profit Margin']:.2f}%."
                ),
            )
        )

        narratives.append(
            (
                "Regional Contribution",
                (
                    f"{best_region} contributes "
                    f"{region.loc[best_region, 'Sales Contribution']:.2f}% "
                    f"of total sales and "
                    f"{region.loc[best_region, 'Profit Contribution']:.2f}% "
                    f"of total profit, with a profit margin of "
                    f"{region.loc[best_region, 'Profit Margin']:.2f}%."
                ),
            )
        )

        narratives.append(
            (
                "Customer Concentration",
                (
                    f"The top 10 customers account for "
                    f"{contribution['top_10_customer_contribution']:.2f}% "
                    f"of total sales, while the top customer alone "
                    f"accounts for "
                    f"{contribution['top_customer_contribution']:.2f}%."
                ),
            )
        )

        narratives.append(
            (
                "Product Concentration",
                (
                    f"The top product accounts for "
                    f"{contribution['top_product_sales_contribution']:.2f}% "
                    f"of total sales and "
                    f"{contribution['top_product_profit_contribution']:.2f}% "
                    f"of total profit."
                ),
            )
        )

        narratives.append(
            (
                "Profitability Risk",
                (
                    f"{profitability['loss_making_product_count']} "
                    f"products generate negative profit. "
                    f"The lowest-margin category is "
                    f"{profitability['lowest_margin_category']}, "
                    f"while the lowest-margin region is "
                    f"{profitability['lowest_margin_region']}."
                ),
            )
        )

        return narratives

    def generate_implications(self, results):
        """Generate business implications and recommendations."""

        category = results["category"]
        region = results["region"]
        monthly = results["monthly"]
        customer = results["customer"]
        product = results["product"]

        implications = []

        # Category implication
        implications.append(
            {
                "area": "Category",
                "finding": (
                    f"{category['highest_sales_category']} leads in sales; "
                    f"{category['highest_profit_category']} leads in profit; "
                    f"{category['highest_margin_category']} leads in profit margin."
                ),
                "implication": (
                    f"The {category['highest_sales_category']} category "
                    "appears to be a key contributor to overall business "
                    "performance."
                ),
                "recommendation": (
                    "Consider maintaining strong product availability "
                    "and evaluating opportunities to expand this category."
                ),
            }
        )

        # Region implication
        implications.append(
            {
                "area": "Region",
                "finding": (
                    f"{region['highest_sales_region']} leads in sales; "
                    f"{region['highest_profit_region']} leads in profit; "
                    f"{region['highest_margin_region']} leads in profit margin."
                ),
                "implication": (
                    f"{region['highest_sales_region']} represents the "
                    "strongest regional performance in the dataset."
                ),
                "recommendation": (
                    "Consider maintaining the current performance level "
                    "while identifying strategies that could be replicated "
                    "in lower-performing regions."
                ),
            }
        )

        # Monthly implication
        implications.append(
            {
                "area": "Monthly Sales",
                "finding": (
                    f"Sales peaked in {monthly['highest_sales_month']} "
                    f"at ${monthly['highest_sales_value']:,.2f}."
                ),
                "implication": (
                    "The peak period may indicate a period of stronger "
                    "customer demand or sales activity."
                ),
                "recommendation": (
                    "Review the characteristics of high-performing periods "
                    "to identify patterns that could support future sales "
                    "planning."
                ),
            }
        )

        # Low month implication
        implications.append(
            {
                "area": "Low Sales Period",
                "finding": (
                    f"Sales reached their lowest point in "
                    f"{monthly['lowest_sales_month']} at "
                    f"${monthly['lowest_sales_value']:,.2f}."
                ),
                "implication": (
                    "The period represents a significant low point in "
                    "monthly sales performance."
                ),
                "recommendation": (
                    "Investigate the factors associated with this period "
                    "before using it as a reference for future sales "
                    "planning."
                ),
            }
        )

        # Customer implication
        implications.append(
            {
                "area": "Customer",
                "finding": (
                    f"{customer['top_customer']} generated "
                    f"${customer['top_customer_sales']:,.2f} "
                    "in sales."
                ),
                "implication": (
                    "The customer represents a high-value contributor "
                    "to sales."
                ),
                "recommendation": (
                    "Consider monitoring high-value customers and "
                    "developing strategies to maintain customer retention."
                ),
            }
        )

        # Product implication
        implications.append(
            {
                "area": "Product",
                "finding": (
                    f"{product['top_sales_product']} generated "
                    f"${product['top_sales_value']:,.2f} in sales, while "
                    f"{product['top_profit_product']} generated "
                    f"${product['top_profit_value']:,.2f} in profit."
                ),
                "implication": (
                    "The same product leads both sales and profitability."
                    if product["top_sales_product"] == product["top_profit_product"]
                    else (
                        "Sales and profit leadership are concentrated in "
                        "different products, so scale and profitability "
                        "should be evaluated separately."
                    )
                ),
                "recommendation": (
                    "Consider monitoring product availability and "
                    "performance while evaluating opportunities to "
                    "maintain its contribution to profitability."
                ),
            }
        )

        return implications

    def run(self):
        """Run complete business insight analysis."""

        logger.info(
            "Starting business insights analysis..."
        )

        df = self.df

        category = self.category_insights(df)
        region = self.region_insights(df)
        monthly = self.monthly_insights(df)
        customer = self.customer_insights(df)
        product = self.product_insights(df)
        contribution = self.contribution_analysis(df)
        profitability = self.profitability_analysis(df)

        results = {
            "category": category,
            "region": region,
            "monthly": monthly,
            "customer": customer,
            "product": product,
            "contribution": contribution,
            "profitability": profitability,
        }

        results["narratives"] = self.generate_narrative(results)
        results["implications"] = self.generate_implications(results)
        results["contribution_narratives"] = (
             self.generate_contribution_narrative(results)
        )

        logger.info(
            "Business insights analysis completed."
        )

        return results