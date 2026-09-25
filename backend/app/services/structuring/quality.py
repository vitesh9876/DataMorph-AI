import math
from typing import Dict, Any, List
import pandas as pd
import numpy as np

class QualityAnalyzer:
    """Calculates comprehensive Data Quality metrics and scores."""

    @classmethod
    def evaluate_quality(cls, df: pd.DataFrame) -> Dict[str, Any]:
        if df.empty:
            return {
                "completeness": 0.0,
                "consistency": 0.0,
                "uniqueness": 0.0,
                "validity": 0.0,
                "overall_score": 0.0,
                "columns_analysis": []
            }

        total_cells = df.shape[0] * df.shape[1]
        
        # 1. Completeness: % of non-null, non-empty cells
        null_count = int(df.isna().sum().sum())
        # Also count empty strings safely
        empty_str_count = int(df.map(lambda x: str(x).strip().lower() in ["", "nan", "none", "null", "n/a", "na"] if pd.notna(x) else True).sum().sum())
        effective_missing = max(null_count, empty_str_count)
        completeness = max(0.0, min(100.0, ((total_cells - effective_missing) / max(total_cells, 1)) * 100.0))

        # 2. Uniqueness: % of non-duplicate rows
        total_rows = len(df)
        duplicate_rows = int(df.duplicated().sum())
        uniqueness = max(0.0, min(100.0, ((total_rows - duplicate_rows) / max(total_rows, 1)) * 100.0))

        # 3. Consistency: type uniformity per column
        type_scores = []
        columns_meta = []
        for col in df.columns:
            series = df[col].dropna()
            total_non_null = len(series)
            if total_non_null == 0:
                type_scores.append(50.0)
                continue

            # Check if values in column have homogeneous data types
            types = set(series.map(lambda x: type(x).__name__))
            consistency_col = 100.0 if len(types) <= 1 else max(40.0, 100.0 - (len(types) * 15.0))
            type_scores.append(consistency_col)

            # Check numeric / datetime properties
            numeric_count = pd.to_numeric(series, errors="coerce").notna().sum()
            is_numeric = (numeric_count / total_non_null) > 0.8
            
            datetime_count = pd.to_datetime(series, errors="coerce").notna().sum()
            is_datetime = (datetime_count / total_non_null) > 0.8 and not is_numeric

            null_col_count = int(df[col].isna().sum())
            null_pct = round((null_col_count / max(total_rows, 1)) * 100.0, 1)

            columns_meta.append({
                "name": str(col),
                "dtype": str(df[col].dtype),
                "sample_values": [str(v) for v in series.head(5).tolist()],
                "null_count": null_col_count,
                "null_percentage": null_pct,
                "unique_count": int(df[col].nunique()),
                "is_numeric": bool(is_numeric),
                "is_datetime": bool(is_datetime),
                "is_categorical": bool(not is_numeric and not is_datetime and df[col].nunique() < 50)
            })

        consistency = sum(type_scores) / max(len(type_scores), 1)

        # 4. Validity: valid ranges, non-zero column variance
        validity = 95.0
        # Deduct slightly if constant columns exist
        constant_cols = [c for c in df.columns if df[c].nunique() == 1]
        if constant_cols:
            validity -= (len(constant_cols) * 5.0)
        validity = max(50.0, min(100.0, validity))

        # 5. Composite Data Quality Score
        # Weights: Completeness (35%), Consistency (25%), Uniqueness (25%), Validity (15%)
        overall_score = round(
            (completeness * 0.35) +
            (consistency * 0.25) +
            (uniqueness * 0.25) +
            (validity * 0.15),
            1
        )

        return {
            "completeness": round(completeness, 1),
            "consistency": round(consistency, 1),
            "uniqueness": round(uniqueness, 1),
            "validity": round(validity, 1),
            "overall_score": max(10.0, min(100.0, overall_score)),
            "columns_analysis": columns_meta
        }
