import pandas as pd

def search_csv(input_csv, search_string, output_csv="filtered_rows.csv"):
    """
    Reads a CSV, filters rows that contain a given string (case-insensitive),
    and saves them into a new CSV file.
    """
    # Read CSV into DataFrame
    df = pd.read_csv(input_csv, dtype=str)  # dtype=str ensures all values are treated as text
    
    # Convert everything to lowercase for comparison
    mask = df.apply(lambda row: row.astype(str).str.lower().str.contains(search_string.lower(), na=False)).any(axis=1)
    
    # Filter rows
    filtered_df = df[mask]
    
    # Save to CSV
    filtered_df.to_csv(output_csv, index=False)
    
    print(f"✅ Found {len(filtered_df)} matching rows. Saved to {output_csv}")
    return filtered_df


# Example usage:
if __name__ == "__main__":
    input_file = "csv_volumi/all_tables.csv"
    search_term = "ANCIPA"   # the string to search for
    search_csv(input_file, search_term, "ANCIPA_rows.csv")
