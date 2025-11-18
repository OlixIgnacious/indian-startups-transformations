import pandas as pd
from typing import Any
from transforms.cleaner import clean_amount_column, clean_column_names
import re

def detect_amount_outliers(df: pd.DataFrame, col: str = "amount") -> pd.DataFrame:
    df = clean_column_names(df)
    df = clean_amount_column(df, col)
    
    def compute_z_score(series: pd.Series) -> pd.Series:
        series = df["amount"].dropna()
        mean = series.mean()
        std = series.std()
        return (series - mean) / std
    
    df['z_score'] = compute_z_score(df[col])
    df['zscore_outlier'] = df['z_score'].abs() > 3
    
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    df['iqr_outlier'] = (df[col] < lower_bound) | (df[col] > upper_bound)
    
    df['is_outlier'] = df['zscore_outlier'] | df['iqr_outlier']
    
    return df

def amount_stats_summary(df: pd.DataFrame, column: str) -> pd.DataFrame:
    series = df[column].dropna()
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    outlier_count = df["is_outlier"].sum() if "is_outlier" in df.columns else None
    pct_outlier = (outlier_count / len(df)) * 100 if outlier_count is not None else None

    return {
        "min": series.min(),
        "max": series.max(),
        "mean": series.mean(),
        "median": series.median(),
        "std": series.std(),
        "Q1": Q1,
        "Q3": Q3,
        "IQR": IQR,
        "outliers": int(outlier_count) if outlier_count is not None else None,
        "pct_outliers": pct_outlier
    }

def bucketize_amount(df: pd.DataFrame, col: str = "amount") -> pd.DataFrame:
    def bucket_amount_value(x: float) -> str:
        if pd.isna(x):
            return "unknown"
        if x <= 1e6:
            return "very_small"
        elif x <= 1e7:
            return "small"
        elif x <= 5e7:
            return "medium"
        elif x <= 2e8:
            return "large"
        elif x <= 5e8:
            return "very_large"
        else:
            return "mega"
    
    df = df.copy()
    df['amount_bucket'] = df[col].apply(bucket_amount_value)
    return df