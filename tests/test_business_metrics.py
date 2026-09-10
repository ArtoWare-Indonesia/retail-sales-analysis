import pytest
import pandas as pd

from src.business_metrics import BusinessMetrics


def test_business_metrics_calculates_kpis_from_dataframe():
    df = pd.DataFrame({
        "Order ID": ["O1", "O1", "O2"],
        "Customer ID": ["C1", "C1", "C2"],
        "Product ID": ["P1", "P2", "P1"],
        "Sales": [100, 50, 25],
        "Profit": [20, -5, 5],
    })
    result = BusinessMetrics(df).run()
    assert result["total_sales"] == pytest.approx(175)
    assert result["total_profit"] == pytest.approx(20)
    assert result["profit_margin"] == pytest.approx(11.428571)
    assert result["total_orders"] == 2
    assert result["total_customers"] == 2
    assert result["total_products"] == 2


def test_business_metrics_handles_zero_sales():
    df = pd.DataFrame({
        "Sales": [0], "Profit": [0],
        "Order ID": ["O1"], "Customer ID": ["C1"], "Product ID": ["P1"],
    })
    assert BusinessMetrics(df).run()["profit_margin"] == 0
