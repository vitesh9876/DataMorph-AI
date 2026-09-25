import os
import pytest
import pandas as pd
from app.services.structuring.normalizer import DataNormalizer
from app.services.structuring.quality import QualityAnalyzer
from app.services.structuring.cleaner import DataCleaner

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "sample_data")

def test_currency_normalization():
    val1, ok1 = DataNormalizer.clean_currency_or_number("$1,200.50")
    assert ok1 and val1 == 1200.50

    val2, ok2 = DataNormalizer.clean_currency_or_number("₹1,00,000")
    assert ok2 and val2 == 100000.0

    val3, ok3 = DataNormalizer.clean_currency_or_number("(500)")
    assert ok3 and val3 == -500.0

def test_date_standardization():
    d1, ok1 = DataNormalizer.standardize_date("01/16/2024")
    assert ok1 and d1 == "2024-01-16"

    d2, ok2 = DataNormalizer.standardize_date("2024-05-20")
    assert ok2 and d2 == "2024-05-20"

def test_category_unification():
    series = pd.Series(["iphone", "iPhone", "IPHONE", "MacBook", "macbook"])
    cleaned, mapping, count = DataNormalizer.unify_category_names(series)
    assert count > 0
    assert cleaned.iloc[0] == cleaned.iloc[1]

def test_quality_and_cleaning_flow():
    file_path = os.path.join(SAMPLE_DIR, "sales_dirty.csv")
    df = pd.read_csv(file_path)

    # Initial quality
    initial_eval = QualityAnalyzer.evaluate_quality(df)
    score_before = initial_eval["overall_score"]

    # Recommendations
    recs = DataCleaner.generate_recommendations(df)
    assert len(recs) > 0

    # Apply all recommendations
    cleaned_df = df.copy()
    for r in recs:
        cleaned_df = DataCleaner.apply_rule(
            df=cleaned_df,
            rule_type=r["rule_type"],
            target_column=r["target_column"],
            suggested_action=r["suggested_action"],
            parameters=r.get("parameters", {})
        )

    # Cleaned quality
    after_eval = QualityAnalyzer.evaluate_quality(cleaned_df)
    score_after = after_eval["overall_score"]

    # Quality score should improve
    assert score_after >= score_before
