"""Canonical retail dataset schema and explicit source-column mapping."""

from __future__ import annotations

import pandas as pd


CANONICAL_COLUMNS = {
    "order_id": "Order ID",
    "customer_id": "Customer ID",
    "product_id": "Product ID",
    "category": "Category",
    "region": "Region",
    "customer_name": "Customer Name",
    "product_name": "Product Name",
    "order_date": "Order Date",
    "ship_date": "Ship Date",
    "sales": "Sales",
    "profit": "Profit",
    "quantity": "Quantity",
    "discount": "Discount",
}

REQUIRED_CANONICAL_COLUMNS = set(CANONICAL_COLUMNS.values())


def normalize_dataset(
    df: pd.DataFrame,
    column_mapping: dict[str, str] | None = None,
) -> pd.DataFrame:
    """Map source column names to the canonical retail schema.

    Args:
        df: Source dataset.
        column_mapping: Mapping of source column name -> canonical column name.

    Returns:
        A copy of the dataset using canonical analysis column names.

    Raises:
        ValueError: If the mapping contains unknown targets or creates
            duplicate canonical column names.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame.")

    mapping = column_mapping or {}
    unknown_targets = set(mapping.values()) - REQUIRED_CANONICAL_COLUMNS
    if unknown_targets:
        raise ValueError(
            "Mapping contains unknown canonical columns: "
            + ", ".join(sorted(unknown_targets))
        )

    if len(set(mapping.values())) != len(mapping.values()):
        raise ValueError("Mapping cannot map multiple source columns to one canonical column.")

    missing_sources = set(mapping) - set(df.columns)
    if missing_sources:
        raise ValueError(
            "Mapping contains missing source columns: "
            + ", ".join(sorted(missing_sources))
        )

    normalized = df.rename(columns=mapping).copy()

    duplicate_columns = normalized.columns[
        normalized.columns.duplicated()
    ].tolist()
    if duplicate_columns:
        raise ValueError(
            "Normalization creates duplicate columns: "
            + ", ".join(map(str, duplicate_columns))
        )

    return normalized
