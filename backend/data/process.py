import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_financial_data(tables):
    """Process extracted tables into structured financial data."""
    financial_data = {
        'revenue': [], 'cost_of_sales': [], 'operating_expenses': [],
        'gross_profit_margin': [], 'eps': [], 'net_asset_per_share': [], 'year': []
    }
    
    for table in tables:
        try:
            table.columns = table.iloc[0].str.lower().str.replace(' ', '_')
            table = table.drop(0).reset_index(drop=True)
            
            for idx, row in table.iterrows():
                try:
                    year = int(row.get('year', 0))
                    if 2019 <= year <= 2024:
                        financial_data['year'].append(year)
                        financial_data['revenue'].append(float(row.get('total_revenue', 0)))
                        financial_data['cost_of_sales'].append(float(row.get('cost_of_sales', 0)))
                        financial_data['operating_expenses'].append(float(row.get('operating_expenses', 0)))
                        financial_data['eps'].append(float(row.get('earnings_per_share', 0)))
                        financial_data['net_asset_per_share'].append(float(row.get('net_asset_per_share', 0)))
                        
                        revenue = float(row.get('total_revenue', 0))
                        cos = float(row.get('cost_of_sales', 0))
                        gpm = ((revenue - cos) / revenue * 100) if revenue > 0 else 0
                        financial_data['gross_profit_margin'].append(gpm)
                except (ValueError, TypeError):
                    continue
        except Exception as e:
            logger.error(f"Error processing table: {str(e)}")
            continue
    
    return pd.DataFrame(financial_data)

def forecast_metric(data, metric, steps=2):
    """Forecast future values using ARIMA."""
    try:
        series = data[metric].dropna()
        model = ARIMA(series, order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=steps)
        return forecast.tolist()
    except Exception as e:
        logger.error(f"Error forecasting {metric}: {str(e)}")
        return []