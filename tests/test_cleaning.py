import pandas as pd

from src.cleaning import DataCleaner


def test_data_cleaner_run_returns_dataframe(tmp_path):
    df = pd.DataFrame(
        {
            "Order Date": ["2017-01-01"],
            "Ship Date": ["2017-01-05"],
            "Sales": [100],
        }
    )

    output_file = tmp_path / "cleaned.csv"

    cleaner = DataCleaner(df, output_file)

    result = cleaner.run()

    assert isinstance(result, pd.DataFrame)

def test_data_cleaner_preserves_row_count(tmp_path):
    df = pd.DataFrame(
        {
            "Order Date": ["2017-01-01", "2017-01-02", "2017-01-03"],
            "Ship Date": ["2017-01-05", "2017-01-06", "2017-01-07"],
            "Sales": [100, 200, 300],
        }
    )

    output_file = tmp_path / "cleaned.csv"

    cleaner = DataCleaner(df, output_file)

    result = cleaner.run()

    assert len(result) == len(df)

def test_data_cleaner_converts_date_columns_to_datetime(tmp_path):
    df = pd.DataFrame(
        {
            "Order Date": ["2017-01-01", "2017-01-02"],
            "Ship Date": ["2017-01-05", "2017-01-06"],
            "Sales": [100, 200],
        }
    )

    output_file = tmp_path / "cleaned.csv"

    cleaner = DataCleaner(df, output_file)

    result = cleaner.run()

    assert pd.api.types.is_datetime64_any_dtype(
        result["Order Date"]
    )

    assert pd.api.types.is_datetime64_any_dtype(
        result["Ship Date"]
    )

def test_data_cleaner_removes_duplicates(tmp_path):
    df = pd.DataFrame(
        {
            "Order Date": [
                "2017-01-01",
                "2017-01-01",
                "2017-01-02",
            ],
            "Ship Date": [
                "2017-01-05",
                "2017-01-05",
                "2017-01-06",
            ],
            "Sales": [100, 100, 200],
        }
    )

    output_file = tmp_path / "cleaned.csv"

    cleaner = DataCleaner(df, output_file)

    result = cleaner.run()

    assert len(result) == 2
    assert result.duplicated().sum() == 0

def test_data_cleaner_creates_output_file(tmp_path):
    df = pd.DataFrame(
        {
            "Order Date": ["2017-01-01"],
            "Ship Date": ["2017-01-05"],
            "Sales": [100],
        }
    )

    output_file = tmp_path / "cleaned.csv"

    cleaner = DataCleaner(df, output_file)

    cleaner.run()

    assert output_file.exists()