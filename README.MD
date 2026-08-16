# Retail Sales Analysis

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Version](https://img.shields.io/badge/version-v0.3.0-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A Business Intelligence portfolio project that analyzes retail sales data using Python, Pandas, and Matplotlib.

The project focuses on data cleaning, exploratory data analysis (EDA), data visualization, and generating business insights from retail sales data.

## Project Overview

This project uses the Superstore retail sales dataset to analyze sales performance and identify useful business insights.

The analysis covers:

* Data cleaning and validation
* Feature engineering
* Exploratory Data Analysis (EDA)
* Sales performance by category
* Sales performance by region
* Monthly sales trends
* Top customers by sales
* Product profitability analysis
* Business insights and conclusions
* Data visualization with Matplotlib

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
* Most profitable products analysis
* Least profitable products analysis
* Business insights generation

### Visualization

* Sales by category
* Sales by region
* Monthly sales trend
* Top 10 customers
* Product profitability
* Export visualization figures as image files

### Project Structure

* Modular Python project structure
* Configurable application settings
* Logging with Python's `logging` module

## Project Structure

```text
retail-sales-analysis/
├── data/
│   ├── raw/
│   │   └── superstore.csv
│   └── processed/
│       └── superstore_clean.csv
├── images/
│   ├── sales_category.png
│   ├── sales_region.png
│   ├── monthly_sales.png
│   ├── top_customers.png
│   └── profit_products.png
├── notebooks/
│   └── retail_sales_analysis.ipynb
├── src/
│   ├── loader.py
│   ├── cleaning.py
│   └── utils/
│       └── logger.py
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

## Requirements

* Python 3.13+
* pandas
* matplotlib
* openpyxl

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Run the Project

From the project root directory:

```bash
python main.py
```

The application performs the following workflow:

```text
Load Dataset
     ↓
Data Cleaning
     ↓
Feature Engineering
     ↓
Exploratory Data Analysis
     ↓
Data Visualization
     ↓
Business Insights
     ↓
Export Results
```

### Jupyter Notebook

The complete exploratory analysis can also be viewed in:

```text
notebooks/retail_sales_analysis.ipynb
```

The notebook contains the EDA process, visualizations, and interpretation of the analysis results.

## Analysis Output

The project generates:

* Cleaned retail sales dataset
* Sales analysis by category
* Sales analysis by region
* Monthly sales trend
* Top 10 customers
* Product profitability analysis
* Visualization figures in PNG format
* Business insights based on the analysis

## Current Version

**v0.3.0 — Exploratory Data Analysis (EDA)**

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
* Top customer analysis
* Product profitability analysis
* Business insights
* Data visualization with Matplotlib
* Export cleaned dataset
* Export visualization images
* Modular project structure
* Configurable application settings
* Logging with Python logging module

## Roadmap

* ✅ **v0.1.0** — Project Setup
* ✅ **v0.2.0** — Data Cleaning
* ✅ **v0.3.0** — Exploratory Data Analysis (EDA)
* ⏳ **v0.4.0** — Advanced Data Visualization
* ⏳ **v0.5.0** — Dashboard & Business Insights
* ⏳ **v0.6.0** — Interactive Visualization
* ⏳ **v1.0.0** — Portfolio Release

## License

This project is licensed under the MIT License.
