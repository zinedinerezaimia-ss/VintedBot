"""
Générateur de descriptions OPTIMISÉES pour l'algo Vinted
"""

import random

class DescriptionGenerator:
    """Descriptions qui CARTONNENT sur Vinted"""
    
    def __init__(self):
        # Templates optimisés SEO Vinted COMPLETS
        self.templates = {
            "maillot": [
                "{marque_txt}Maillot {couleur} authentique et officiel ! {etat_txt}, porté {frequence}. {tech_txt}. Collector pour les vrais fans ! ⚽ Logo et écusson en parfait état. Idéal pour supporter votre équipe ou pour votre collection ! Taille {taille_txt}. Envoi rapide et soigné en colis protégé 📦✨",
                "{marque_txt}Superbe maillot de football {couleur} ! {etat_txt}, {tech_txt}. Parfait pour le sport ou en casual. Logo officiel, matière respirante et confortable. Pour les passionnés de foot ! ⚽ Taille {taille_txt}. Expédition rapide et soignée 📦",
                "{marque_txt}Maillot {couleur} collector ! {etat_txt}. Technologie {tech_txt} pour performances optimales. Écusson et sponsors intacts. Parfait état, porté {frequence}. Un must-have pour tout fan ! ⚽🏆 Taille {taille_txt}. Envoi protégé 📦"
            ],
            "t-shirt": [
                "{marque_txt}T-shirt {couleur} {style}. {etat_txt}, {matiere}. Coupe {coupe}, très confortable au quotidien. Parfait pour un look {occasion} ! S'associe facilement avec tout. Basique indispensable de votre garde-robe. 👕 Taille {taille_txt}. Envoi rapide 📦",
                "{marque_txt}Tee-shirt {couleur} de qualité. {etat_txt}, matière {matiere} agréable à porter. Coupe {coupe}, tombe parfaitement. Idéal {saison}. Look casual et moderne ! ✨ Taille {taille_txt}. Expédition soignée 📦"
            ],
            "pantalon": [
                "{marque_txt}Pantalon {couleur} {style}. {etat_txt}, coupe {coupe} moderne. Matière {matiere} confortable et résistante. Taille parfaitement, s'adapte à toutes les morphologies. Parfait pour un look {occasion} ! Poches fonctionnelles. 👖 Taille {taille_txt}. Envoi rapide et soigné 📦",
                "{marque_txt}Super pantalon {couleur} ! {etat_txt}, porté {frequence}. Coupe {coupe}, très confortable toute la journée. Matière {matiere} de qualité. S'associe avec tout ! Indispensable garde-robe. 👌 Taille {taille_txt}. Expédition protégée 📦"
            ],
            "chaussures": [
                "{marque_txt}Chaussures {couleur} {style}. {etat_txt}, semelle {semelle} en bon état. Intérieur propre et bien entretenu. Très confortables, portées {frequence}. Parfaites pour {occasion} ! Pointure {taille_txt}. Look moderne et élégant. 👟 Envoi en colis renforcé 📦",
                "{marque_txt}Paire de chaussures {couleur} de qualité ! {etat_txt}. Semelle {semelle}, maintien parfait. Très bon confort de marche. Style {style}, s'associe avec tout ! 👞 Pointure {taille_txt}. Expédition rapide et protégée 📦"
            ],
            "bottine": [
                "{marque_txt}Bottines {couleur} stylées ! {etat_txt}, cuir/matière {matiere}. Semelle {semelle}, talon {talon}. Très confortables, portées {frequence}. Parfaites pour {saison} ! Look élégant et moderne. 👢 Pointure {taille_txt}. Envoi soigné 📦",
                "{marque_txt}Jolies bottines {couleur}. {etat_txt}. Finitions soignées, semelle {semelle}. Confort assuré toute la journée. Style {style}, indispensable ! ⭐ Pointure {taille_txt}. Expédition protégée 📦"
            ]
        }
        
        # Variables dynamiques enrichies
        self.variables = {
            "style": ["classique", "moderne", "casual", "élégant", "sport", "streetwear", "tendance", "intemporel"],
            "coupe": ["droite", "slim", "regular", "ajustée", "ample", "confortable", "moderne"],
            "occasion": ["décontracté", "casual", "chic", "sport", "quotidien", "travail", "sorties"],
            "saison": ["toute l'année", "été", "mi-saison", "automne-hiver", "toutes saisons"],
            "frequence": ["peu", "avec soin", "occasionnellement", "quelques fois"],
            "matiere": ["coton", "polyester", "mélange coton", "matière agréable", "tissu respirant"],
            "tech": ["respirant Dri-FIT", "anti-transpiration", "performance", "Climacool", "respirant"],
            "semelle": ["confortable", "antidérapante", "souple", "renforcée", "adhérente"],
            "talon": ["moyen", "confortable", "stable", "3-4cm"]
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
        
        taille = product_info.get('taille', 'À préciser')
        taille_txt = taille if taille != 'À préciser' else 'voir photos'
        
        # Variables aléatoires pour naturel
        variables = {
            "marque_txt": marque_txt,
            "couleur": product_info['couleur'],
            "etat_txt": etat_txt,
            "taille_txt": taille_txt,
            "style": random.choice(self.variables['style']),
            "coupe": random.choice(self.variables['coupe']),
            "occasion": random.choice(self.variables['occasion']),
            "saison": random.choice(self.variables['saison']),
            "frequence": random.choice(self.variables['frequence']),
            "matiere": random.choice(self.variables['matiere']),
            "tech_txt": random.choice(self.variables['tech']),
            "semelle": random.choice(self.variables['semelle']),
            "talon": random.choice(self.variables['talon'])
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
