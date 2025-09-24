import requests
from bs4 import BeautifulSoup
import os

# URL di partenza
#BASE_URL = "https://www.regione.sicilia.it/istituzioni/regione/strutture-regionali/presidenza-regione/autorita-bacino-distretto-idrografico-sicilia/gennaio-1"

def base_url(mese):
    if mese == "gennaio":
        numero = '1'
    else:
        numero = '0'

    #base_url = f"https://www.regione.sicilia.it/istituzioni/regione/strutture-regionali/presidenza-regione/autorita-bacino-distretto-idrografico-sicilia/{mese}-{numero}"
    base_url = f"https://www.regione.sicilia.it/istituzioni/regione/strutture-regionali/presidenza-regione/autorita-bacino-distretto-idrografico-sicilia/{mese}"
    return base_url


mesi = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", 
        "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]


def get_data(mese):

    #DOWNLOAD_DIR = f"pdf_volumi/{mese}"
    DOWNLOAD_DIR = f"pdf_volumi/2024"
    # Crea cartella per i PDF
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Scarica la pagina iniziale
    resp = requests.get(base_url(mese))
    soup = BeautifulSoup(resp.text, "html.parser")

    # Trova tutti i link ai PDF
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.lower().endswith(".pdf"):
            if href.startswith("http"):
                links.append(href)
            else:
                links.append("https://www.regione.sicilia.it" + href)

    print(f"Trovati {len(links)} PDF per {mese}")

    # Scarica i PDF trovati
    pdf_files = []
    for url in links:
        filename = os.path.join(DOWNLOAD_DIR, url.split("/")[-1])
        if not os.path.exists(filename):
            r = requests.get(url)
            with open(filename, "wb") as f:
                f.write(r.content)
        pdf_files.append(filename)


if __name__ == '__main__':

    for mese in mesi:
        get_data(mese)
