import camelot

def extract_tables_from_pdf(file_path):
    tables = camelot.read_pdf(file_path, pages='all', flavor='stream') 
    print(f"Total tables extracted: {tables.n}")
    
    extracted_data = []
    
    for i, table in enumerate(tables):
        df = table.df  # pandas dataframe
        print(f"Table {i} Preview:")
        print(df.head())
        extracted_data.append(df)
    
    return extracted_data

if __name__ == "__main__":
    # Test it
    pdf_path = 'assets/508_1590052852777.pdf'
    extract_tables_from_pdf(pdf_path)
