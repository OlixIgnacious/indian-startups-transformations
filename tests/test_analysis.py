import pandas as pd
from transforms.analysis import detect_amount_outliers, amount_stats_summary

def test_amount_outliers_small():
    df = pd.DataFrame({"amount": [10, 12, 14, 16, 1000]})
    df2 = detect_amount_outliers(df, col="amount")
    assert df2["is_outlier"].sum() >= 1
    summary = amount_stats_summary(df2, column="amount")
    assert summary["outliers"] >= 1
    assert summary["min"] == 10
    assert summary["max"] == 1000