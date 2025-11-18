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

SPLIT_PATTERN = r",\s*|;\s*|\s+&\s+"

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

def normalize_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    MISSING_TOKENS = ["N/A", "n/a", "NA", "na", "-", "--", " ", ""]
    df = df.copy()
    df.replace(to_replace=MISSING_TOKENS, value=pd.NA, inplace=True)
    return df

def clean_amount_column(df: pd.DataFrame, col: str = "amount") -> pd.DataFrame:
    df = df.copy()
    df[col] = df[col].astype(str).fillna("")
    #df[col] = df[col].str.replace(",", "")
    df[col] = df[col].str.strip()
    #df[col] = df[col].str.replace(r"[\$,€£¥]", "", regex=True)
    df[col] = df[col].str.replace(r"[^0-9\.\-]", '', regex=True).replace('', pd.NA)
    df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def parse_dates(df: pd.DataFrame, col: str = "date") -> pd.DataFrame:
    df = df.copy()
    df[col] = pd.to_datetime(df[col], errors='coerce') 
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

def split_investors(s: pd.Series) -> pd.Series:
    s = s.astype(str).str.strip()
    out = s.fillna("").str.split(SPLIT_PATTERN)
    return out

def clean_startup_name(name: str) -> str:
    if not isinstance(name, str):
        return name
    s = name.strip()
    s = re.sub(SUFFIX_PATTERN, "", s, flags=re.IGNORECASE | re.VERBOSE)
    s = re.sub(r'\bpvt\.?\b', '', s, flags=re.IGNORECASE)
    return s.strip()

