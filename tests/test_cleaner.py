import pandas as pd
from pathlib import Path
from transforms.cleaner import (
    clean_column_names,
    normalize_missing_values,
    clean_amount_column,
    parse_dates,
    date_analysis,
    canonical_investment_type,
    split_investors,
    clean_startup_name,
)

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "starup.csv"

def test_clean_column_names():
    df = pd.read_csv(DATA_PATH)
    cleaned_df = clean_column_names(df)
    assert "date" in cleaned_df.columns
    assert "startup" in cleaned_df.columns

def test_normalize_missing_values():
    df = pd.read_csv(DATA_PATH)
    df = normalize_missing_values(df)
    assert df.isna().sum().sum() > 0

def test_clean_amount_column():
    df = pd.read_csv(DATA_PATH)
    df = clean_amount_column(df, col="Amount")
    assert df["Amount"].dtype == float

def test_parse_dates():
    df = pd.read_csv(DATA_PATH)
    df = parse_dates(df, col="Date")
    assert pd.api.types.is_datetime64_any_dtype(df["Date"])

def test_date_analysis():
    df = pd.read_csv(DATA_PATH)
    df = parse_dates(df, col="Date")
    df = date_analysis(df, date_col="Date")
    assert "year" in df.columns
    assert "date_missing" in df.columns

def test_canonical_investment_type():
    df = pd.read_csv(DATA_PATH)
    df["Type"] = canonical_investment_type(df["Type"])
    assert "other" in df["Type"].values

def test_split_investors():
    df = pd.read_csv(DATA_PATH)
    df = split_investors(df, col="Investor")
    assert "investor_list" in df.columns
    assert "investor_count" in df.columns
    assert isinstance(df["investor_list"].iloc[0], list)

def test_clean_startup_name():
    df = pd.read_csv(DATA_PATH)
    df["Startup"] = df["Startup"].apply(clean_startup_name)
    assert df["Startup"].str.contains(r"\s+", regex=True, na=False).any()
