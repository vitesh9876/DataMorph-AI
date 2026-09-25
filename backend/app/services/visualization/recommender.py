import uuid
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
from app.services.visualization.aggregator import ChartAggregator

class VisualizationRecommender:
    """Intelligently inspects dataset schema and recommends rich multi-dimensional visualizations."""

    @classmethod
    def recommend_charts(cls, df: pd.DataFrame) -> List[Dict[str, Any]]:
        if df.empty:
            return []

        recommendations = []
        
        # Categorize columns
        date_cols = []
        numeric_cols = []
        categorical_cols = []

        for col in df.columns:
            series = df[col].dropna()
            if series.empty:
                continue

            num_converted = pd.to_numeric(series, errors="coerce")
            if num_converted.notna().sum() > len(series) * 0.5:
                numeric_cols.append(col)
                continue

            date_converted = pd.to_datetime(series, errors="coerce")
            if date_converted.notna().sum() > len(series) * 0.5:
                date_cols.append(col)
                continue

            if series.nunique() < 100:
                categorical_cols.append(col)

        # 1. Date + Numeric -> Line Chart (Trend)
        if date_cols and numeric_cols:
            d_col = date_cols[0]
            n_col = numeric_cols[0]
            chart_data = ChartAggregator.aggregate_for_chart(df, x_col=d_col, y_col=n_col, chart_type="line", aggregation="sum")
            if chart_data:
                recommendations.append({
                    "id": str(uuid.uuid4()),
                    "title": f"{n_col} Trajectory Over Time",
                    "chart_type": "line",
                    "confidence_score": 96,
                    "reason": f"Temporal column '{d_col}' with continuous numerical metric '{n_col}' detected.",
                    "chart_config": {
                        "chart_type": "line",
                        "title": f"{n_col} Over Time",
                        "x_axis": d_col,
                        "y_axis": n_col,
                        "aggregation": "sum",
                        "color_palette": "indigo"
                    },
                    "chart_data": chart_data,
                    "is_selected": True
                })

        # 2. Categorical + Numeric -> Vertical Bar Chart (Comparison)
        if categorical_cols and numeric_cols:
            c_col = categorical_cols[0]
            n_col = numeric_cols[0]
            chart_data = ChartAggregator.aggregate_for_chart(df, x_col=c_col, y_col=n_col, chart_type="bar", aggregation="sum", max_points=12)
            if chart_data:
                recommendations.append({
                    "id": str(uuid.uuid4()),
                    "title": f"{n_col} by {c_col}",
                    "chart_type": "bar",
                    "confidence_score": 94,
                    "reason": f"High cardinality category comparison detected between '{c_col}' and '{n_col}'.",
                    "chart_config": {
                        "chart_type": "bar",
                        "title": f"{n_col} by {c_col}",
                        "x_axis": c_col,
                        "y_axis": n_col,
                        "aggregation": "sum",
                        "color_palette": "emerald"
                    },
                    "chart_data": chart_data,
                    "is_selected": True
                })

        # 3. Categorical + Numeric -> Horizontal Bar Chart (Ranked Performance)
        if categorical_cols and numeric_cols:
            c_col = categorical_cols[0]
            n_col = numeric_cols[0]
            chart_data = ChartAggregator.aggregate_for_chart(df, x_col=c_col, y_col=n_col, chart_type="horizontal_bar", aggregation="sum", max_points=8)
            if chart_data:
                recommendations.append({
                    "id": str(uuid.uuid4()),
                    "title": f"Ranked {c_col} Leaderboard",
                    "chart_type": "horizontal_bar",
                    "confidence_score": 93,
                    "reason": f"Ranked horizontal breakdown highlighting top performing {c_col} entities.",
                    "chart_config": {
                        "chart_type": "horizontal_bar",
                        "title": f"Top {c_col} Rankings",
                        "x_axis": c_col,
                        "y_axis": n_col,
                        "aggregation": "sum",
                        "color_palette": "cyan"
                    },
                    "chart_data": chart_data,
                    "is_selected": False
                })

        # 4. Donut Chart (Segment Share with Central Focus)
        low_card_cats = [c for c in categorical_cols if 2 <= df[c].nunique() <= 8]
        if low_card_cats and numeric_cols:
            c_col = low_card_cats[0]
            n_col = numeric_cols[0]
            chart_data = ChartAggregator.aggregate_for_chart(df, x_col=c_col, y_col=n_col, chart_type="donut", aggregation="sum", max_points=8)
            if chart_data:
                recommendations.append({
                    "id": str(uuid.uuid4()),
                    "title": f"{c_col} Share Breakdown",
                    "chart_type": "donut",
                    "confidence_score": 90,
                    "reason": f"Donut visualization of segment volume distribution for {c_col}.",
                    "chart_config": {
                        "chart_type": "donut",
                        "title": f"{c_col} Market Share",
                        "x_axis": c_col,
                        "y_axis": n_col,
                        "aggregation": "sum",
                        "color_palette": "violet"
                    },
                    "chart_data": chart_data,
                    "is_selected": True
                })

        # 5. Dual-Axis Composed Combo Chart (Line + Bar)
        if (date_cols or categorical_cols) and len(numeric_cols) >= 2:
            x_dim = date_cols[0] if date_cols else categorical_cols[0]
            n_col1 = numeric_cols[0]
            n_col2 = numeric_cols[1]
            chart_data = ChartAggregator.aggregate_for_chart(
                df,
                x_col=x_dim,
                y_col=n_col1,
                secondary_y_col=n_col2,
                chart_type="composed",
                aggregation="sum"
            )
            if chart_data:
                recommendations.append({
                    "id": str(uuid.uuid4()),
                    "title": f"Dual-Metric Overview: {n_col1} & {n_col2}",
                    "chart_type": "composed",
                    "confidence_score": 92,
                    "reason": f"Composed dual-axis chart pairing {n_col1} (Bar) and {n_col2} (Line Trend).",
                    "chart_config": {
                        "chart_type": "composed",
                        "title": f"{n_col1} & {n_col2} Combo",
                        "x_axis": x_dim,
                        "y_axis": n_col1,
                        "group_by": n_col2,
                        "aggregation": "sum",
                        "color_palette": "mixed"
                    },
                    "chart_data": chart_data,
                    "is_selected": True
                })

        # 6. Area Chart (Cumulative Volume)
        if date_cols and numeric_cols:
            d_col = date_cols[0]
            n_col = numeric_cols[0]
            chart_data = ChartAggregator.aggregate_for_chart(df, x_col=d_col, y_col=n_col, chart_type="area", aggregation="sum")
            if chart_data:
                recommendations.append({
                    "id": str(uuid.uuid4()),
                    "title": f"Cumulative {n_col} Volume Area",
                    "chart_type": "area",
                    "confidence_score": 91,
                    "reason": f"Continuous temporal accumulation pattern detected for {n_col}.",
                    "chart_config": {
                        "chart_type": "area",
                        "title": f"Cumulative {n_col}",
                        "x_axis": d_col,
                        "y_axis": n_col,
                        "aggregation": "sum",
                        "color_palette": "amber"
                    },
                    "chart_data": chart_data,
                    "is_selected": False
                })

        # 7. Scatter Plot (Two Numeric Correlation with Safe Coercion)
        if len(numeric_cols) >= 2:
            n_col1 = numeric_cols[0]
            n_col2 = numeric_cols[1]
            s_col1 = pd.to_numeric(df[n_col1], errors="coerce")
            s_col2 = pd.to_numeric(df[n_col2], errors="coerce")
            valid_mask = s_col1.notna() & s_col2.notna()
            s1_clean = s_col1[valid_mask].head(100)
            s2_clean = s_col2[valid_mask].head(100)
            
            scatter_data = []
            for i, (v1, v2) in enumerate(zip(s1_clean, s2_clean)):
                try:
                    val1 = round(float(v1), 2)
                    val2 = round(float(v2), 2)
                    scatter_data.append({"x": val1, "y": val2, "name": f"Item {i+1}"})
                except Exception:
                    continue

            if scatter_data:
                recommendations.append({
                    "id": str(uuid.uuid4()),
                    "title": f"{n_col1} vs {n_col2} Scatter Correlation",
                    "chart_type": "scatter",
                    "confidence_score": 88,
                    "reason": f"Continuous bivariate dispersion between '{n_col1}' and '{n_col2}'.",
                    "chart_config": {
                        "chart_type": "scatter",
                        "title": f"{n_col1} vs {n_col2}",
                        "x_axis": n_col1,
                        "y_axis": n_col2,
                        "aggregation": "none",
                        "color_palette": "cyan"
                    },
                    "chart_data": scatter_data,
                    "is_selected": False
                })

        # 8. Radar / Spider Performance Profile
        if len(categorical_cols) >= 1 and numeric_cols:
            c_col = categorical_cols[0]
            n_col = numeric_cols[0]
            chart_data = ChartAggregator.aggregate_for_chart(df, x_col=c_col, y_col=n_col, chart_type="radar", aggregation="avg", max_points=6)
            if len(chart_data) >= 3:
                recommendations.append({
                    "id": str(uuid.uuid4()),
                    "title": f"Radial Profile across {c_col}",
                    "chart_type": "radar",
                    "confidence_score": 85,
                    "reason": f"Multi-variable radial performance across {c_col} segments.",
                    "chart_config": {
                        "chart_type": "radar",
                        "title": f"{c_col} Radar Profile",
                        "x_axis": c_col,
                        "y_axis": n_col,
                        "aggregation": "avg",
                        "color_palette": "rose"
                    },
                    "chart_data": chart_data,
                    "is_selected": False
                })

        # 9. Treemap Segment Density
        if categorical_cols and numeric_cols:
            c_col = categorical_cols[0]
            n_col = numeric_cols[0]
            chart_data = ChartAggregator.aggregate_for_chart(df, x_col=c_col, y_col=n_col, chart_type="treemap", aggregation="sum", max_points=10)
            if chart_data:
                recommendations.append({
                    "id": str(uuid.uuid4()),
                    "title": f"{n_col} Treemap Density Map",
                    "chart_type": "treemap",
                    "confidence_score": 87,
                    "reason": f"Hierarchical area-weighted density layout for {c_col}.",
                    "chart_config": {
                        "chart_type": "treemap",
                        "title": f"{c_col} Treemap",
                        "x_axis": c_col,
                        "y_axis": n_col,
                        "aggregation": "sum",
                        "color_palette": "purple"
                    },
                    "chart_data": chart_data,
                    "is_selected": False
                })

        return recommendations
