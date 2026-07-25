"""
Dataset loader for Retail Sales Analysis.
"""

from pathlib import Path

import pandas as pd


def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Load a CSV dataset into a pandas DataFrame.

    Args:
        file_path: Path to the CSV dataset.

    Returns:
        pandas.DataFrame: Loaded dataset.

    Raises:
        FileNotFoundError: If the dataset file does not exist.
        ValueError: If the CSV file is empty.
        Exception: For any other errors while reading the CSV.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    try:
        dataframe = pd.read_csv(path)
    except pd.errors.EmptyDataError as exc:
        raise ValueError("The dataset is empty.") from exc
    except Exception as exc:
        raise Exception(f"Failed to load dataset: {exc}") from exc

    return dataframe