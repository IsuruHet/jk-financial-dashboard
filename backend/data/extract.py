import camelot
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_tables_from_pdf(file_path):
    """
    Extract useful financial tables (like income statements) from a PDF.
    We only scan page range 170-end to avoid unnecessary noise.
    """
    try:
        # Focus on financial statements pages
        tables = camelot.read_pdf(file_path, pages='170-end', flavor='stream')

        if tables.n == 0:
            logger.warning(f"No tables found in {file_path}")
            return []

        useful_tables = []
        keywords = ['total revenue', 'cost of sales', 'operating expenses', 'gross profit','earnings per share', 'net asset']

        for i, table in enumerate(tables):
            df = table.df
            # Flatten table text
            table_text = ' '.join(df.apply(lambda row: ' '.join(row), axis=1).tolist()).lower()

            if any(keyword in table_text for keyword in keywords):
                logger.info(f"Selected table {i} (financial content detected)")
                useful_tables.append(df)
            else:
                logger.info(f"Skipped table {i} (non-financial content)")

        if not useful_tables:
            logger.warning(f"No financial tables found in {file_path}")

        return useful_tables

    except Exception as e:
        logger.error(f"Error extracting tables from {file_path}: {str(e)}")
        return []
