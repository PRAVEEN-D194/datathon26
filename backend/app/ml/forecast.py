import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.schemas.prediction_schema import ForecastPoint
from app.core.logging import logger

def forecast_crime_counts(dates: List[datetime], months_to_forecast: int = 6) -> List[ForecastPoint]:
    """
    Perform Time Series Forecasting using ARIMA (via statsmodels) 
    with a robust Moving Average / Linear Regression fallback if data is sparse.
    """
    if not dates or len(dates) < 3:
        # Extreme fallback: mock projection if virtually no data
        logger.warning("Insufficient data points for forecasting. Generating baseline projection.")
        return generate_mock_forecast(months_to_forecast)

    # 1. Prepare historical time series (Group by Month)
    df = pd.DataFrame({"date": dates})
    df["month"] = df["date"].dt.to_period("M")
    monthly_counts = df.groupby("month").size().reset_index(name="count")
    
    # Sort and set index
    monthly_counts = monthly_counts.sort_values("month")
    monthly_counts.index = monthly_counts["month"].dt.to_timestamp()
    ts = monthly_counts["count"].astype(float)
    
    forecast_results = []
    last_date = ts.index[-1]
    
    # Generate future dates
    future_dates = [last_date + pd.DateOffset(months=i) for i in range(1, months_to_forecast + 1)]
    
    # 2. Try Fitting ARIMA Model
    try:
        from statsmodels.tsa.arima.model import ARIMA
        # Use simpler order (1, 1, 0) or (1, 0, 0) to avoid convergence issues
        order = (1, 1, 0) if len(ts) >= 12 else (1, 0, 0)
        
        # Fit model
        model = ARIMA(ts, order=order)
        model_fit = model.fit()
        
        # Forecast
        forecast_res = model_fit.get_forecast(steps=months_to_forecast)
        predicted = forecast_res.predicted_mean
        conf_int = forecast_res.conf_int(alpha=0.2)  # 80% confidence interval
        
        for idx, date in enumerate(future_dates):
            pred_val = max(0.0, float(predicted.iloc[idx]))
            lower_val = max(0.0, float(conf_int.iloc[idx, 0]))
            upper_val = float(conf_int.iloc[idx, 1])
            
            # Ensure logical lower bounds
            if lower_val > pred_val:
                lower_val = pred_val * 0.8
            if upper_val < pred_val:
                upper_val = pred_val * 1.2
                
            forecast_results.append(
                ForecastPoint(
                    date=date.strftime("%Y-%m-%d"),
                    predicted_count=round(pred_val, 1),
                    confidence_lower=round(lower_val, 1),
                    confidence_upper=round(upper_val, 1)
                )
            )
            
    except Exception as e:
        logger.warning(f"ARIMA fitting failed: {e}. Falling back to Exponential Moving Average & Trend.")
        # Fallback: Exponential Moving Average + linear trend projection
        # Calculate moving average and trend
        n = len(ts)
        x = np.arange(n)
        y = ts.values
        
        # Fit linear regression trend
        slope, intercept = np.polyfit(x, y, 1) if n >= 2 else (0.0, y[0] if n >= 1 else 10.0)
        
        # Calculate standard deviation of residuals for confidence limits
        residuals = y - (slope * x + intercept)
        std_err = np.std(residuals) if len(residuals) > 1 else (y[0] * 0.2 if n >= 1 else 3.0)
        
        for i in range(1, months_to_forecast + 1):
            future_idx = n + i - 1
            pred_val = max(0.0, slope * future_idx + intercept)
            # Add some slight smoothing / stabilization factor
            if n >= 3:
                last_ema = ts.ewm(span=3).mean().iloc[-1]
                pred_val = 0.4 * last_ema + 0.6 * pred_val
                
            # Confidence interval
            lower_val = max(0.0, pred_val - (1.28 * std_err * np.sqrt(i)))
            upper_val = pred_val + (1.28 * std_err * np.sqrt(i))
            
            future_date = future_dates[i-1]
            forecast_results.append(
                ForecastPoint(
                    date=future_date.strftime("%Y-%m-%d"),
                    predicted_count=round(pred_val, 1),
                    confidence_lower=round(lower_val, 1),
                    confidence_upper=round(upper_val, 1)
                )
            )
            
    return forecast_results

def generate_mock_forecast(months_to_forecast: int) -> List[ForecastPoint]:
    """Generates simple baseline counts if data is absent."""
    start_date = datetime.now()
    results = []
    base_val = 25.0
    for i in range(1, months_to_forecast + 1):
        future_date = start_date + timedelta(days=30 * i)
        pred_val = base_val + np.random.uniform(-3, 3)
        results.append(
            ForecastPoint(
                date=future_date.strftime("%Y-%m-%d"),
                predicted_count=round(pred_val, 1),
                confidence_lower=round(pred_val * 0.7, 1),
                confidence_upper=round(pred_val * 1.3, 1)
            )
        )
    return results
