from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np

class ChartAggregator:
    """Aggregates and formats DataFrame columns into clean JSON structures for rich charts."""

    @classmethod
    def aggregate_for_chart(
        cls,
        df: pd.DataFrame,
        x_col: str,
        y_col: Optional[str] = None,
        secondary_y_col: Optional[str] = None,
        chart_type: str = "bar",
        aggregation: str = "sum",
        group_by: Optional[str] = None,
        max_points: int = 25
    ) -> List[Dict[str, Any]]:
        if df.empty or x_col not in df.columns:
            return []

        temp_df = df.copy()

        # If y_col is not provided, count occurrences of x_col
        if not y_col or y_col == x_col or y_col not in temp_df.columns:
            val_counts = temp_df[x_col].value_counts().head(max_points)
            return [{"name": str(k), "value": int(v), str(x_col): str(k), "count": int(v)} for k, v in val_counts.items()]

        # Ensure numeric conversion on y_col
        temp_df[y_col] = pd.to_numeric(temp_df[y_col], errors="coerce")
        subset_cols = [x_col, y_col]
        
        if secondary_y_col and secondary_y_col in temp_df.columns:
            temp_df[secondary_y_col] = pd.to_numeric(temp_df[secondary_y_col], errors="coerce")
            subset_cols.append(secondary_y_col)

        temp_df = temp_df.dropna(subset=[x_col, y_col])

        # Date formatting if x_col is temporal
        try:
            if pd.to_datetime(temp_df[x_col], errors="coerce").notna().sum() > len(temp_df) * 0.7:
                temp_df[x_col] = pd.to_datetime(temp_df[x_col], errors="coerce").dt.strftime("%Y-%m-%d")
                temp_df = temp_df.sort_values(by=x_col)
        except Exception:
            pass

        # Apply aggregation
        agg_func = "sum" if aggregation == "sum" else ("mean" if aggregation in ["avg", "mean"] else ("count" if aggregation == "count" else "sum"))
        
        agg_dict = {y_col: agg_func}
        if secondary_y_col and secondary_y_col in temp_df.columns:
            agg_dict[secondary_y_col] = agg_func

        grouped = temp_df.groupby(x_col).agg(agg_dict).reset_index()

        # Sorting based on chart type
        if chart_type in ["bar", "horizontal_bar", "pie", "donut", "treemap", "radar"]:
            grouped = grouped.sort_values(by=y_col, ascending=False).head(max_points)
        elif chart_type in ["line", "area", "composed", "forecast"]:
            grouped = grouped.head(max_points)

        results = []
        for _, row in grouped.iterrows():
            val = row[y_col]
            clean_val = round(float(val), 2) if isinstance(val, (int, float, np.number)) and not pd.isna(val) else 0.0
            
            res_item: Dict[str, Any] = {
                "name": str(row[x_col]),
                "value": clean_val,
                str(x_col): str(row[x_col]),
                str(y_col): clean_val
            }

            if secondary_y_col and secondary_y_col in row:
                sec_val = row[secondary_y_col]
                sec_clean = round(float(sec_val), 2) if isinstance(sec_val, (int, float, np.number)) and not pd.isna(sec_val) else 0.0
                res_item[str(secondary_y_col)] = sec_clean
                res_item["secondary_value"] = sec_clean

            results.append(res_item)

        return results
