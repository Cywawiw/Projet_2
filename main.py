import requests
from bs4 import BeautifulSoup
import csv
import os
import re

# URL de base
base_url = "https://books.toscrape.com/"
category_url = "catalogue/category/books/"

# Fonction pour nettoyer les noms de fichiers
def clean_filename(filename):
    # Remplacer les caractères invalides par des underscores
    filename = re.sub(r'[<>:"/\\|?*\'’“”]', '_', filename)  # Supprime les caractères invalides
    # Limite à 150 caractères pour assurer un chemin valide
    return filename[:150]

# Fonction pour télécharger les images
def download_image(image_url, save_path):
    # Créer le dossier avant de télécharger l'image
    folder = os.path.dirname(save_path)
    os.makedirs(folder, exist_ok=True)  # Créer le dossier de manière récursive

    # Télécharger l'image
    response = requests.get(image_url)
    if response.status_code == 200:
        try:
            with open(save_path, 'wb') as file:  # 'wb' pour écrire en mode binaire
                file.write(response.content)
        except Exception as e:
            print(f"Erreur lors de l'enregistrement de l'image : {e}")

# Fonction pour extraire les informations détaillées d'un livre
def extract_book_details(book_url):
    response = requests.get(book_url)
    response.encoding = 'utf-8'  # Forcer l'encodage UTF-8
    soup = BeautifulSoup(response.text, 'html.parser')

    # Transformation des données
    url_page_produit = book_url
    upc = soup.select("table.table-striped tr:nth-child(1) td")[0].text
    titre = soup.select("h1")[0].text
    prix_ttc = soup.select("table.table-striped tr:nth-child(4) td")[0].text
    prix_ht = soup.select("table.table-striped tr:nth-child(3) td")[0].text
    disponibilite = soup.select("table.table-striped tr:nth-child(6) td")[0].text
    description_produit = soup.select_one("meta[name='description']")['content'].strip()
    categorie = soup.select("ul.breadcrumb li:nth-child(3) a")[0].text.strip()
    evaluation = soup.select("p.star-rating")[0]['class'][1]
    url_image = base_url + soup.select("img")[0]['src'][5:]

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

    return donnees_livre

# Fonction pour extraire les livres d'une catégorie donnée
def extract_books_from_category(category_url, category_name):
    all_books = []
    current_page = 1

    while True:
        url = f"{category_url}/page-{current_page}.html" if current_page > 1 else f"{category_url}/index.html"
        response = requests.get(url)
        response.encoding = 'utf-8'  # Forcer l'encodage UTF-8
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraire les livres de la page
        books = soup.find_all('article', class_='product_pod')
        for book in books:
            book_url = base_url + "catalogue/" + book.h3.a['href'].replace('../../../', '')
            book_details = extract_book_details(book_url)
            all_books.append(book_details)

            # Nettoyer le titre pour créer un nom de fichier valide
            safe_title = clean_filename(book_details['title'])
            # Créer le chemin du fichier pour l'image avec les caractères nettoyés
            image_filename = f"output/{category_name.replace(' ', '_').lower()}/{safe_title}.jpg"

            download_image(book_details['image_url'], image_filename)

        # Vérifier s'il y a une page suivante
        next_button = soup.find('li', class_='next')
        if not next_button:
            break  # Pas de page suivante, sortir de la boucle
        current_page += 1

    return all_books

# Fonction pour charger les livres dans un fichier CSV
def save_to_csv(books, category_name):
    # Créer le dossier de sortie pour la catégorie s'il n'existe pas
    os.makedirs(f"output/{category_name.replace(' ', '_').lower()}", exist_ok=True)

    filename = f"output/{category_name.replace(' ', '_').lower()}/{category_name.replace(' ', '_').lower()}.csv"
    keys = books[0].keys()  # Utiliser les clés du premier livre comme en-têtes de colonne
    with open(filename, 'w', newline='', encoding='utf-8-sig') as fichier:
        writer = csv.DictWriter(fichier, fieldnames=keys)
        writer.writeheader()
        writer.writerows(books)

# Fonction pour extraire toutes les catégories depuis la page d'accueil
def get_all_categories():
    response = requests.get(base_url + "index.html")
    response.encoding = 'utf-8'  # Forcer l'encodage UTF-8
    soup = BeautifulSoup(response.text, 'html.parser')
    categories = soup.find('ul', class_='nav nav-list').find('ul').find_all('a')

    category_links = {}
    for category in categories:
        category_name = category.text.strip()
        category_link = base_url + category['href']
        category_links[category_name] = category_link

    return category_links

# Lancer le scraping pour toutes les catégories
def main():
    category_links = get_all_categories()

    for category_name, category_link in category_links.items():
        books_data = extract_books_from_category(category_link.replace('index.html', ''), category_name)
        save_to_csv(books_data, category_name)

# Appel direct à la fonction principale
main()
