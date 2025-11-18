# 📊 Indian Startups – Data Cleaning & Transformation Pipeline

A fully reproducible data-cleaning pipeline for the Indian Startup Funding dataset.
Includes standardized cleaning functions, investor extraction, investment type normalization, date parsing, and final cleaned dataset export.

This repo is part of a structured learning project focused on **real-world data wrangling**, **analytics readiness**, and **reproducible pipelines**.

## 🚀 Features

### **Data Cleaning**
- Clean & normalize column names (snake_case)
- Strip whitespace, newlines, and garbage characters
- Normalize missing values across the dataset
- Parse Indian-format dates (DD-MM-YYYY)
- Convert Indian-number-format "Amount" into numeric
- Clean noisy startup names
- Standardize Industry names (EdTech, FinTech, etc.)
- Detect missing dates + year extraction

### **Investor Processing**
- Split multi-investor fields into lists
- Remove noise tokens like `"others"`
- Normalize spacing, punctuation, and Unicode
- Generate investor_count column

### **Investment Type Standardization**
Handles messy variants like:

```
Series A, Series-A, Series J, Pre-series E,
Seed, Seed Funding, Venture Round, Debt Financing,
Equity and Debt, Bridge Funding, Personal Investment
```

Outputs clean canonical values.

## 📁 Project Structure

```
indian-startups-transformations/
│
├── data/
│   ├── startups.csv
│   ├── cleaned_startups.csv
│   └── missing_report.json
│
├── src/
│   └── transforms/
│       ├── cleaner.py
│       └── __init__.py
│
├── notebooks/
│   └── week2_exploration.ipynb
│
├── tests/
│   └── test_cleaner.py
│
├── pyproject.toml
└── README.md
```

## ⚙️ Installation

### Clone the repo
```bash
git clone https://github.com/OlixIgnacious/indian-startups-transformations.git
cd indian-startups-transformations
```

### Install with pip
```bash
pip install -e .
```

### Install dev dependencies (for tests)
```bash
pip install -e ".[dev]"
```

## 🧪 Running Tests
Run tests locally:
```bash
pytest -q
```

## 📘 How to Use the Cleaning Pipeline

```python
import pandas as pd
from transforms.cleaner import (
    clean_column_names,
    normalize_missing_values,
    clean_amount_column,
    parse_dates,
    split_investors,
    canonical_investment_type,
    clean_startup_name
)

df = pd.read_csv("data/startups.csv")

df = clean_column_names(df)
df = normalize_missing_values(df)
df = clean_amount_column(df, col="amount")
df = parse_dates(df, col="date")

df["investors_list"] = split_investors(df["investor"])
df["investor_count"] = df["investors_list"].apply(len)

df["type_clean"] = canonical_investment_type(df["type"])

df.to_csv("data/cleaned_startups.csv", index=False)
```

## 📈 Example Outputs

**Missing Value Summary**
```json
{
  "date": 5,
  "startup": 5,
  "industry": 5,
  "location": 5,
  "investor": 35,
  "type": 12,
  "amount": 57
}
```

## 🧭 Roadmap

- [ ] Add analytics module
- [ ] Create investor co-occurrence graph
- [ ] Add industry canonicalization map
- [ ] Build API endpoint
- [ ] Tableau dashboard

## 📄 License
MIT License.
