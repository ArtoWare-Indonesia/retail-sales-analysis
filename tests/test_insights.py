import pytest
import pandas as pd

from src.loader import load_dataset
from src.cleaning import DataCleaner
from src.insights import BusinessInsights


def get_insights():
    df = load_dataset("data/raw/superstore.csv")
    cleaner = DataCleaner(df, "data/processed/superstore_clean.csv")
    return BusinessInsights(cleaner.run()).run()


def make_df(rows):
    return pd.DataFrame(rows)


def test_business_insights_run():
    results = get_insights()
    expected_keys = {
        "category", "region", "monthly", "customer", "product",
        "contribution", "profitability", "narratives", "implications",
        "contribution_narratives",
    }
    assert set(results.keys()) == expected_keys


def test_business_insights_key_results():
    results = get_insights()
    assert results["category"]["highest_sales_category"] == "Technology"
    assert results["category"]["highest_profit_category"] == "Technology"
    assert results["category"]["highest_margin_category"] == "Technology"
    assert results["region"]["highest_sales_region"] == "West"
    assert results["region"]["highest_profit_region"] == "West"
    assert results["region"]["highest_margin_region"] == "West"
    assert str(results["monthly"]["highest_sales_month"]) == "2017-11"
    assert str(results["monthly"]["lowest_sales_month"]) == "2014-02"
    assert results["customer"]["top_customer"] == "Sean Miller"
    assert results["product"]["top_sales_product"] == "Canon imageCLASS 2200 Advanced Copier"
    assert results["product"]["top_profit_product"] == "Canon imageCLASS 2200 Advanced Copier"
    assert results["profitability"]["lowest_margin_category"] == "Furniture"
    assert results["profitability"]["lowest_margin_region"] == "Central"
    assert results["profitability"]["loss_making_product_count"] == 301


def test_business_insights_key_metrics():
    results = get_insights()
    technology = results["category"]["summary"].loc["Technology"]
    assert technology["Sales"] == pytest.approx(836154.0330)
    assert technology["Profit"] == pytest.approx(145454.9481)
    assert technology["Profit Margin"] == pytest.approx(17.395712)
    west = results["region"]["summary"].loc["West"]
    assert west["Sales"] == pytest.approx(725457.8245)
    assert west["Profit"] == pytest.approx(108418.4489)
    assert west["Profit Margin"] == pytest.approx(14.944831)
    assert results["customer"]["top_customer_sales"] == pytest.approx(25043.05)
    assert results["product"]["top_sales_value"] == pytest.approx(61599.824)
    assert results["product"]["top_profit_value"] == pytest.approx(25199.928)


def test_contribution_analysis_values():
    results = get_insights()["contribution"]
    category = results["category"].loc["Technology"]
    assert category["Sales Contribution"] == pytest.approx(36.4, abs=0.1)
    assert category["Profit Contribution"] == pytest.approx(50.79, abs=0.1)
    assert category["Profit Margin"] == pytest.approx(17.395712)
    assert results["top_customer_contribution"] > 1
    assert results["top_10_customer_contribution"] > results["top_customer_contribution"]
    assert results["top_product_sales_contribution"] > 2
    assert results["top_product_profit_contribution"] > 5


def test_profitability_analysis_values():
    results = get_insights()["profitability"]
    assert results["lowest_margin_category"] == "Furniture"
    assert results["lowest_margin_region"] == "Central"
    assert results["loss_making_product_count"] == len(results["loss_making_products"])
    assert (results["loss_making_products"]["Profit"] < 0).all()


def test_narrative_respects_distinct_category_winners():
    df = make_df([
        {"Category": "A", "Region": "X", "Customer Name": "C1", "Product Name": "P1", "Order Date": "2024-01-01", "Sales": 100, "Profit": 10},
        {"Category": "B", "Region": "X", "Customer Name": "C2", "Product Name": "P2", "Order Date": "2024-01-01", "Sales": 90, "Profit": 30},
        {"Category": "C", "Region": "X", "Customer Name": "C3", "Product Name": "P3", "Order Date": "2024-01-01", "Sales": 20, "Profit": 15},
    ])
    insights = BusinessInsights(df)
    category = insights.category_insights(df)
    results = {"category": category}
    narrative = insights.generate_narrative({
        "category": category,
        "region": {"highest_sales_region": "X", "highest_profit_region": "X", "highest_margin_region": "X"},
        "monthly": {"highest_sales_month": "2024-01", "highest_sales_value": 210, "lowest_sales_month": "2024-01", "lowest_sales_value": 210},
        "customer": {"top_customer": "C1", "top_customer_sales": 100},
        "product": {"top_sales_product": "P1", "top_profit_product": "P2", "top_sales_value": 100, "top_profit_value": 30},
    })
    text = dict(narrative)["Category Performance"]
    assert "A leads in sales" in text
    assert "B leads in profit" in text
    assert "C leads in profit margin" in text


def test_narrative_and_implications_structure():
    results = get_insights()
    assert len(results["narratives"]) == 6
    assert len(results["contribution_narratives"]) == 5
    assert len(results["implications"]) == 6
    for title, text in results["narratives"] + results["contribution_narratives"]:
        assert isinstance(title, str)
        assert isinstance(text, str)
        assert text
    for item in results["implications"]:
        assert set(item) == {"area", "finding", "implication", "recommendation"}
        assert all(item[key] for key in item)
