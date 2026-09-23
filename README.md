# Retail Sales Analysis

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Version](https://img.shields.io/badge/version-v0.6.0-green)
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

### Advanced Data Visualization

The visualization pipeline generates analysis charts including:

* Sales and profit contribution
* Region contribution
* Discount vs profit relationship
* Sales performance by category
* Sales performance by region
* Product performance
* Profitability analysis

Visualization figures are exported as PNG files to the `images/` directory. Version 0.6.0 also generates an interactive Plotly HTML dashboard in `output/interactive/`.

### Business Metrics & Insights

Version 0.6.0 includes the dedicated business analysis layer introduced in v0.5.0 and extends it with interactive visualization.

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

**Current test status: 25 tests passed.**

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
│   ├── visualization.py
│   └── utils/
│       └── logger.py
├── tests/
│   ├── test_business_metrics.py
│   ├── test_cleaning.py
│   ├── test_insights.py
│   ├── test_pipeline.py
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

The repository baseline currently passes 25 tests.

### Jupyter Notebook

The exploratory analysis can also be viewed in:

```text
notebooks/retail_sales_analysis.ipynb
```

The notebook contains the EDA process, visualizations, and interpretation of the analysis results.

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

## Current Version

**v0.6.0 — Interactive Visualization**

The v0.6.0 release extends the structured Business Intelligence pipeline with interactive Plotly visualization.

### Implemented

* Project setup
* Data loading
* Data cleaning pipeline
* Missing value detection
* Duplicate detection and removal
* Data type validation
* Feature engineering
* Exploratory Data Analysis (EDA)
* Sales analysis by category
* Sales analysis by region
* Monthly sales trend analysis
* Top 10 customer analysis
* Top product analysis
* Bottom product analysis
* Profitability analysis
* Advanced data visualization
* Business metrics module
* Business insights module
* Integrated analysis pipeline
* Configurable application settings
* Centralized logging
* Automated chart generation
* Export cleaned dataset
* Export visualization images
* Automated test suite
* Unit tests for cleaning
* Unit tests for insights
* Unit tests for visualization
* Business metrics tests
* End-to-end pipeline integration test
* Interactive Plotly HTML dashboard
* GitHub Actions test workflow

## Roadmap

* ✅ v0.1.0 — Project Setup
* ✅ v0.2.0 — Data Cleaning
* ✅ v0.3.0 — Exploratory Data Analysis (EDA)
* ✅ v0.4.0 — Advanced Data Visualization
* ✅ v0.5.0 — Business Insights & Tested Analysis Pipeline
* ✅ v0.6.0 — Interactive Visualization
* ⏳ v1.0.0 — Portfolio Release

### Future Development

The next development phase will focus on portfolio readiness, presentation quality, and broader dataset reusability. Dataset reusability and generic-schema abstraction are intentionally tracked separately from the v0.6.0 baseline.

## Architecture Decisions

Repository-level architectural and process decisions are documented in `docs/adr/`:

* ADR-001 — Internal Deduplication Refactor for `BusinessInsights`
* ADR-002 — Automated CI Test Workflow
* ADR-003 — Repository Documentation & Version Consistency

## License

This project is licensed under the MIT License.
