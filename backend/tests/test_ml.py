import os
import pytest
import pandas as pd
from app.services.ml.anomaly import AnomalyDetector
from app.services.ml.forecasting import TimeSeriesForecaster
from app.services.ml.clustering import CorrelationEngine

def test_anomaly_detection():
    # Normal data + 1 clear massive outlier
    df = pd.DataFrame({
        "Revenue": [100, 105, 98, 102, 110, 95, 105, 10000, 99, 103, 101, 97],
        "Units": [2, 2, 2, 2, 2, 2, 2, 50, 2, 2, 2, 2]
    })
    result = AnomalyDetector.detect_anomalies(df, contamination=0.1)
    assert result["total_anomalies"] > 0
    # Top anomaly should be row 7 (value 10000)
    top_anomaly = result["anomalies"][0]
    assert top_anomaly["row_index"] == 7

def test_time_series_forecasting():
    dates = pd.date_range(start="2023-01-01", periods=12, freq="ME")
    revenue = [1000, 1100, 1250, 1300, 1450, 1500, 1650, 1700, 1850, 1900, 2050, 2200]
    df = pd.DataFrame({"Date": dates, "Revenue": revenue})

    forecast = TimeSeriesForecaster.generate_forecast(
        df=df,
        date_column="Date",
        value_column="Revenue",
        periods=6,
        frequency="M"
    )
    assert len(forecast["forecast_data"]) == 18 # 12 actual + 6 predicted
    assert forecast["summary_insight"] != ""

def test_correlation_analysis():
    df = pd.DataFrame({
        "A": [1, 2, 3, 4, 5, 6],
        "B": [2, 4, 6, 8, 10, 12],
        "C": [10, 9, 8, 7, 6, 5]
    })
    result = CorrelationEngine.analyze_correlations(df)
    assert len(result["columns"]) == 3
    assert len(result["strong_correlations"]) >= 1
