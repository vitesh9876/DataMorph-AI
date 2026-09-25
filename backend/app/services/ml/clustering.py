import logging
from typing import Dict, Any, List
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class CorrelationEngine:
    """Computes correlation matrices and extracts significant variable relationships."""

    @classmethod
    def analyze_correlations(cls, df: pd.DataFrame) -> Dict[str, Any]:
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.empty or numeric_df.shape[1] < 2:
            return {
                "columns": [],
                "matrix": [],
                "strong_correlations": []
            }

        corr_matrix = numeric_df.corr().fillna(0.0)
        cols = list(corr_matrix.columns)
        matrix = [[round(float(val), 3) for val in row] for row in corr_matrix.values]

        # Extract strong pairs
        strong = []
        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                r_val = corr_matrix.iloc[i, j]
                if abs(r_val) >= 0.5:
                    strong.append({
                        "var1": cols[i],
                        "var2": cols[j],
                        "correlation": round(float(r_val), 3),
                        "type": "positive" if r_val > 0 else "negative"
                    })

        strong.sort(key=lambda x: abs(x["correlation"]), reverse=True)

        return {
            "columns": cols,
            "matrix": matrix,
            "strong_correlations": strong[:10]
        }
