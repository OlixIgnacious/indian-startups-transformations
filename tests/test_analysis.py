import pandas as pd
from transforms.analysis import detect_amount_outliers, amount_stats_summary, bucketize_amount

def test_amount_outliers_small():
    df = pd.DataFrame({"amount": [10, 12, 14, 16, 1000]})
    df2 = detect_amount_outliers(df, col="amount")
    assert df2["is_outlier"].sum() >= 1
    summary = amount_stats_summary(df2, column="amount")
    assert summary["outliers"] >= 1
    assert summary["min"] == 10
    assert summary["max"] == 1000

def test_bucketize_amount_boundaries():
    df = pd.DataFrame({
        "amount": [
            0,          # very_small
            1_000_000,  # very_small upper boundary
            1_000_001,  # small
            10_000_000, # small upper boundary
            10_000_001, # medium
            50_000_000, # medium upper boundary
            50_000_001, # large
            200_000_000,# large upper boundary
            200_000_001,# very_large
            500_000_000,# very_large upper boundary
            500_000_001 # mega
        ]
    })
    df_b = bucketize_amount(df, col="amount")
    expected = [
        "very_small",
        "very_small",
        "small",
        "small",
        "medium",
        "medium",
        "large",
        "large",
        "very_large",
        "very_large",
        "mega",
    ]
    assert df_b["amount_bucket"].tolist() == expected

def test_bucketize_amount_nan():
    df = pd.DataFrame({"amount": [None, float("nan"), 1_000_000]})
    df_b = bucketize_amount(df, col="amount")
    assert df_b["amount_bucket"].iloc[0] == "unknown"
    assert df_b["amount_bucket"].iloc[1] == "unknown"
    assert df_b["amount_bucket"].iloc[2] == "very_small"