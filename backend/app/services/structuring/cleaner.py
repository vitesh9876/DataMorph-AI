import uuid
from typing import List, Dict, Any, Tuple
import pandas as pd
import numpy as np
from app.services.structuring.normalizer import DataNormalizer
from app.services.structuring.quality import QualityAnalyzer

class DataCleaner:
    """Detects issues and generates interactive cleaning recommendations."""

    @classmethod
    def generate_recommendations(cls, df: pd.DataFrame) -> List[Dict[str, Any]]:
        recommendations = []

        # 1. Check for duplicate rows
        duplicates_count = int(df.duplicated().sum())
        if duplicates_count > 0:
            dup_sample = df[df.duplicated(keep=False)].head(4).to_dict(orient="records")
            recommendations.append({
                "id": str(uuid.uuid4()),
                "rule_type": "duplicates",
                "title": f"Deduplicate Records",
                "description": f"{duplicates_count} duplicate records detected across the dataset.",
                "target_column": None,
                "suggested_action": "drop_duplicates",
                "parameters": {},
                "status": "pending",
                "impact_score_gain": round(min(18.0, (duplicates_count / max(len(df), 1)) * 40.0), 1),
                "before_preview": dup_sample,
                "after_preview": []
            })

        # 2. Check each column for specific data issues
        for col in df.columns:
            series = df[col]
            non_null_series = series.dropna()

            # A. Missing Values
            null_count = int(series.isna().sum())
            if null_count > 0:
                is_numeric = pd.to_numeric(non_null_series, errors="coerce").notna().sum() / max(len(non_null_series), 1) > 0.8
                action = "impute_median" if is_numeric else "impute_mode"
                action_desc = "imputing with median value" if is_numeric else "imputing with most frequent category"

                recommendations.append({
                    "id": str(uuid.uuid4()),
                    "rule_type": "missing_values",
                    "title": f"Handle Missing Values in '{col}'",
                    "description": f"Found {null_count} missing values ({round((null_count/len(df))*100, 1)}%). Recommended: {action_desc}.",
                    "target_column": str(col),
                    "suggested_action": action,
                    "parameters": {"strategy": action},
                    "status": "pending",
                    "impact_score_gain": round(min(12.0, (null_count / max(len(df), 1)) * 25.0), 1),
                    "before_preview": [f"Row has NaN in {col}"],
                    "after_preview": ["Imputed with standard representative value"]
                })

            # B. Category Casing / Variations (e.g. iphone vs iPhone vs IPHONE)
            if series.dtype == "object" and 0 < series.nunique() < 100:
                _, mapping, var_count = DataNormalizer.unify_category_names(series)
                if var_count > 0:
                    before_examples = list(mapping.keys())[:4]
                    after_examples = [mapping[k] for k in before_examples]
                    recommendations.append({
                        "id": str(uuid.uuid4()),
                        "rule_type": "category_unify",
                        "title": f"Standardize Inconsistent Casing in '{col}'",
                        "description": f"Detected {var_count} inconsistent text variations (e.g., {', '.join(before_examples[:2])}).",
                        "target_column": str(col),
                        "suggested_action": "unify_categories",
                        "parameters": {"mapping": mapping},
                        "status": "pending",
                        "impact_score_gain": 4.5,
                        "before_preview": before_examples,
                        "after_preview": after_examples
                    })

            # C. Mixed Currency Symbols in text column
            if series.dtype == "object":
                has_currency = non_null_series.astype(str).str.contains(r"[\$€£₹¥]|USD|INR|EUR", regex=True).sum()
                if has_currency > max(2, len(non_null_series) * 0.3):
                    sample_vals = non_null_series.head(3).tolist()
                    cleaned_sample = [DataNormalizer.clean_currency_or_number(v)[0] for v in sample_vals]
                    recommendations.append({
                        "id": str(uuid.uuid4()),
                        "rule_type": "currency_normalize",
                        "title": f"Normalize Currency Values in '{col}'",
                        "description": f"Column contains mixed currency symbols and formatted strings. Convert to standard numeric floats.",
                        "target_column": str(col),
                        "suggested_action": "clean_currency",
                        "parameters": {},
                        "status": "pending",
                        "impact_score_gain": 6.0,
                        "before_preview": sample_vals,
                        "after_preview": cleaned_sample
                    })

            # D. Inconsistent Date Strings
            if series.dtype == "object":
                # Check if it looks like dates
                parsed_dates = pd.to_datetime(non_null_series, errors="coerce")
                valid_dates_count = parsed_dates.notna().sum()
                if valid_dates_count > len(non_null_series) * 0.7:
                    sample_dates = non_null_series.head(3).tolist()
                    cleaned_dates = [DataNormalizer.standardize_date(d)[0] for d in sample_dates]
                    recommendations.append({
                        "id": str(uuid.uuid4()),
                        "rule_type": "date_normalize",
                        "title": f"Standardize Date Format in '{col}'",
                        "description": f"Standardize mixed date timestamps into ISO 8601 (YYYY-MM-DD).",
                        "target_column": str(col),
                        "suggested_action": "standardize_dates",
                        "parameters": {},
                        "status": "pending",
                        "impact_score_gain": 5.0,
                        "before_preview": sample_dates,
                        "after_preview": cleaned_dates
                    })

        return recommendations

    @classmethod
    def apply_rule(cls, df: pd.DataFrame, rule_type: str, target_column: str, suggested_action: str, parameters: Dict[str, Any]) -> pd.DataFrame:
        """Applies a single cleaning rule deterministically to the dataframe."""
        cleaned_df = df.copy()

        if suggested_action == "drop_duplicates" or rule_type == "duplicates":
            cleaned_df = cleaned_df.drop_duplicates().reset_index(drop=True)

        elif suggested_action == "impute_median" and target_column in cleaned_df:
            numeric_col = pd.to_numeric(cleaned_df[target_column], errors="coerce")
            median_val = numeric_col.median()
            cleaned_df[target_column] = cleaned_df[target_column].fillna(median_val)

        elif suggested_action == "impute_mode" and target_column in cleaned_df:
            mode_vals = cleaned_df[target_column].mode()
            if not mode_vals.empty:
                cleaned_df[target_column] = cleaned_df[target_column].fillna(mode_vals[0])
            else:
                cleaned_df[target_column] = cleaned_df[target_column].fillna("Unknown")

        elif suggested_action == "unify_categories" and target_column in cleaned_df:
            mapping = parameters.get("mapping", {})
            if not mapping:
                cleaned_series, mapping, _ = DataNormalizer.unify_category_names(cleaned_df[target_column])
                cleaned_df[target_column] = cleaned_series
            else:
                cleaned_df[target_column] = cleaned_df[target_column].replace(mapping)

        elif suggested_action == "clean_currency" and target_column in cleaned_df:
            cleaned_df[target_column] = cleaned_df[target_column].map(lambda x: DataNormalizer.clean_currency_or_number(x)[0])

        elif suggested_action == "standardize_dates" and target_column in cleaned_df:
            cleaned_df[target_column] = cleaned_df[target_column].map(lambda x: DataNormalizer.standardize_date(x)[0])

        return cleaned_df
