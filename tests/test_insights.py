import pytest

from src.loader import load_dataset
from src.cleaning import DataCleaner
from src.insights import BusinessInsights


def get_insights():
    df = load_dataset("data/raw/superstore.csv")

    cleaner = DataCleaner(
        df,
        "data/processed/superstore_clean.csv",
    )

    cleaned_df = cleaner.run()

    insights = BusinessInsights(cleaned_df)

    return insights.run()


def test_business_insights_run():
    results = get_insights()

    expected_keys = {
        "category",
        "region",
        "monthly",
        "customer",
        "product",
        "contribution",
        "profitability",
        "narratives",
        "implications",
        "contribution_narratives",
    }

    assert set(results.keys()) == expected_keys

def test_business_insights_key_results():
    results = get_insights()

    # Category
    assert results["category"]["highest_sales_category"] == "Technology"
    assert results["category"]["highest_profit_category"] == "Technology"
    assert results["category"]["highest_margin_category"] == "Technology"

    # Region
    assert results["region"]["highest_sales_region"] == "West"
    assert results["region"]["highest_profit_region"] == "West"
    assert results["region"]["highest_margin_region"] == "West"

    # Monthly
    assert str(results["monthly"]["highest_sales_month"]) == "2017-11"
    assert str(results["monthly"]["lowest_sales_month"]) == "2014-02"

    # Customer
    assert results["customer"]["top_customer"] == "Sean Miller"

    # Product
    assert (
        results["product"]["top_sales_product"]
        == "Canon imageCLASS 2200 Advanced Copier"
    )
    assert (
        results["product"]["top_profit_product"]
        == "Canon imageCLASS 2200 Advanced Copier"
    )

    # Profitability
    assert results["profitability"]["lowest_margin_category"] == "Furniture"
    assert results["profitability"]["lowest_margin_region"] == "Central"
    assert results["profitability"]["loss_making_product_count"] == 301

def test_business_insights_key_metrics():
    results = get_insights()

    # Category metrics
    technology = results["category"]["summary"].loc["Technology"]

    assert technology["Sales"] == pytest.approx(836154.0330)
    assert technology["Profit"] == pytest.approx(145454.9481)
    assert technology["Profit Margin"] == pytest.approx(17.395712)

    # Region metrics
    west = results["region"]["summary"].loc["West"]

    assert west["Sales"] == pytest.approx(725457.8245)
    assert west["Profit"] == pytest.approx(108418.4489)
    assert west["Profit Margin"] == pytest.approx(14.944831)

    # Customer
    assert results["customer"]["top_customer_sales"] == pytest.approx(
        25043.05
    )

    # Product
    assert results["product"]["top_sales_value"] == pytest.approx(
        61599.824
    )

    assert results["product"]["top_profit_value"] == pytest.approx(
        25199.928
    )