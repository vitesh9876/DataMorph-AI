import pytest
import pandas as pd
from app.services.visualization.recommender import VisualizationRecommender
from app.services.visualization.aggregator import ChartAggregator

def test_visualization_recommender():
    df = pd.DataFrame({
        "Date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
        "Product": ["iPhone", "MacBook", "iPad", "AirPods"],
        "Revenue": [1200, 2400, 800, 300],
        "Units": [2, 1, 3, 5]
    })

    charts = VisualizationRecommender.recommend_charts(df)
    assert len(charts) >= 2
    chart_types = [c["chart_type"] for c in charts]
    assert "line" in chart_types or "bar" in chart_types

def test_chart_aggregator():
    df = pd.DataFrame({
        "Category": ["A", "B", "A", "B", "C"],
        "Sales": [100, 200, 150, 250, 300]
    })
    agg_res = ChartAggregator.aggregate_for_chart(df, x_col="Category", y_col="Sales", chart_type="bar", aggregation="sum")
    assert len(agg_res) == 3
    cat_a = next((item for item in agg_res if item["name"] == "A"), None)
    assert cat_a is not None and cat_a["value"] == 250
