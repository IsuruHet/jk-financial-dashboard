from flask import Flask, jsonify, request,send_file
from flask_cors import CORS
from config import Config
from data.extract import extract_tables_from_pdf
from data.process import process_financial_data,process_shareholder_data, forecast_metric
import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

@app.route('/api/extract', methods=['POST'])
def extract_pdfs():
    """Extract data from uploaded PDFs."""
    try:
        files = request.files.getlist('files')
        all_data = []
        shareholder_data = []
        
        for file in files:
            if file.filename.split('.')[-1].lower() not in Config.ALLOWED_EXTENSIONS:
                continue
            file_path = os.path.join(Config.PDF_DIR, file.filename)
            file.save(file_path)
            tables = extract_tables_from_pdf(file_path)
            df,year = process_financial_data(tables)
            sh = process_shareholder_data(tables,year)

            all_data.append(df)
            shareholder_data.append(sh)
        
        if not all_data:
            return jsonify({'status': 'error', 'message': 'No valid data extracted'}), 400
        
        if not shareholder_data:
            return jsonify({'status': 'error', 'message': 'No valid data extracted'}), 400
        
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df = combined_df.groupby('year').mean().reset_index()

        combined_sh = pd.concat(shareholder_data, ignore_index=True)
        combined_sh = combined_sh.sort_values(by='year').reset_index(drop=True)


        
        output_path = os.path.join(Config.PROCESSED_DATA_DIR, 'financial_data.csv')
        combined_df.to_csv(output_path, index=False)

        output_path_sh = os.path.join(Config.PROCESSED_DATA_DIR, 'shareholder_data.csv')
        combined_sh.to_csv(output_path_sh, index=False)
        
        return jsonify({
            'status': 'success',
            'data': combined_df.to_dict(orient='records'),
            'shareholder':combined_sh.to_dict(orient='records')
        })
    except Exception as e:
        logger.error(f"Error in extract_pdfs: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/financials', methods=['GET'])
def get_financials():
    """Get processed financial data with optional filters."""
    try:
        year = request.args.get('year', type=int)
        metric = request.args.get('metric')
        currency = request.args.get('currency', 'LKR')
        
        data_path = os.path.join(Config.PROCESSED_DATA_DIR, 'financial_data.csv')
        if not os.path.exists(data_path):
            return jsonify({'status': 'error', 'message': 'No processed data available'}), 404
        
        df = pd.read_csv(data_path)
        
        if year:
            df = df[df['year'] == year]
        
        if metric:
            df = df[['year', metric]]
        
        if currency == 'USD':
            df[['revenue', 'cost_of_sales', 'operating_expenses', 'eps', 'net_asset_per_share']] *= 0.005
        
        return jsonify({
            'status': 'success',
            'data': df.to_dict(orient='records')
        })
    except Exception as e:
        logger.error(f"Error in get_financials: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/forecast', methods=['GET'])
def get_forecast():
    """Get forecast for a specific metric."""
    try:
        metric = request.args.get('metric', 'revenue')
        data_path = os.path.join(Config.PROCESSED_DATA_DIR, 'financial_data.csv')
        
        if not os.path.exists(data_path):
            return jsonify({'status': 'error', 'message': 'No processed data available'}), 404
        
        df = pd.read_csv(data_path)
        forecast_values = forecast_metric(df, metric)
        
        return jsonify({
            'status': 'success',
            'metric': metric,
            'forecast': forecast_values
        })
    except Exception as e:
        logger.error(f"Error in get_forecast: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/annotations', methods=['GET'])
def get_annotations():
    """Generate annotations for key events."""
    annotations = [
        {'year': 2019, 'event': 'Easter Sunday attacks impacted Leisure sector'},
        {'year': 2020, 'event': 'COVID-19 pandemic caused revenue decline'},
        {'year': 2021, 'event': 'Tax policy changes affected profitability'}
    ]
    return jsonify({
        'status': 'success',
        'annotations': annotations
    })

@app.route('/api/download', methods=['GET'])
def download_csv():
    try:
        csv_path = os.path.join(Config.PROCESSED_DATA_DIR, 'financial_data.csv')
        if not os.path.exists(csv_path):
            return jsonify({'status': 'error', 'message': 'CSV not found'}), 404
        return send_file(csv_path, mimetype='text/csv', as_attachment=True)
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)