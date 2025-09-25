import os
import pdfplumber
import pandas as pd

def extract_tables_from_pdf(pdf_path):
    """Extract tables from a single PDF file and return as list of DataFrames."""
    tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_tables = page.extract_tables()
                for table in page_tables:
                    # Convert each table into DataFrame
                    df = pd.DataFrame(table)
                    tables.append(df)
    except Exception as e:
        print(f"❌ Error reading {pdf_path}: {e}")
    return tables

def extract_all_tables(root_folder, output_csv="combined_tables.csv"):
    """Walk through subfolders, read PDFs, and extract tables into one CSV."""
    all_dfs = []
    
    for subdir, _, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(subdir, file)
                print(f"📄 Processing: {pdf_path}")
                tables = extract_tables_from_pdf(pdf_path)
                
                for i, df in enumerate(tables):
                    # Add metadata: file + table number
                    df["SourceFile"] = file
                    df["TableIndex"] = i
                    all_dfs.append(df)
    
    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        combined_df.to_csv(output_csv, index=False)
        print(f"✅ Extracted {len(all_dfs)} tables. Saved to {output_csv}")
    else:
        print("⚠️ No tables found in any PDF.")

# Example usage:
if __name__ == "__main__":
    main_folder = "pdf_volumi/"
    extract_all_tables(main_folder, "all_tables.csv")

