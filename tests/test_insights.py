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


def test_category_summary_calculates_margin_from_aggregated_totals():
    df = make_df([
        {"Category": "A", "Region": "X", "Customer Name": "C1", "Product Name": "P1", "Order Date": "2024-01-01", "Sales": 100, "Profit": 10},
        {"Category": "A", "Region": "X", "Customer Name": "C2", "Product Name": "P2", "Order Date": "2024-01-01", "Sales": 300, "Profit": 90},
        {"Category": "B", "Region": "Y", "Customer Name": "C3", "Product Name": "P3", "Order Date": "2024-01-01", "Sales": 100, "Profit": 20},
    ])
    summary = BusinessInsights(df).category_insights(df)["summary"]
    assert summary.loc["A", "Sales"] == pytest.approx(400)
    assert summary.loc["A", "Profit"] == pytest.approx(100)
    assert summary.loc["A", "Profit Margin"] == pytest.approx(25)


def test_customer_concentration_uses_top_ten_customers():
    rows = [
        {"Category": "A", "Region": "X", "Customer Name": f"C{i}", "Product Name": f"P{i}", "Order Date": "2024-01-01", "Sales": 100 - i, "Profit": 10}
        for i in range(12)
    ]
    df = make_df(rows)
    result = BusinessInsights(df).run()["contribution"]
    assert result["top_customer_contribution"] == pytest.approx(100 / sum(100 - i for i in range(12)) * 100)
    assert result["top_10_customer_contribution"] == pytest.approx(sum(100 - i for i in range(10)) / sum(100 - i for i in range(12)) * 100)


def test_loss_making_products_excludes_zero_profit_products():
    df = make_df([
        {"Category": "A", "Region": "X", "Customer Name": "C1", "Product Name": "Loss", "Order Date": "2024-01-01", "Sales": 100, "Profit": -20},
        {"Category": "A", "Region": "X", "Customer Name": "C2", "Product Name": "BreakEven", "Order Date": "2024-01-01", "Sales": 100, "Profit": 0},
        {"Category": "A", "Region": "X", "Customer Name": "C3", "Product Name": "Profit", "Order Date": "2024-01-01", "Sales": 100, "Profit": 30},
    ])
    result = BusinessInsights(df).run()["profitability"]
    assert result["loss_making_product_count"] == 1
    assert list(result["loss_making_products"].index) == ["Loss"]


def test_product_narrative_keeps_sales_and_profit_values_with_their_leaders():
    df = make_df([
        {"Category": "A", "Region": "X", "Customer Name": "C1", "Product Name": "Sales Leader", "Order Date": "2024-01-01", "Sales": 100, "Profit": 10},
        {"Category": "A", "Region": "X", "Customer Name": "C2", "Product Name": "Profit Leader", "Order Date": "2024-01-01", "Sales": 50, "Profit": 40},
    ])
    insights = BusinessInsights(df)
    product = insights.product_insights(df)
    narrative = dict(insights.generate_narrative({
        "category": {"highest_sales_category": "A", "highest_profit_category": "A", "highest_margin_category": "A"},
        "region": {"highest_sales_region": "X", "highest_profit_region": "X", "highest_margin_region": "X"},
        "monthly": {"highest_sales_month": "2024-01", "highest_sales_value": 150, "lowest_sales_month": "2024-01", "lowest_sales_value": 150},
        "customer": {"top_customer": "C1", "top_customer_sales": 100},
        "product": product,
    }))["Product Performance"]
    assert "Sales Leader leads in sales at $100.00" in narrative
    assert "Profit Leader leads in profit at $40.00" in narrative
    assert "Sales Leader leads in profit" not in narrative


def test_product_implication_keeps_sales_and_profit_leaders_distinct():
    df = make_df([
        {"Category": "A", "Region": "X", "Customer Name": "C1", "Product Name": "Sales Leader", "Order Date": "2024-01-01", "Sales": 100, "Profit": 10},
        {"Category": "A", "Region": "X", "Customer Name": "C2", "Product Name": "Profit Leader", "Order Date": "2024-01-01", "Sales": 50, "Profit": 40},
    ])
    insights = BusinessInsights(df)
    product = insights.product_insights(df)
    implication = next(item for item in insights.generate_implications({
        "category": {"highest_sales_category": "A", "highest_profit_category": "A", "highest_margin_category": "A"},
        "region": {"highest_sales_region": "X", "highest_profit_region": "X", "highest_margin_region": "X"},
        "monthly": {"highest_sales_month": "2024-01", "highest_sales_value": 150, "lowest_sales_month": "2024-01", "lowest_sales_value": 150},
        "customer": {"top_customer": "C1", "top_customer_sales": 100},
        "product": product,
    }) if item["area"] == "Product")
    assert "Sales Leader generated $100.00 in sales" in implication["finding"]
    assert "Profit Leader generated $40.00 in profit" in implication["finding"]


def test_business_insights_rejects_missing_required_columns():
    df = make_df([{"Category": "A", "Region": "X", "Sales": 100, "Profit": 20}])
    with pytest.raises(ValueError, match="Missing required columns"):
        BusinessInsights(df)


def test_business_insights_handles_zero_sales_margin():
    df = make_df([
        {"Category": "A", "Region": "X", "Customer Name": "C1", "Product Name": "P1", "Order Date": "2024-01-01", "Sales": 0, "Profit": 0},
    ])
    results = BusinessInsights(df).run()
    assert results["category"]["summary"].loc["A", "Profit Margin"] == 0
    assert results["region"]["summary"].loc["X", "Profit Margin"] == 0
    assert results["contribution"]["top_customer_contribution"] == 0
    assert results["contribution"]["top_product_sales_contribution"] == 0
    assert results["contribution"]["top_product_profit_contribution"] == 0


def test_business_insights_handles_single_group():
    df = make_df([
        {"Category": "A", "Region": "X", "Customer Name": "C1", "Product Name": "P1", "Order Date": "2024-01-01", "Sales": 100, "Profit": 20},
    ])
    results = BusinessInsights(df).run()
    assert results["category"]["highest_sales_category"] == "A"
    assert results["region"]["highest_margin_region"] == "X"
    assert results["customer"]["top_customer"] == "C1"
    assert results["product"]["top_sales_product"] == "P1"
    assert results["product"]["top_profit_product"] == "P1"
    assert results["contribution"]["top_customer_contribution"] == pytest.approx(100)
    assert results["contribution"]["top_10_customer_contribution"] == pytest.approx(100)


def test_business_insights_handles_tied_winners_deterministically():
    df = make_df([
        {"Category": "A", "Region": "X", "Customer Name": "C1", "Product Name": "P1", "Order Date": "2024-01-01", "Sales": 100, "Profit": 20},
        {"Category": "B", "Region": "Y", "Customer Name": "C2", "Product Name": "P2", "Order Date": "2024-01-01", "Sales": 100, "Profit": 20},
    ])
    results = BusinessInsights(df).run()
    assert results["category"]["highest_sales_category"] == "A"
    assert results["category"]["highest_profit_category"] == "A"
    assert results["region"]["highest_sales_region"] == "X"
    assert results["product"]["top_sales_product"] == "P1"
    assert results["product"]["top_profit_product"] == "P1"


def test_profitability_analysis_exposes_total_loss():
    df = make_df([
        {"Category": "A", "Region": "X", "Customer Name": "C1", "Product Name": "Loss A", "Order Date": "2024-01-01", "Sales": 100, "Profit": -20},
        {"Category": "A", "Region": "X", "Customer Name": "C2", "Product Name": "Loss B", "Order Date": "2024-01-01", "Sales": 50, "Profit": -5},
        {"Category": "A", "Region": "X", "Customer Name": "C3", "Product Name": "Profit", "Order Date": "2024-01-01", "Sales": 200, "Profit": 40},
    ])
    results = BusinessInsights(df).run()["profitability"]
    assert results["loss_making_product_count"] == 2
    assert results["total_loss"] == pytest.approx(-25)
