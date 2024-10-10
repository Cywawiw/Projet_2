import requests
from bs4 import BeautifulSoup
import csv

# URL de base
base_url = "https://books.toscrape.com/"
category_url = "catalogue/category/books/"


# Fonction pour nettoyer les chaînes de caractères et convertir les prix en float
def clean_price(price_str):
    # Enlever les caractères indésirables, comme 'Â'
    cleaned_str = price_str.replace('Â', '').strip()

    # Conversion en float pour les opérations numériques
    price_value = float(cleaned_str.replace('£', ''))
    return f"£{price_value:.2f}"  # Format avec symbole et deux décimales


# Fonction pour extraire les informations détaillées d'un livre depuis sa page
def extract_book_details(book_url):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Transformation des données
    url_page_produit = book_url
    upc = soup.select("table.table-striped tr:nth-child(1) td")[0].text
    titre = soup.select("h1")[0].text
    prix_ttc = clean_price(soup.select("table.table-striped tr:nth-child(4) td")[0].text)  # Nettoyer ici
    prix_ht = clean_price(soup.select("table.table-striped tr:nth-child(3) td")[0].text)  # Nettoyer ici
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
        "price_including_tax": prix_ttc,  # Prix comme float avec symbole
        "price_excluding_tax": prix_ht,  # Prix comme float avec symbole
        "number_available": nombre_disponible,
        "product_description": description_produit,
        "category": categorie,
        "review_rating": evaluation,
        "image_url": url_image
    }

    return donnees_livre


# Fonction pour extraire les livres d'une catégorie donnée
def extract_books_from_category(category_url):
    all_books = []
    current_page = 1

    while True:
        url = f"{category_url}/page-{current_page}.html" if current_page > 1 else f"{category_url}/index.html"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraire les livres de la page
        books = soup.find_all('article', class_='product_pod')
        for book in books:
            book_url = base_url + "catalogue/" + book.h3.a['href'].replace('../../../', '')
            book_details = extract_book_details(book_url)
            all_books.append(book_details)

        # Vérifier s'il y a une page suivante
        next_button = soup.find('li', class_='next')
        if not next_button:
            break  # Pas de page suivante, sortir de la boucle
        current_page += 1

    return all_books


# Fonction pour charger les livres dans un fichier CSV
def save_to_csv(books, category_name):
    filename = f"{category_name.replace(' ', '_').lower()}.csv"
    keys = books[0].keys()  # Utiliser les clés du premier livre comme en-têtes de colonne
    with open(filename, 'w', newline='', encoding='utf-8') as fichier:
        writer = csv.DictWriter(fichier, fieldnames=keys)
        writer.writeheader()
        writer.writerows(books)
    print(f"CSV créé pour la catégorie '{category_name}' : {filename}")


# Fonction pour extraire toutes les catégories depuis la page d'accueil
def get_all_categories():
    response = requests.get(base_url + "index.html")
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
        print(f"Scraping catégorie : {category_name}")
        books_data = extract_books_from_category(category_link.replace('index.html', ''))
        save_to_csv(books_data, category_name)

# Appel direct à la fonction principale
main()
