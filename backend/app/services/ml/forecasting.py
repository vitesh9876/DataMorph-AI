import logging
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

try:
    from sklearn.linear_model import Ridge
    from sklearn.preprocessing import PolynomialFeatures
    SKLEARN_AVAILABLE = True
except (ImportError, Exception) as e:
    SKLEARN_AVAILABLE = False
    logger.warning(f"Scikit-learn Ridge unavailable ({e}), using robust polynomial numpy regression.")

class TimeSeriesForecaster:
    """Predicts future trends from historical date-value series with robust regression."""

    @classmethod
    def generate_forecast(
        cls,
        df: pd.DataFrame,
        date_column: str,
        value_column: str,
        periods: int = 12,
        frequency: str = "M"
    ) -> Dict[str, Any]:
        if df.empty or date_column not in df.columns or value_column not in df.columns:
            raise ValueError("Invalid dataframe or columns specified for forecasting.")

        # Prepare and sort date series
        temp_df = df[[date_column, value_column]].copy()
        temp_df[date_column] = pd.to_datetime(temp_df[date_column], errors="coerce")
        temp_df[value_column] = pd.to_numeric(temp_df[value_column], errors="coerce")
        
        # Drop invalid rows
        temp_df = temp_df.dropna().sort_values(by=date_column)
        if len(temp_df) < 3:
            raise ValueError("Insufficient temporal data points to generate forecast (minimum 3 required).")

        # Resample to ensure uniform frequency
        temp_df = temp_df.set_index(date_column)
        rule_map = {"D": "D", "W": "W", "M": "ME", "Y": "YE"}
        resample_rule = rule_map.get(frequency.upper(), "ME")
        
        try:
            resampled = temp_df.resample(resample_rule).mean().interpolate(method="linear")
        except Exception:
            resampled = temp_df.resample("ME").mean().interpolate(method="linear")

        if len(resampled) < 3:
            resampled = temp_df

        y = resampled[value_column].values
        n = len(y)
        X = np.arange(n).reshape(-1, 1)

        deg = min(2, max(1, n // 5))

        if SKLEARN_AVAILABLE:
            try:
                poly = PolynomialFeatures(degree=deg)
                X_poly = poly.fit_transform(X)
                
                model = Ridge(alpha=1.0)
                model.fit(X_poly, y)
                
                y_fit = model.predict(X_poly)
                
                future_X = np.arange(n, n + periods).reshape(-1, 1)
                future_X_poly = poly.transform(future_X)
                y_pred = model.predict(future_X_poly)
            except Exception:
                # Fallback to pure numpy
                coeffs = np.polyfit(X.flatten(), y, deg=deg)
                y_fit = np.polyval(coeffs, X.flatten())
                future_X = np.arange(n, n + periods)
                y_pred = np.polyval(coeffs, future_X)
        else:
            coeffs = np.polyfit(X.flatten(), y, deg=deg)
            y_fit = np.polyval(coeffs, X.flatten())
            future_X = np.arange(n, n + periods)
            y_pred = np.polyval(coeffs, future_X)

        # Standard error & confidence bounds
        residuals = y - y_fit
        sigma = np.std(residuals) if len(residuals) > 0 else 0.1
        
        # Build date timeline
        last_date = resampled.index[-1]
        freq_offset = pd.tseries.frequencies.to_offset(resample_rule)
        future_dates = pd.date_range(start=last_date + freq_offset, periods=periods, freq=resample_rule)

        historical_points = []
        for d, actual, fit in zip(resampled.index, y, y_fit):
            historical_points.append({
                "date": d.strftime("%Y-%m-%d"),
                "actual": round(float(actual), 2),
                "predicted": round(float(fit), 2),
                "lower_bound": None,
                "upper_bound": None
            })

        forecast_points = []
        for i, (fd, pred) in enumerate(zip(future_dates, y_pred)):
            expansion = 1.0 + (i * 0.05)
            spread = 1.96 * sigma * expansion
            forecast_points.append({
                "date": fd.strftime("%Y-%m-%d"),
                "actual": None,
                "predicted": round(float(pred), 2),
                "lower_bound": round(float(max(0, pred - spread)), 2),
                "upper_bound": round(float(pred + spread), 2)
            })

        trend_direction = "Upward" if y_pred[-1] > y[-1] else "Downward"
        growth_pct = round(((y_pred[-1] - y[-1]) / (abs(y[-1]) or 1.0)) * 100, 1)

        return {
            "historical": historical_points,
            "forecast": forecast_points,
            "metrics": {
                "trend_direction": trend_direction,
                "projected_growth_pct": growth_pct,
                "confidence_level": 95,
                "standard_error": round(float(sigma), 2),
                "algorithm": "Polynomial Ridge Regression"
            }
        }
