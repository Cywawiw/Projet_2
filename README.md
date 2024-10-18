# Projet de Scraping de Livres sur Books to Scrape

Ce projet permet de scraper les informations sur les livres depuis le site [Books to Scrape](http://books.toscrape.com/) et de les enregistrer dans des fichiers CSV, ainsi que de télécharger les images associées dans des dossiers correspondant aux catégories de livres.

## Fonctionnalités

- Scraper les informations détaillées sur les livres (titre, catégorie, prix, disponibilité, évaluation, etc.).
- Télécharger les images des livres et les enregistrer localement dans des dossiers organisés par catégories.
- Enregistrer les informations des livres dans des fichiers CSV organisés par catégories.

## Prérequis

- Python 3.12
- Les bibliothèques Python suivantes :
  - `requests`
  - `beautifulsoup4`

## Installation

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/votre-utilisateur/nom-du-projet.git
   cd Utilisez les bases de Python pour l'analyse de marché
   ```
 2.Créer un environnement virtuel :
  ```bash
    python -m venv venv
  ```
3. Activer l'environnement virtuel:
   -Sur Windows, exécutez : `venv\Scripts\activate`
   -Sur macOS et Linux, exécutez :`source venv/bin/activate`

 4. Installer les dépendances
    ```bash
    pip install -r requirements.txt
    ```
## Utilisation
Exécuter le script principal :
  ```bash
  python main.py
  ```
Le script lancera le scraping de toutes les catégories de livres disponibles sur le site et enregistrera les données et les images correspondantes dans le répertoire output.
Les fichiers CSV seront enregistrés dans le dossier `output` sous la forme `output/nom_de_la_catégorie/nom_de_la_catégorie.csv`.
Les images seront enregistrées dans le dossier correspondant à chaque catégorie, par exemple `output/nom_de_la_catégorie/nom_du_livre.jpg`.


