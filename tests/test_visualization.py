import pandas as pd
import matplotlib.pyplot as plt

from src.visualization import Visualizer


def test_visualizer_can_be_created(tmp_path):
    df = pd.DataFrame(
        {
            "Category": ["Technology"],
            "Region": ["West"],
            "Sales": [100],
            "Profit": [20],
        }
    )

    output_dir = tmp_path / "images"

    visualizer = Visualizer(df, output_dir)

    assert isinstance(visualizer, Visualizer)

def test_visualizer_creates_output_directory(tmp_path):
    df = pd.DataFrame(
        {
            "Category": ["Technology"],
            "Region": ["West"],
            "Sales": [100],
            "Profit": [20],
        }
    )

    output_dir = tmp_path / "charts"

    Visualizer(df, output_dir)

    assert output_dir.exists()
    assert output_dir.is_dir()

def test_save_plot_creates_image_file(tmp_path):
    df = pd.DataFrame(
        {
            "Category": ["Technology"],
            "Sales": [100],
        }
    )

    output_dir = tmp_path / "images"
    visualizer = Visualizer(df, output_dir)

    plt.figure()
    plt.plot([1, 2, 3], [1, 2, 3])

    visualizer.save_plot("test_plot.png")

    output_file = output_dir / "test_plot.png"

    assert output_file.exists()
    assert output_file.stat().st_size > 0

def test_visualizer_run_generates_all_charts(tmp_path):
    df = pd.DataFrame(
        {
            "Customer Name": ["Customer A", "Customer B", "Customer C"],
            "Product Name": ["Product A", "Product B", "Product C"],
            "Category": ["Technology", "Furniture", "Office Supplies"],
            "Region": ["West", "East", "Central"],
            "Order Date": pd.to_datetime(
                ["2023-01-01", "2023-02-01", "2023-03-01"]
            ),
            "Sales": [1000, 800, 600],
            "Profit": [200, 100, 50],
            "Discount": [0.1, 0.2, 0.3],
        }
    )

    output_dir = tmp_path / "images"

    visualizer = Visualizer(df, output_dir)

    visualizer.run()

    expected_charts = [
        "sales_by_category.png",
        "sales_by_region.png",
        "monthly_sales_trend.png",
        "top_10_customers.png",
        "top_products.png",
        "bottom_products.png",
        "profit_by_category.png",
        "sales_vs_profit.png",
        "discount_vs_profit.png",
        "sales_profit_contribution.png",
        "region_contribution.png",
        "profit_margin_by_category.png",
        "sales_profit_by_region.png",
    ]

    for chart in expected_charts:
        assert (output_dir / chart).exists()

def test_visualizer_run_creates_expected_number_of_charts(tmp_path):
    df = pd.DataFrame(
        {
            "Customer Name": ["Customer A", "Customer B", "Customer C"],
            "Product Name": ["Product A", "Product B", "Product C"],
            "Category": ["Technology", "Furniture", "Office Supplies"],
            "Region": ["West", "East", "Central"],
            "Order Date": pd.to_datetime(
                ["2023-01-01", "2023-02-01", "2023-03-01"]
            ),
            "Sales": [1000, 800, 600],
            "Profit": [200, 100, 50],
            "Discount": [0.1, 0.2, 0.3],
        }
    )

    output_dir = tmp_path / "images"

    visualizer = Visualizer(df, output_dir)
    visualizer.run()

    chart_files = list(output_dir.glob("*.png"))

    assert len(chart_files) == 13

def test_interactive_visualizer_creates_dashboard(tmp_path):
    from src.interactive_visualization import InteractiveVisualizer
    from src.business_metrics import BusinessMetrics

    df = pd.DataFrame(
        {
            "Order ID": ["O1", "O2", "O3"],
            "Customer ID": ["C1", "C2", "C3"],
            "Product ID": ["P1", "P2", "P3"],
            "Customer Name": ["Customer A", "Customer B", "Customer C"],
            "Product Name": ["Product A", "Product B", "Product C"],
            "Category": ["Technology", "Furniture", "Office Supplies"],
            "Region": ["West", "East", "Central"],
            "Order Date": pd.to_datetime(["2023-01-01", "2023-02-01", "2023-03-01"]),
            "Ship Date": pd.to_datetime(["2023-01-03", "2023-02-03", "2023-03-03"]),
            "Sales": [1000, 800, 600],
            "Profit": [200, 100, 50],
            "Quantity": [2, 3, 4],
            "Discount": [0.1, 0.2, 0.3],
        }
    )
    output_dir = tmp_path / "interactive"
    output = InteractiveVisualizer(df, output_dir).run(BusinessMetrics(df).run())
    assert output.exists()
    assert output.suffix == ".html"
    assert output.stat().st_size > 0
