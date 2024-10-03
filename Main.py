import requests
from bs4 import BeautifulSoup
import csv

# URL de la page du produit
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# Extraction des données
reponse = requests.get(url)
soup = BeautifulSoup(reponse.text, 'html.parser')

# Transformation des données
url_page_produit = url
upc = soup.select("table.table-striped tr:nth-child(1) td")[0].text
titre = soup.select("h1")[0].text
prix_ttc = soup.select("table.table-striped tr:nth-child(4) td")[0].text
prix_ht = soup.select("table.table-striped tr:nth-child(3) td")[0].text
disponibilite = soup.select("table.table-striped tr:nth-child(6) td")[0].text
description_produit = soup.select_one("meta[name='description']")['content'].strip()
categorie = soup.select("ul.breadcrumb li:nth-child(3) a")[0].text.strip()
evaluation = soup.select("p.star-rating")[0]['class'][1]
url_image = "https://books.toscrape.com" + soup.select("img")[0]['src'][5:]

# Traiter la disponibilité pour extraire le nombre
nombre_disponible = ''.join(filter(str.isdigit, disponibilite))

# Stocker les données dans un dictionnaire avec les champs demandés
donnees_livre = {
    "product_page_url": url_page_produit,
    "universal_product_code (upc)": upc,
    "title": titre,
    "price_including_tax": prix_ttc,
    "price_excluding_tax": prix_ht,
    "number_available": nombre_disponible,
    "product_description": description_produit,
    "category": categorie,
    "review_rating": evaluation,
    "image_url": url_image
}

# Chargement des données dans un fichier CSV avec les en-têtes demandées
fichier_csv = "donnees_livre.csv"
with open(fichier_csv, mode='w') as fichier:
    writer = csv.DictWriter(fichier, fieldnames=donnees_livre.keys())
    writer.writeheader()
    writer.writerow(donnees_livre)



