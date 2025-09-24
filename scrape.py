import os
import requests
from datetime import date, timedelta

# Output folder
output_dir = "downloads"
os.makedirs(output_dir, exist_ok=True)

# Date range: from 2020-01-01 to today
start_date = date(2025, 1, 1)
end_date = date.today()

delta = timedelta(days=1)
current_date = start_date

while current_date <= end_date:
    # Format year-month folder and full date
    year_month = current_date.strftime("%Y-%m")
    file_date = current_date.strftime("%Y.%m.%d")
    file_day = current_date.strftime("%dd")
    file_month = int(current_date.strftime("%m"))

    months = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug"]
    
    # Construct URL
    url = f"https://www.regione.sicilia.it/sites/default/files/{year_month}/{file_date}_A_Tabella_volumi_invasi_0.pdf"
    url = f"https://www.regione.sicilia.it/sites/default/files/{year_month}/_Situazione_volumi_invasati_AdB_Sicilia_{file_day}_{months[file_month]}_25.pdf"

    
    # Output filename
    filename = os.path.join(output_dir, f"{file_date}_A_Tabella_volumi_invasi.pdf")
    
    # Skip if already downloaded
    if os.path.exists(filename):
        current_date += delta
        continue
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200 and response.headers.get("Content-Type") == "application/pdf":
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"No file for {file_date}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    
    current_date += delta
