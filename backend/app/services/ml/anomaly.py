import logging
from typing import List, Dict, Any
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

try:
    from sklearn.ensemble import IsolationForest
    SKLEARN_AVAILABLE = True
except (ImportError, Exception) as e:
    SKLEARN_AVAILABLE = False
    logger.warning(f"Scikit-learn IsolationForest unavailable ({e}), using robust statistical anomaly scoring.")

class AnomalyDetector:
    """Detects multi-dimensional statistical outliers and anomalies using Isolation Forest with statistical fallback."""

    @classmethod
    def detect_anomalies(cls, df: pd.DataFrame, contamination: float = 0.05) -> Dict[str, Any]:
        if df.empty or len(df) < 5:
            return {
                "total_anomalies": 0,
                "anomaly_percentage": 0.0,
                "algorithm": "Isolation Forest",
                "anomalies": []
            }

        # Select numeric columns
        numeric_cols = []
        for col in df.columns:
            cleaned_col = pd.to_numeric(df[col], errors="coerce")
            if cleaned_col.notna().sum() > len(df) * 0.7:
                numeric_cols.append(col)

        if not numeric_cols:
            return {
                "total_anomalies": 0,
                "anomaly_percentage": 0.0,
                "algorithm": "Isolation Forest (No numeric columns detected)",
                "anomalies": []
            }

        # Build feature matrix
        feature_df = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
        # Impute NaNs with median for model stability
        for col in numeric_cols:
            feature_df[col] = feature_df[col].fillna(feature_df[col].median() if not pd.isna(feature_df[col].median()) else 0.0)

        # Scale contamination based on row count
        contam = min(max(contamination, 0.01), 0.15)
        
        if SKLEARN_AVAILABLE:
            try:
                iso_forest = IsolationForest(
                    n_estimators=100,
                    contamination=contam,
                    random_state=42
                )
                predictions = iso_forest.fit_predict(feature_df)
                decision_scores = iso_forest.decision_function(feature_df)

                anomaly_items = []
                for idx, (pred, score) in enumerate(zip(predictions, decision_scores)):
                    if pred == -1:
                        row_vals = feature_df.iloc[idx]
                        reasons = []
                        for c in numeric_cols:
                            med = feature_df[c].median()
                            std = feature_df[c].std()
                            if std > 0 and abs(row_vals[c] - med) / std > 1.8:
                                reasons.append(f"{c} is {round(row_vals[c], 2)} (deviates from median {round(med, 2)})")

                        anomaly_items.append({
                            "row_index": idx,
                            "anomaly_score": round(float(-score), 3),
                            "severity": "high" if score < -0.15 else "medium",
                            "reasons": reasons or ["Multi-dimensional outlier across joint feature distributions"],
                            "row_data": df.iloc[idx].to_dict()
                        })

                return {
                    "total_anomalies": len(anomaly_items),
                    "anomaly_percentage": round((len(anomaly_items) / len(df)) * 100, 1),
                    "algorithm": "Isolation Forest",
                    "anomalies": anomaly_items
                }
            except Exception as e:
                logger.warning(f"IsolationForest execution failed ({e}), falling back to robust IQR/Z-score.")

        # Fallback: Robust IQR & Z-score multi-variate anomaly detector
        anomaly_items = []
        z_scores_max = np.zeros(len(df))
        for col in numeric_cols:
            vals = feature_df[col].values
            med = np.median(vals)
            mad = np.median(np.abs(vals - med)) or np.std(vals) or 1.0
            col_z = np.abs(vals - med) / (1.4826 * mad)
            z_scores_max = np.maximum(z_scores_max, col_z)

        threshold = 2.5
        for idx in range(len(df)):
            score = z_scores_max[idx]
            if score > threshold:
                row_vals = feature_df.iloc[idx]
                reasons = []
                for c in numeric_cols:
                    med = feature_df[c].median()
                    std = feature_df[c].std() or 1.0
                    if abs(row_vals[c] - med) / std > 1.8:
                        reasons.append(f"{c} is {round(row_vals[c], 2)} (deviates from median {round(med, 2)})")

                anomaly_items.append({
                    "row_index": idx,
                    "anomaly_score": round(float(score), 3),
                    "severity": "high" if score > 3.5 else "medium",
                    "reasons": reasons or ["Statistical deviation beyond 99% threshold"],
                    "row_data": df.iloc[idx].to_dict()
                })

        return {
            "total_anomalies": len(anomaly_items),
            "anomaly_percentage": round((len(anomaly_items) / len(df)) * 100, 1),
            "algorithm": "Robust Statistical Isolation (IQR & Z-score)",
            "anomalies": anomaly_items
        }
