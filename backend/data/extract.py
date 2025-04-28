import camelot
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_tables_from_pdf(file_path):
    """Extract tables from a PDF using Camelot."""
    try:
        tables = camelot.read_pdf(file_path, pages='all', flavor='stream')
        logger.info(f"Extracted {tables.n} tables from {file_path}")
        return [table.df for table in tables]
    except Exception as e:
        logger.error(f"Error extracting tables from {file_path}: {str(e)}")
        return []