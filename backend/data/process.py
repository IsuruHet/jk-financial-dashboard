import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_column_name(name):
    """Utility to clean messy column names."""
    return str(name).strip().lower().replace(' ', '_').replace('\n', '').replace('.', '').replace('/', '_')

def match_column(available_columns, keywords):
    """Try to match closest column name based on list of keywords."""
    for col in available_columns:
        for keyword in keywords:
            if keyword in col:
                return col
    return None

def process_financial_data(tables):
    """Extract financial metrics from the messy PDFs into clean structured DataFrame."""
    financial_data = {
        'year': [],
        'revenue': [],
        'cost_of_sales': [],
        'operating_expenses': [],
        'eps': [],
        'net_asset_per_share': [],
        'gross_profit_margin': [],
    }

    for table in tables:
        try:
            # Clean table headers
            table.columns = table.iloc[0].apply(clean_column_name)
            table = table.drop(0).reset_index(drop=True)
            available_columns = list(table.columns)

            # Try matching best-fit columns
            year_col = match_column(available_columns, ['year', 'year_ended', 'financial_year'])
            revenue_col = match_column(available_columns, ['revenue', 'total_revenue'])
            cost_col = match_column(available_columns, ['cost_of_sales', 'cost_of_revenue'])
            opex_col = match_column(available_columns, ['operating_expenses', 'administrative_expenses', 'expenses'])
            eps_col = match_column(available_columns, ['earnings_per_share', 'eps'])
            net_asset_col = match_column(available_columns, ['net_asset_per_share', 'nav_per_share'])

            if not year_col:
                continue  # Skip if no year column found

            for idx, row in table.iterrows():
                try:
                    year = int(str(row.get(year_col)).split()[0])  # Pick only first part if mixed
                    if 2019 <= year <= 2025:
                        revenue = float(str(row.get(revenue_col)).replace(',', '').strip() or 0)
                        cost_of_sales = float(str(row.get(cost_col)).replace(',', '').strip() or 0)
                        operating_expenses = float(str(row.get(opex_col)).replace(',', '').strip() or 0)
                        eps = float(str(row.get(eps_col)).replace(',', '').strip() or 0)
                        net_asset_per_share = float(str(row.get(net_asset_col)).replace(',', '').strip() or 0)

                        gpm = ((revenue - cost_of_sales) / revenue * 100) if revenue else 0

                        financial_data['year'].append(year)
                        financial_data['revenue'].append(revenue)
                        financial_data['cost_of_sales'].append(cost_of_sales)
                        financial_data['operating_expenses'].append(operating_expenses)
                        financial_data['eps'].append(eps)
                        financial_data['net_asset_per_share'].append(net_asset_per_share)
                        financial_data['gross_profit_margin'].append(gpm)
                except (ValueError, TypeError) as e:
                    logger.warning(f"Row skipped: {e}")
        except Exception as e:
            logger.error(f"Table processing failed: {e}")

    df = pd.DataFrame(financial_data)
    if df.empty:
        logger.warning("Warning: No financial data extracted!")
    return df

def forecast_metric(df, metric, steps=3):
    """Forecast future values of a metric using ARIMA."""
    try:
        series = df[metric].dropna()
        if len(series) < 3:
            logger.warning(f"Not enough data to forecast {metric}")
            return []
        model = ARIMA(series, order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=steps)
        return forecast.round(2).tolist()
    except Exception as e:
        logger.error(f"Forecasting failed for {metric}: {e}")
        return []
