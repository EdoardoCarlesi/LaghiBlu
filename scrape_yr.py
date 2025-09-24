import requests
from bs4 import BeautifulSoup
import os

def download_pdfs_from_page(page_url, base_domain=None, download_dir="2012"):
    os.makedirs(download_dir, exist_ok=True)
    resp = requests.get(page_url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    pdf_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.lower().endswith(".pdf"):
            if href.startswith("http"):
                pdf_links.append(href)
            else:
                # If relative, prepend base domain if provided
                if base_domain:
                    pdf_links.append(base_domain.rstrip("/") + "/" + href.lstrip("/"))
                else:
                    pdf_links.append(href)
    print(f"Found {len(pdf_links)} PDF links on {page_url}")
    for url in pdf_links:
        fname = url.split("/")[-1]
        path = os.path.join(download_dir, fname)
        if os.path.exists(path):
            print(f"Already exists: {path}")
            continue
        print(f"Downloading {url} → {path}")
        r = requests.get(url)
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)
    print("Done.")

if __name__ == "__main__":
    year = '2023'
    #page = f"https://www.regione.sicilia.it/istituzioni/regione/strutture-regionali/presidenza-regione/autorita-bacino-distretto-idrografico-sicilia/volumi-invasi-anno-{year}"
    page = "https://www.regione.sicilia.it/istituzioni/regione/strutture-regionali/presidenza-regione/autorita-bacino-distretto-idrografico-sicilia/volumi-invasi-anno-2023"
    base = "https://www.regione.sicilia.it"
    download_pdfs_from_page(page, base_domain=base, download_dir=f"{year}")
