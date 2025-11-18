import pandas as pd
from typing import Any
from transforms.cleaner import clean_amount_column, clean_column_names
import re

def detect_amount_outliers(df: pd.DataFrame, col: str = "amount") -> pd.DataFrame:
    df = clean_column_names(df)
    df = clean_amount_column(df, col)
    
    def compute_z_score(series: pd.Series) -> pd.Series:
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
    stats = {
        'mean': df[column].mean(),
        'median': df[column].median(),
        'std_dev': df[column].std(),
        'min': df[column].min(),
        'max': df[column].max(),
        'q1': df[column].quantile(0.25),
        'q3': df[column].quantile(0.75),
        'iqr': df[column].quantile(0.75) - df[column].quantile(0.25),
        'count_outliers': df['is_outlier'].sum(),
        'pct_outliers': df['is_outlier'].mean() * 100
    }
    return pd.DataFrame([stats])