# Retail Sales Analysis

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Version](https://img.shields.io/badge/version-v0.2.0-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A Business Intelligence portfolio project that analyzes retail sales data using Python and Pandas.


## New Features

- Load retail sales dataset
- Data cleaning pipeline
- Missing value detection
- Duplicate detection and removal
- Data type validation
- Export cleaned dataset

## Features

- Modular project structure
- Configurable application settings
- Logging with Python logging module

## Project Structure

```
retail-sales-analysis/
├── data/
|   ├── raw/
│   └── processed
|   
├── output/
├── src/
│   ├── loader.py
|   ├── cleaning.py
│   └── utils/
│       └── logger.py
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.13+
- pandas
- openpyxl

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
python src/cleaning.py
```
Output:

- Detect missing values
- Detect duplicate rows
- Validate data types
- Export cleaned dataset to `data/processed/`
```

## Current Version

**v0.2.0**

### Features

- Load retail sales dataset
- Data cleaning pipeline
- Missing value detection
- Duplicate detection and removal
- Data type validation
- Export cleaned dataset
- Modular project structure
- Configurable application settings
- Logging with Python logging module

## Roadmap

- ✅ v0.1.0 - Project setup
- ✅ v0.2.0 - Data Cleaning
- ⏳ v0.3.0 - Exploratory Data Analysis (EDA)
- ⏳ v0.4.0 - Data Visualization
- ⏳ v0.5.0 - Dashboard & Insights
- ⏳ v0.6.0 – Visualization
- ⏳ v1.0.0 – Portfolio Release

## License

This project is licensed under the MIT License.