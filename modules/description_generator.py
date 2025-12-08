"""
Générateur de descriptions OPTIMISÉES pour l'algo Vinted
"""

import random

class DescriptionGenerator:
    """Descriptions qui CARTONNENT sur Vinted"""
    
    def __init__(self):
        # Templates optimisés SEO Vinted par type
        self.templates = {
            "pantalon": [
                "{marque_txt}Pantalon {couleur} {style}. Coupe {coupe}, taille parfaitement. {etat_txt}. Parfait pour un look {occasion} ! 👖 Envoi rapide et soigné 📦",
                "{marque_txt}Super pantalon {couleur} {style} ! {etat_txt}, porté {frequence}. Taille nickel, très confortable. Idéal {saison} ! 👌 Expédition rapide 📦",
                "{marque_txt}Pantalon {couleur} de qualité. {etat_txt}, {coupe}. S'associe avec tout ! Look {occasion}. Envoi soigné 📦✨"
            ],
            "jean": [
                "{marque_txt}Jean {couleur} {style}. {etat_txt}, coupe {coupe}. Denim de qualité, très confortable ! 👖 Envoi rapide 📦",
                "{marque_txt}Super jean {couleur} ! {etat_txt}, porté {frequence}. Coupe parfaite, taille bien. Indispensable ! ⭐ Expédition soignée 📦"
            ],
            "t-shirt": [
                "{marque_txt}T-shirt {couleur} {style}. {etat_txt}, {matiere}. Parfait pour l'été ou en layering ! 👕 Envoi rapide 📦",
                "{marque_txt}Tee-shirt {couleur} confortable. {etat_txt}, porté {frequence}. Basique indispensable ! ✨ Expédition soignée 📦"
            ],
            "maillot": [
                "{marque_txt}Maillot {couleur} authentique ! {etat_txt}, {matiere}. Pour les vrais fans ! ⚽ Collector. Envoi rapide 📦",
                "{marque_txt}Maillot de sport {couleur}. {etat_txt}, technologie {tech}. Parfait training ou collection ! 🏆 Expédition soignée 📦"
            ],
            "pull": [
                "{marque_txt}Pull {couleur} tout doux. {etat_txt}, {matiere}. Parfait pour l'automne/hiver ! 🍂 Très chaud. Envoi rapide 📦",
                "{marque_txt}Sweat {couleur} confortable. {etat_txt}, coupe {coupe}. Indispensable garde-robe ! ⭐ Expédition soignée 📦"
            ],
            "chaussures": [
                "{marque_txt}Chaussures {couleur} {style}. {etat_txt}, semelle {semelle}. Très confortables ! 👟 Envoi rapide avec soin 📦",
                "{marque_txt}Basket {couleur} stylée. {etat_txt}, portée {frequence}. Look moderne ! ⭐ Expédition soignée 📦"
            ]
        }
        
        # Variables dynamiques pour naturalité
        self.variables = {
            "style": ["classique", "moderne", "casual", "élégant", "sport", "streetwear"],
            "coupe": ["droite", "slim", "regular", "ajustée", "ample", "confortable"],
            "occasion": ["décontracté", "casual", "chic", "sport", "quotidien", "travail"],
            "saison": ["toute l'année", "été", "mi-saison", "automne-hiver"],
            "frequence": ["peu", "avec soin", "occasionnellement"],
            "matiere": ["coton", "polyester", "mélange coton", "matière agréable"],
            "tech": ["respirant", "anti-transpiration", "performance"],
            "semelle": ["confortable", "antidérapante", "souple", "renforcée"]
        }
        
        # Textes d'état optimisés
        self.etat_texts = {
            "Neuf": "Neuf avec étiquette",
            "Très bon": "Excellent état, comme neuf",
            "Bon": "Très bon état général",
            "Satisfaisant": "Bon état d'usage"
        }
    
    def generate_title(self, product_info):
        """Titre SEO optimisé Vinted"""
        parts = []
        
        # Marque en premier (important pour SEO)
        if product_info.get('marque') not in ['À préciser', 'Non visible']:
            parts.append(product_info['marque'])
        
        # Type
        parts.append(product_info['type'].capitalize())
        
        # Couleur
        if product_info.get('couleur'):
            parts.append(product_info['couleur'])
        
        # Taille
        if product_info.get('taille') not in ['À préciser', 'Non visible']:
            parts.append(f"T.{product_info['taille']}")
        
        # État (important pour visibilité)
        etat_short = {
            "Neuf": "Neuf",
            "Très bon": "TBE",
            "Bon": "BE"
        }
        if product_info['etat'] in etat_short:
            parts.append(etat_short[product_info['etat']])
        
        return " ".join(parts)[:80]
    
    def generate_description(self, product_info, price_info):
        """Description optimisée algo Vinted"""
        
        product_type = product_info['type'].lower()
        
        # Choisir template approprié
        if product_type in self.templates:
            templates = self.templates[product_type]
        elif product_type in ['sweat', 'hoodie']:
            templates = self.templates['pull']
        elif product_type in ['basket', 'bottine']:
            templates = self.templates['chaussures']
        else:
            templates = self.templates.get('pantalon')  # Défaut
        
        template = random.choice(templates)
        
        # Construire les variables
        marque = product_info.get('marque', '')
        marque_txt = f"{marque} - " if marque not in ['À préciser', 'Non visible'] else ""
        
        etat_txt = self.etat_texts.get(product_info['etat'], "Bon état")
        
        # Variables aléatoires pour naturel
        variables = {
            "marque_txt": marque_txt,
            "couleur": product_info['couleur'],
            "etat_txt": etat_txt,
            "style": random.choice(self.variables['style']),
            "coupe": random.choice(self.variables['coupe']),
            "occasion": random.choice(self.variables['occasion']),
            "saison": random.choice(self.variables['saison']),
            "frequence": random.choice(self.variables['frequence']),
            "matiere": random.choice(self.variables['matiere']),
            "tech": random.choice(self.variables['tech']),
            "semelle": random.choice(self.variables['semelle'])
        }
        
        # Générer
        try:
            description = template.format(**variables)
            return description[:300]  # Limite Vinted
        except:
            # Fallback basique
            return f"{marque_txt}{product_type.capitalize()} {product_info['couleur']}. {etat_txt}. Parfait état ! Envoi rapide 📦"
    
    def create_full_listing(self, product_info, price_info):
        """Annonce complète optimisée"""
        
        title = self.generate_title(product_info)
        description = self.generate_description(product_info, price_info)
        
        return {
            "titre": title,
            "description": description,
            "prix": price_info['prix_recommande'],
            "prix_min": price_info['prix_min'],
            "prix_max": price_info['prix_max']
        }
