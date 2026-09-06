from pathlib import Path

from src.loader import load_dataset
from src.cleaning import DataCleaner
from src.insights import BusinessInsights
from src.visualization import Visualizer


def test_full_pipeline(tmp_path):
    # Load raw data
    input_file = Path("data/raw/superstore.csv")
    df = load_dataset(input_file)

    assert not df.empty

    # Cleaning
    cleaned_file = tmp_path / "superstore_clean.csv"
    cleaner = DataCleaner(df, cleaned_file)
    cleaned_df = cleaner.run()

    assert not cleaned_df.empty
    assert cleaned_file.exists()

    # Business insights
    insights = BusinessInsights(cleaned_df)
    results = insights.run()

    assert isinstance(results, dict)
    assert len(results) > 0

    # Visualization
    output_dir = tmp_path / "images"
    visualizer = Visualizer(cleaned_df, output_dir)
    visualizer.run()

    chart_files = list(output_dir.glob("*.png"))

    assert len(chart_files) == 13