import os

class Config:
    DEBUG = True
    PDF_DIR = os.path.join(os.path.dirname(__file__), 'assets/pdfs')
    PROCESSED_DATA_DIR = os.path.join(os.path.dirname(__file__), 'assets/processed')
    ALLOWED_EXTENSIONS = {'pdf'}