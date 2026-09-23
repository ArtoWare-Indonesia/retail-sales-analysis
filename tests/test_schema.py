import pandas as pd
import pytest

from src.business_metrics import BusinessMetrics
from src.cleaning import DataCleaner
from src.schema import REQUIRED_CANONICAL_COLUMNS, normalize_dataset


def make_alternate_dataset():
    return pd.DataFrame(
        {
            "OrderNumber": ["O1", "O2"],
            "CustomerNumber": ["C1", "C2"],
            "SKU": ["P1", "P2"],
            "Department": ["Technology", "Furniture"],
            "Territory": ["West", "East"],
            "Buyer": ["Customer A", "Customer B"],
            "Item": ["Product A", "Product B"],
            "PurchaseDate": ["2024-01-01", "2024-01-02"],
            "DeliveryDate": ["2024-01-03", "2024-01-04"],
            "Revenue": [100, 50],
            "NetProfit": [20, 5],
            "Units": [2, 1],
            "PromoRate": [0.1, 0.2],
        }
    )


ALTERNATE_MAPPING = {
    "OrderNumber": "Order ID",
    "CustomerNumber": "Customer ID",
    "SKU": "Product ID",
    "Department": "Category",
    "Territory": "Region",
    "Buyer": "Customer Name",
    "Item": "Product Name",
    "PurchaseDate": "Order Date",
    "DeliveryDate": "Ship Date",
    "Revenue": "Sales",
    "NetProfit": "Profit",
    "Units": "Quantity",
    "PromoRate": "Discount",
}


def test_normalize_dataset_preserves_canonical_schema():
    source = pd.DataFrame({column: [1] for column in REQUIRED_CANONICAL_COLUMNS})
    normalized = normalize_dataset(source)

    assert list(normalized.columns) == list(source.columns)
    assert normalized is not source


def test_normalize_dataset_maps_alternate_schema():
    normalized = normalize_dataset(make_alternate_dataset(), ALTERNATE_MAPPING)

    assert REQUIRED_CANONICAL_COLUMNS <= set(normalized.columns)
    assert list(normalized["Sales"]) == [100, 50]
    assert list(normalized["Profit"]) == [20, 5]


def test_normalize_dataset_rejects_unknown_canonical_target():
    with pytest.raises(ValueError, match="unknown canonical"):
        normalize_dataset(
            make_alternate_dataset(),
            {"Revenue": "Not A Canonical Column"},
        )


def test_alternate_schema_passes_through_analysis_pipeline(tmp_path):
    normalized = normalize_dataset(make_alternate_dataset(), ALTERNATE_MAPPING)

    cleaned = DataCleaner(
        normalized,
        tmp_path / "alternate_clean.csv",
    ).run()

    kpis = BusinessMetrics(cleaned).run()

    assert kpis["total_sales"] == pytest.approx(150)
    assert kpis["total_profit"] == pytest.approx(25)
    assert kpis["total_orders"] == 2
    assert kpis["total_customers"] == 2
    assert kpis["total_products"] == 2
