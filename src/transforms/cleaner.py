import pandas as pd
from typing import Any
import re

CANONICAL_PATTERNS = {
    r"^angel.*": "angel",
    r".*angel funding.*": "angel",
    r"^seed.*": "seed",
    r".*seed funding.*": "seed",
    r".*seed / angel.*": "seed",
    r"^pre[\s\-]?seed.*": "pre_seed",
    r"^pre[\s\-]?series a.*": "pre_seed",   # or "pre_series_a"
    r"^series [a-z0-9].*": "series",
    r".*venture.*": "venture",
    r".*private equity.*": "private_equity",
    r".*debt.*": "debt",
    r".*equity.*": "equity",
    r".*mezzanine.*": "mezzanine",
    r".*m&a.*": "ma",
    r".*bridge.*": "bridge",
    r".*secondary market.*": "secondary_market",
    r".*in progress.*": "in_progress",
    r".*unspecified.*": "unspecified",
}

SPLIT_PATTERN = r",\s*|;\s*|/\s*|\s+and\s+|\s+AND\s+|\n+"

SUFFIX_PATTERN = r"""
    \s+(
        pvt\.?\s*ltd      |   # Pvt Ltd / Pvt. Ltd
        private\s*limited |   # Private Limited
        ltd\.?            |   # Ltd / Ltd.
        limited           |   # Limited
        inc\.?            |   # Inc / Inc.
        incorporated      |
        corp\.?           |
        corporation
    )\s*$
"""   
INDUSTRY_PATTERNS_ORDERED = [
    (r"\bed[\s\-]?tech\b", "edtech"),
    (r"\b(edutech|edutech|edu tech)\b", "edtech"),  # extra safety
    (r"\bfin[\s\-]?tech\b|\bfinancial\b|\bfinance\b", "fintech"),
    (r"\bb2b[\s\-]?e[\s\-]?commerce\b|\be[\s\-]?commerce\b", "ecommerce"),
    # SaaS/Tech must be specific: match 'saas' or 'technology provider' or 'tech provider' NOT bare 'tech'
    (r"\bsaas\b|\btechnology\s*provider\b|\btech\s*provider\b", "saas_tech"),
    (r"\bfood\b|\bbeverage\b", "food_beverage"),
    (r"\bagri[\s\-]?tech\b|\bagritech\b", "agritech"),
    (r"\bhealth\b", "healthtech"),
    (r"\btransport(ation)?\b", "transport"),
    (r"\blifestyle\b", "lifestyle"),
    (r"\bhospital\b|\bhospitality\b", "hospitality"),
    (r"\badvertis", "advertising"),
    (r"\bdigital\b", "digital"),
    (r"\bdairy\b", "dairytech"),
    (r"\bsupply\s*chain\b", "supply_chain"),
] 

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    def _snake_case(s: Any) -> str:
        if not isinstance(s, str):
            s = str(s)
        s  = s.strip()
        s = s.replace(" ", "_")
        s = re.sub(r"[^\w\s]", "", s)  
        return s.lower()
    df =  df.copy()
    df.columns = [_snake_case(col) for col in df.columns]
    return df

def normalize_missing_values(df):
    df = df.copy()
    # normalize common textual tokens (case-insensitive)
    df = df.replace(r'(?i)^(n/?a|na|none|null|undisclosed|unknown)$', pd.NA, regex=True)
    # blank-only → NA
    df = df.replace(r'^\s*$', pd.NA, regex=True)
    return df

def clean_amount_column(df: pd.DataFrame, col: str = "amount") -> pd.DataFrame:
    df = df.copy()
    # handle missing and raw strings first
    series = df[col].fillna("").astype(str).str.strip()
    series = series.replace(r"(?i)undisclosed", "", regex=True)  # remove case-insensitive 'Undisclosed'
    series = series.str.replace(r"[^0-9\.\-]", "", regex=True)
    series = series.replace("", pd.NA)
    df[col] = pd.to_numeric(series, errors="coerce")
    return df

def parse_dates(df: pd.DataFrame, col: str = "date") -> pd.DataFrame:
    df = df.copy()
    df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce') 
    return df

def date_analysis(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    df = df.copy()
    df["year"] = df[date_col].dt.year
    df["date_missing"] = df[date_col].isna()
    return df

def canonical_investment_type(s: pd.Series) -> pd.Series:
    s = s.astype(str).str.lower().str.strip()
    out = s.replace(CANONICAL_PATTERNS, regex=True)
    out = out.where(out.isin(set(CANONICAL_PATTERNS.values())), other="other")
    return out

def split_investors(df: pd.DataFrame, col: str = "investor") -> pd.DataFrame:
    out = df.copy()
    if col not in out.columns:
        out["investor_list"]  = [[] for _ in range(len(out))]
        out["investor_count"] = 0
        return out

    # ensure we handle missing values BEFORE casting to str
    series = out[col].where(out[col].notna(), "")
    series = series.astype(str).str.strip()
    split_pattern = r",\s*|;\s*|/\s*|\s+and\s+|\s+AND\s+|\n+"
    out["investor_list"] = series.str.split(split_pattern)

    # clean each list: strip, drop empty, drop 'others'
    def clean_list(lst):
        return [x.strip() for x in lst if x and x.strip() and x.strip().lower() != "others"]

    out["investor_list"] = out["investor_list"].apply(clean_list)
    out["investor_count"] = out["investor_list"].apply(len)
    return out

def clean_startup_name(name: str) -> str:
    if not isinstance(name, str):
        return name
    s = name.strip().replace("\n", " ")
    s = re.sub(r"\s+", " ", s)
    return s

def normalize_industry(series: pd.Series) -> pd.Series:
    s = series.fillna("").astype(str).str.lower().str.strip()
    s = s.str.replace(r"[\-_/]", " ", regex=True)         # normalize separators
    s = s.str.replace(r"\s+", " ", regex=True)            # collapse spaces

    def map_one(val: str) -> str:
        for pat, canon in INDUSTRY_PATTERNS_ORDERED:
            if re.search(pat, val):
                return canon
        return "other"

    return s.apply(map_one)
