import pytest
from app import app
import os
import pandas as pd

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_financials(client, tmp_path):
    # Create a mock CSV file for testing
    data = {
        'year': [2019, 2020],
        'revenue': [1000, 800],
        'cost_of_sales': [600, 500],
        'operating_expenses': [200, 150],
        'gross_profit_margin': [40, 37.5],
        'eps': [2.5, 2.0],
        'net_asset_per_share': [10, 9]
    }
    df = pd.DataFrame(data)
    processed_dir = tmp_path / 'processed'
    processed_dir.mkdir()
    df.to_csv(processed_dir / 'financial_data.csv', index=False)
    
    # Update config to use tmp_path
    app.config['PROCESSED_DATA_DIR'] = str(processed_dir)
    
    response = client.get('/api/financials?year=2019')
    assert response.status_code == 200
    data = response.json['data']
    assert len(data) == 1
    assert data[0]['year'] == 2019
    assert data[0]['revenue'] == 1000