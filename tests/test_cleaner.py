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
    # focussed unit test that matches clean_startup_name behavior
    raw = pd.Series([
        "Open Appliances Pvt. Ltd.\n",
        "  HungerBox   \n",
        "Mystifly\n\nLabs",
    ])
    cleaned = raw.apply(clean_startup_name)

    # strips leading/trailing whitespace and newlines
    assert cleaned.iloc[0] == "Open Appliances Pvt. Ltd."
    assert cleaned.iloc[1] == "HungerBox"
    # replaces internal newlines with a space and collapses multiple whitespace
    assert cleaned.iloc[2] == "Mystifly Labs"
    
def test_normalize_industry_edtech_not_saas():
    from transforms.cleaner import normalize_industry
    s = pd.Series(["Edu-tech", "EdTech", "EduTech", "Edu Tech", "Technology Provider", "Tech Provider"])
    out = normalize_industry(s)
    assert out.iloc[0] == "edtech"
    assert out.iloc[1] == "edtech"
    assert out.iloc[2] == "edtech"
    assert out.iloc[3] == "edtech"
    assert out.iloc[4] == "saas_tech"
    assert out.iloc[5] == "saas_tech"

def test_normalize_city():
    from transforms.cleaner import normalize_city
    # representative variants that should collapse to the same canonical city
    raw = pd.Series([
        "Bangalore",
        "Bengaluru",
        "New Delhi",
        "Delhi",
        "Gurgaon",
        "Gurugram",
        "  mumbai  ",
    ])
    out = normalize_city(raw)

    # Bangalore/Bengaluru should normalize to the same canonical, lowercase form
    assert out.iloc[0] == out.iloc[1]
    assert out.iloc[0] == out.iloc[0].lower().strip()

    # New Delhi / Delhi should normalize to the same canonical string
    assert out.iloc[2] == out.iloc[3]

    # Gurgaon / Gurugram should normalize to the same canonical string
    assert out.iloc[4] == out.iloc[5]

    # Mumbai: trimming and case-normalization only
    assert out.iloc[6] == "mumbai"