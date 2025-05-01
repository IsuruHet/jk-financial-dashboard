import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_number(value):
    
    """Convert financial string to float. Handles commas, parentheses, and missing values."""
    if not isinstance(value, str):
        return value
    value = value.replace(',', '').strip()
    if value.startswith('(') and value.endswith(')'):
        value = '-' + value[1:-1]
    try:
        return float(value)
    except ValueError:
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

    # Define the keywords for both financial categories
    keywords_1 = ['for the year ended 31 march','total revenue', 'cost of sales', 'gross profit', 'other operating income', 'basic']
    keywords_2 = ['net assets per share** (rs.)','net assets per share* (rs.)','basic earnings per share (rs.)']

    # Initialize variables 
    year = None
    revenue = None
    cost_of_sales = None
    operating_expenses = None
    eps = None
    net_asset_per_share = None
    gross_profit = None     
          
    for i, table in enumerate(tables):
        # Convert all cells to lowercase for matching
        table_lower = table.astype(str).apply(lambda col: col.str.lower())
    
        # Dictionary to store matched values
        matched_rows = {}

        for keyword in keywords_1:
            # Find rows containing the keyword
            row = table[table_lower.apply(lambda r: keyword in ' '.join(r), axis=1)]
            if not row.empty:
                matched_rows[keyword] = row.iloc[0, 3]

        if matched_rows:
            print(f"\n✅ Table {i+1} contains financial rows:")
            for k, v in matched_rows.items():
                print(f"{k.title()} (column 3): {v}")
                match k.title(): 
                    case "For The Year Ended 31 March": year = v 
                    case "Total Revenue": revenue = v 
                    case "Cost Of Sales": cost_of_sales = v 
                    case "Gross Profit": gross_profit = v 
                    case "Other Operating Income": operating_expenses = v 
                    case "Basic": eps = v
            #display(table)  # Show the full table (optional)
            break
        else:
            print(f"Table {i+1} does not contain any of the target keywords.")



    # Loop through all the tables
    for i, table in enumerate(tables):
        # Convert all cells to lowercase for matching
        table_lower = table.astype(str).apply(lambda col: col.str.lower())
    
        # Dictionary to store matched values
        matched_rows = {}

        for keyword in keywords_2:
            # Find rows containing the keyword
            row = table[table_lower.apply(lambda r: keyword in ' '.join(r), axis=1)]
            if not row.empty:
                matched_rows[keyword] = row.iloc[0, 1]

        if matched_rows:
            print(f"\n✅ Table {i+1} contains financial rows:")
            for k, v in matched_rows.items():
                print(f"{k.title()} (column ): {v}")
                if(k.title()== "Basic Earnings Per Share (Rs.)"):
                    eps = v
                else:
                    net_asset_per_share = v
                

               
            #display(table)  # Show the full table (optional)
            break
        else:
            print(f"Table {i+1} does not contain any of the target keywords.")
                    

                    

            # Append to financial_data if year is found
    if year is not None:
        financial_data['year'].append(year)
        financial_data['revenue'].append(clean_number(revenue))
        financial_data['cost_of_sales'].append(clean_number(cost_of_sales))
        financial_data['operating_expenses'].append(clean_number(operating_expenses))
        financial_data['eps'].append(clean_number(eps))
        financial_data['net_asset_per_share'].append(clean_number(net_asset_per_share))
        financial_data['gross_profit_margin'].append(clean_number(gross_profit))

    
    # Create DataFrame
    df = pd.DataFrame(financial_data)
    if df.empty:
        logger.warning("Warning: No financial data extracted!")
    return df,year


def process_shareholder_data(tables,y):
    # Initialize a list to store extracted data
    shareholders_data = []

    for i, table in enumerate(tables):
        # Convert all cells to lowercase and strip spaces
        table_lower = table.astype(str).map(lambda x: x.strip().lower())

        # Check each row
        for _, row in table_lower.iterrows():
            row_list = row.tolist()
            number_of_count = sum("number of" in cell for cell in row_list)
            percent_count = sum("%" in cell for cell in row_list)
        
            if number_of_count == 2 and percent_count == 2:
                print("Row has at least two 'number of' and two '%' entries")
                #display(table)

                # Extract data starting from row 1 (assuming row 0 is header)
                share_holder_names = table.iloc[1:, 0].astype(str).str.strip().tolist()
                share_percentage = table.iloc[1:, 2].astype(str).str.strip().tolist()
                year = [y] * len(share_holder_names)

                for name, percentage, yr in zip(share_holder_names, share_percentage, year):
                    shareholders_data.append([yr, name, percentage])

                print(year)
                print(share_holder_names)
                print(share_percentage)
       
                break  # stop checking more rows in the same table

  
    ds = pd.DataFrame(shareholders_data, columns=["year", "shareholder_name", "share_percentage"])
    return ds

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
