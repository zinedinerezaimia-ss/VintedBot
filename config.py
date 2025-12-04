import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de l'API Claude (gratuite avec limites)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Configuration Vinted
VINTED_EMAIL = os.getenv("VINTED_EMAIL", "")
VINTED_PASSWORD = os.getenv("VINTED_PASSWORD", "")

# Dossiers
TEMP_IMAGE_FOLDER = "data/temp_images"
os.makedirs(TEMP_IMAGE_FOLDER, exist_ok=True)

# Sites à scraper pour les prix
PRICE_SOURCES = [
    "https://www.vinted.fr/vetements",
    "https://www.leboncoin.fr/recherche?category=15&text=",
    "https://www.vestiairecollective.com/search/"
]

# Catégories Vinted (simplifié)
VINTED_CATEGORIES = {
    "t-shirt": 1,
    "pull": 2,
    "pantalon": 3,
    "robe": 4,
    "chaussures": 5,
    "accessoires": 6
}