import pandas as pd
import pytest

from src.cleaning import DataCleaner


def valid_row():
    return {
        "Order ID": "O1", "Customer ID": "C1", "Product ID": "P1",
        "Category": "Technology", "Region": "West",
        "Customer Name": "Customer A", "Product Name": "Product A",
        "Order Date": "2017-01-01", "Ship Date": "2017-01-05",
        "Sales": 100, "Profit": 20, "Quantity": 2, "Discount": 0.1,
    }


def test_data_cleaner_run_returns_dataframe(tmp_path):
    result = DataCleaner(pd.DataFrame([valid_row()]), tmp_path / "cleaned.csv").run()
    assert isinstance(result, pd.DataFrame)


def test_data_cleaner_preserves_row_count(tmp_path):
    rows = [valid_row() for _ in range(3)]
    for i, row in enumerate(rows): row["Order ID"] = f"O{i}"
    result = DataCleaner(pd.DataFrame(rows), tmp_path / "cleaned.csv").run()
    assert len(result) == 3


def test_data_cleaner_converts_date_columns_to_datetime(tmp_path):
    result = DataCleaner(pd.DataFrame([valid_row()]), tmp_path / "cleaned.csv").run()
    assert pd.api.types.is_datetime64_any_dtype(result["Order Date"])
    assert pd.api.types.is_datetime64_any_dtype(result["Ship Date"])


def test_data_cleaner_removes_duplicates(tmp_path):
    row = valid_row()
    result = DataCleaner(pd.DataFrame([row, row]), tmp_path / "cleaned.csv").run()
    assert len(result) == 1
    assert result.duplicated().sum() == 0


def test_data_cleaner_creates_output_file(tmp_path):
    output_file = tmp_path / "cleaned.csv"
    DataCleaner(pd.DataFrame([valid_row()]), output_file).run()
    assert output_file.exists()


def test_data_cleaner_rejects_invalid_ship_date(tmp_path):
    row = valid_row(); row["Ship Date"] = "2016-12-31"
    with pytest.raises(ValueError, match="Ship Date"):
        DataCleaner(pd.DataFrame([row]), tmp_path / "cleaned.csv").run()


def test_data_cleaner_rejects_invalid_discount(tmp_path):
    row = valid_row(); row["Discount"] = 1.5
    with pytest.raises(ValueError, match="Discount"):
        DataCleaner(pd.DataFrame([row]), tmp_path / "cleaned.csv").run()
