# Retail Sales Analysis

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Portfolio Release](https://img.shields.io/badge/portfolio-v1.0.0-green)
![Core Application](https://img.shields.io/badge/core--application-v0.6.0-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A Business Intelligence portfolio project that analyzes retail sales data using Python, Pandas, Matplotlib, and Plotly.

The project focuses on data cleaning, exploratory data analysis (EDA), advanced visualization, business metrics, actionable business insights, testing, and interactive visualization.

## Project Overview

This project uses the Superstore retail sales dataset to analyze sales performance, profitability, customer behavior, product performance, and business trends.

The analysis covers:

* Data cleaning and validation
* Feature engineering
* Exploratory Data Analysis (EDA)
* Advanced data visualization
* Business metrics
* Sales performance by category
* Sales performance by region
* Monthly sales trends
* Top customers by sales
* Product sales performance
* Profitability analysis
* Sales and profit relationship
* Interactive sales, regional, monthly, and discount-profit analysis
* Profit margin analysis
* Business insights and conclusions
* Automated analysis pipeline
* Automated testing
* Interactive HTML dashboard

## Release & Versioning

**Portfolio Release:** `v1.0.0 — Portfolio Release`

**Core Application Version:** `v0.6.0 — Interactive Visualization`

The project uses two version references with different scopes:

* **v1.0.0** identifies the finalized portfolio release, including the portfolio notebook, analytical narrative, reproducibility improvements, canonical schema integration, and portfolio-ready evidence.
* **v0.6.0** identifies the reusable core application layer in `src/`, `main.py`, and related application metadata.

This separation is intentional: the `v1.0.0` portfolio release builds on the established `v0.6.0` application architecture without introducing a new application architecture version.

## Features

### Data Processing

* Load retail sales dataset
* Missing value detection
* Duplicate detection and removal
* Data type validation
* Feature engineering
* Export cleaned dataset

### Exploratory Data Analysis

* Sales analysis by category
* Sales analysis by region
* Monthly sales trend analysis
* Top 10 customers analysis
* Top product analysis
* Bottom product analysis
* Profitability analysis
* Business insights generation
* Explicit canonical dataset schema mapping

### Advanced Data Visualization

The visualization pipeline generates analysis charts including:

* Sales and profit contribution
* Region contribution
* Discount vs profit relationship
* Sales performance by category
* Sales performance by region
* Product performance
* Profitability analysis

Visualization figures are exported as PNG files to the `images/` directory. The core application also generates an interactive Plotly HTML dashboard in `output/interactive/`.

### Business Metrics & Insights

The core application includes the dedicated business analysis layer introduced in v0.5.0 and extended with interactive visualization in v0.6.0.

Business metrics and business insights consume the same cleaned DataFrame, keeping the pipeline consistent and easier to test and extend.

The analysis includes metrics such as:

* Total sales
* Total profit
* Profit margin
* Total orders
* Total customers
* Total products
* Sales performance by category
* Profit performance by category
* Regional performance
* Monthly sales performance
* Top customer performance
* Top product performance

### Integrated Analysis Pipeline

The project provides an integrated pipeline through `main.py`:

```text
Raw Dataset
     ↓
Data Cleaning
     ↓
Feature Engineering
     ↓
Business Metrics
     ↓
Business Insights
     ↓
Static Visualization
     ↓
Interactive Visualization
     ↓
Analysis Output
```

### Automated Testing

The project uses `pytest` for automated regression testing.

The test suite covers:

* Data cleaning
* Business insights
* Visualization
* End-to-end pipeline integration
* Dataset schema normalization and reusability

**Current test status: 29 tests passed.**

### Dataset Reusability

The analysis pipeline uses a canonical retail schema defined in `src/schema.py`. Source datasets can be connected through an explicit source-column → canonical-column mapping before entering the cleaning and analysis layers.

This is controlled reusability: datasets are supported when their business fields can be explicitly mapped to the documented canonical schema. The project does not attempt automatic semantic column inference.

The canonical schema currently includes:

* Order ID
* Customer ID
* Product ID
* Category
* Region
* Customer Name
* Product Name
* Order Date
* Ship Date
* Sales
* Profit
* Quantity
* Discount

See `docs/adr/004-dataset-reusability.md` for the architectural decision and implementation contract.

### Continuous Integration

GitHub Actions automatically runs the test suite for:

* Pull requests targeting `main`
* Pushes to `main`

The workflow uses Python 3.12, installs dependencies from `requirements.txt`, and runs:

```bash
python -m pytest -q
```

See `docs/adr/002-automated-ci-test-workflow.md` for the CI decision record.

## Project Structure

```text
retail-sales-analysis/
├── data/
│   ├── raw/
│   │   └── superstore.csv
│   └── processed/
│       └── superstore_clean.csv
├── docs/
│   └── adr/
├── images/
├── notebooks/
├── output/
│   └── interactive/
├── src/
│   ├── business_metrics.py
│   ├── cleaning.py
│   ├── insights.py
│   ├── interactive_visualization.py
│   ├── loader.py
│   ├── schema.py
│   ├── visualization.py
│   └── utils/
│       └── logger.py
├── tests/
│   ├── test_business_metrics.py
│   ├── test_cleaning.py
│   ├── test_insights.py
│   ├── test_pipeline.py
│   ├── test_schema.py
│   └── test_visualization.py
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

## Requirements

* Python 3.12+
* pandas
* matplotlib
* openpyxl
* plotly
* pytest

Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

### Run the Project

From the project root directory:

```bash
python main.py
```

The main pipeline runs the data processing, business analysis, and visualization workflow.

### Run Tests

Run the complete test suite with:

```bash
python -m pytest -q
```

The repository baseline currently passes 29 tests.

### Portfolio Notebook

The finalized portfolio notebook is:

```text
notebooks/Retail_Sales_Analysis.ipynb
```

The notebook is the **portfolio storytelling layer**. It presents the analysis as a reproducible business narrative covering data quality, preparation, KPIs, business analysis, visual evidence, implications, and the interactive dashboard reference.

The notebook identifies itself as **v1.0.0 portfolio notebook** and uses the reusable `src/` application layers rather than duplicating the underlying analysis logic.

## Analysis Workflow

```text
Load Dataset
     ↓
Data Cleaning
     ↓
Feature Engineering
     ↓
Exploratory Data Analysis
     ↓
Business Metrics
     ↓
Business Insights
     ↓
Advanced Data Visualization
     ↓
Interactive Visualization
     ↓
Export Results
```

## Analysis Output

The project generates:

* Cleaned retail sales dataset
* Business metrics
* Business insights
* Sales and profit analysis
* Regional analysis
* Product performance analysis
* Customer performance analysis
* Profitability analysis
* Visualization figures in PNG format
* Interactive HTML dashboard

## Milestones

### Core Application Milestones

* ✅ v0.1.0 — Project Setup
* ✅ v0.2.0 — Data Cleaning
* ✅ v0.3.0 — Exploratory Data Analysis (EDA)
* ✅ v0.4.0 — Advanced Data Visualization
* ✅ v0.5.0 — Business Insights & Tested Analysis Pipeline
* ✅ v0.6.0 — Interactive Visualization

### Portfolio Milestone

* ✅ v1.0.0 — Portfolio Release

The v1.0.0 portfolio milestone finalizes the analytical presentation layer and reproducible portfolio narrative on top of the v0.6.0 core application.

### Future Development

The ADR-004 controlled reusability boundary is implemented. Future work may extend reuse through additional explicit schema adapters or broader dataset coverage, while automatic semantic inference remains outside the project's current scope.

## Architecture Decisions

Repository-level architectural and process decisions are documented in `docs/adr/`:

* ADR-001 — Internal Deduplication Refactor for `BusinessInsights`
* ADR-002 — Automated CI Test Workflow
* ADR-003 — Repository Documentation & Version Consistency
* ADR-004 — Dataset Reusability / Generic Schema Abstraction

## License

This project is licensed under the MIT License.
