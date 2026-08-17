# Retail Sales Analysis

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Version](https://img.shields.io/badge/version-v0.4.0-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A Business Intelligence portfolio project that analyzes retail sales data using Python, Pandas, and Matplotlib.

The project focuses on data cleaning, exploratory data analysis (EDA), advanced data visualization, and generating business insights from retail sales data.

## Project Overview

This project uses the Superstore retail sales dataset to analyze sales performance, profitability, and business trends.

The analysis covers:

* Data cleaning and validation
* Feature engineering
* Exploratory Data Analysis (EDA)
* Advanced data visualization
* Sales performance by category
* Sales performance by region
* Monthly sales trends
* Top customers by sales
* Product sales performance
* Profitability analysis
* Sales and profit relationship
* Profit margin analysis
* Business insights and conclusions

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

* Sales by category
* Sales by region
* Monthly sales trend
* Top 10 customers
* Top 10 products
* Bottom 10 products
* Profit by category
* Sales vs Profit
* Sales vs Profit by Category
* Profit Margin by Category
* Sales & Profit by Region
* Chart annotations for key values
* Improved chart readability and presentation
* Export visualization figures as PNG files

### Project Structure

* Modular Python project structure
* Configurable application settings
* Centralized logging
* Reusable visualization pipeline
* Automated chart generation

## Project Structure

```text
retail-sales-analysis/
├── data/
│   ├── raw/
│   │   └── superstore.csv
│   └── processed/
│       └── superstore_clean.csv
├── images/
│   ├── sales_by_category.png
│   ├── sales_by_region.png
│   ├── monthly_sales_trend.png
│   ├── top_10_customers.png
│   ├── top_products.png
│   ├── bottom_products.png
│   ├── profit_by_category.png
│   ├── sales_vs_profit.png
│   ├── profit_margin_by_category.png
│   └── sales_profit_by_region.png
├── notebooks/
│   └── retail_sales_analysis.ipynb
├── src/
│   ├── loader.py
│   ├── cleaning.py
│   ├── visualization.py
│   └── utils/
│       └── logger.py
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

##Requirements

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
### Run Visualization Pipeline

The visualization module can be executed from the project root using:

```bash
python -m src.visualization
```

The visualization pipeline loads the cleaned dataset and automatically generates the analysis charts in the images/ directory.

### Jupyter Notebook

The complete exploratory analysis can also be viewed in:

```text
notebooks/retail_sales_analysis.ipynb
```

The notebook contains the EDA process, visualizations, and interpretation of the analysis results.

### Analysis Workflow

```text
Load Dataset
     ↓
Data Cleaning
     ↓
Feature Engineering
     ↓
Exploratory Data Analysis
     ↓
Advanced Data Visualization
     ↓
Business Insights
     ↓
Export Results
```

### Analysis Output

The project generates:

* Cleaned retail sales dataset
* Sales analysis by category
* Sales analysis by region
* Monthly sales trend
* Top 10 customers
* Top and bottom products
* Profit analysis
* Sales vs Profit analysis
* Profit margin analysis
* Sales & Profit by Region analysis
* Visualization figures in PNG format
* Business insights based on the analysis

### Current Version

v0.4.0 — Advanced Data Visualization

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
* Profit by category analysis
* Sales vs Profit analysis
* Sales vs Profit by Category analysis
* Profit Margin by Category analysis
* Sales & Profit by Region analysis
* Advanced chart formatting
* Chart annotations
* Data visualization with Matplotlib
* Export cleaned dataset
* Export visualization images
* Modular project structure
* Configurable application settings
* Logging with Python logging module

### Roadmap

* ✅ v0.1.0 — Project Setup
* ✅ v0.2.0 — Data Cleaning
* ✅ v0.3.0 — Exploratory Data Analysis (EDA)
* ✅ v0.4.0 — Advanced Data Visualization
* ⏳ v0.5.0 — Dashboard & Business Insights
* ⏳ v0.6.0 — Interactive Visualization
* ⏳ v1.0.0 — Portfolio Release

### License

This project is licensed under the MIT License.
