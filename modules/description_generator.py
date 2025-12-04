"""
Générateur de descriptions amélioré avec templates intelligents
"""

import requests
import json
import random

class DescriptionGenerator:
    """Génère des descriptions attractives"""
    
    def __init__(self):
        self.api_url = "https://api.airforce/v1/chat/completions"
        
        # Templates de descriptions par type
        self.templates = {
            "t-shirt": [
                "{marque} {couleur} en {etat_fr}. {details}. Parfait pour un look décontracté ! Envoi rapide 📦",
                "T-shirt {marque} {couleur} {etat_fr}. {details}. Idéal pour toutes les occasions ! 👕",
                "Superbe t-shirt {couleur} {marque}. {details}. État impeccable, envoi soigné ! ✨"
            ],
            "maillot": [
                "Maillot {marque} {couleur}. {details}. Pour les vrais fans ! ⚽ Envoi rapide 📦",
                "{marque} - {details}. {etat_fr}, idéal pour supporter votre équipe ! 🏆",
                "Magnifique maillot {couleur}. {details}. État {etat_fr}, envoi soigné ! ⚽"
            ],
            "pull": [
                "Pull {marque} {couleur} tout doux. {details}. Parfait pour l'hiver ! ❄️ Envoi rapide 📦",
                "{marque} {couleur} {etat_fr}. {details}. Chaleureux et confortable ! 🧶",
                "Joli pull {couleur}. {details}. État {etat_fr}, envoi soigné ! ✨"
            ],
            "pantalon": [
                "Pantalon {marque} {couleur}. {details}. Coupe parfaite ! 👖 Envoi rapide 📦",
                "{marque} {couleur} {etat_fr}. {details}. Style et confort ! ✨",
                "Super pantalon {couleur}. {details}. État {etat_fr}, envoi soigné ! 👌"
            ],
            "default": [
                "{type} {marque} {couleur}. {details}. État {etat_fr} ! Envoi rapide 📦",
                "Article {couleur} {marque}. {details}. Parfait état, envoi soigné ! ✨",
                "{type} {couleur} en {etat_fr}. {details}. N'hésitez pas ! 👌"
            ]
        }
    
    def generate_title(self, product_info):
        """Génère un titre optimisé"""
        parts = []
        
        # Marque en premier si identifiée
        if product_info.get('marque') and product_info['marque'] not in ["À préciser", "Non identifiée"]:
            parts.append(product_info['marque'])
        
        # Type de produit
        type_clean = product_info['type'].capitalize()
        if type_clean not in ["Vêtement", "Article"]:
            parts.append(type_clean)
        
        # Couleur
        if product_info.get('couleur') and product_info['couleur'] != "À préciser":
            parts.append(product_info['couleur'])
        
        # Taille si disponible
        if product_info.get('taille') and product_info['taille'] not in ["À préciser", "Non visible"]:
            parts.append(f"T.{product_info['taille']}")
        
        # État
        if product_info.get('etat'):
            parts.append(f"- {product_info['etat']}")
        
        # Si le titre est trop court, ajouter des infos
        title = " ".join(parts)
        if len(title) < 15:
            title = f"{product_info['type'].capitalize()} {product_info['couleur']} - {product_info['etat']}"
        
        return title[:80]  # Limite Vinted
    
    def generate_description(self, product_info, price_info):
        """Génère une description avec fallback intelligent"""
        
        # Essayer l'IA d'abord
        ai_desc = self._generate_with_ai(product_info, price_info)
        if ai_desc and len(ai_desc) > 50:
            return ai_desc
        
        # Fallback : utiliser les templates
        return self._generate_from_template(product_info)
    
    def _generate_with_ai(self, product_info, price_info):
        """Génération avec IA"""
        try:
            prompt = f"""Crée une description Vinted attractive (200 caractères max) pour :

Type : {product_info.get('type')}
Marque : {product_info.get('marque')}
Couleur : {product_info.get('couleur')}
État : {product_info.get('etat')}
Détails : {product_info.get('details')}

Règles :
- 200 caractères maximum
- Ton amical et naturel
- 1-2 emojis pertinents
- Termine par "Envoi rapide !"
- Pas de guillemets

Réponds UNIQUEMENT avec la description."""

            payload = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 200,
                "temperature": 0.7
            }
            
            response = requests.post(self.api_url, json=payload, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                desc = result['choices'][0]['message']['content'].strip()
                desc = desc.replace('"', '').replace("'", "'")
                
                # Vérifier que c'est une vraie description
                if len(desc) > 30 and "does not exist" not in desc.lower():
                    return desc[:250]
                    
        except Exception as e:
            print(f"⚠️ IA description erreur : {e}")
        
        return None
    
    def _generate_from_template(self, product_info):
        """Génère depuis un template"""
        
        # Choisir le bon template
        product_type = product_info['type'].lower()
        templates = self.templates.get(product_type, self.templates['default'])
        
        # Sélectionner un template aléatoire
        template = random.choice(templates)
        
        # Mapper l'état en français
        etat_map = {
            "Neuf": "neuf avec étiquette",
            "Très bon": "excellent état",
            "Bon": "bon état",
            "Satisfaisant": "état correct"
        }
        
        etat_fr = etat_map.get(product_info.get('etat', 'Bon'), "bon état")
        
        # Préparer les variables
        variables = {
            "type": product_info['type'].capitalize(),
            "marque": product_info.get('marque', ''),
            "couleur": product_info.get('couleur', ''),
            "etat_fr": etat_fr,
            "details": product_info.get('details', 'Article de qualité')
        }
        
        # Nettoyer les variables vides
        for key, value in variables.items():
            if value in ["À préciser", "Non identifiée", ""]:
                if key == "marque":
                    variables[key] = ""
                elif key == "couleur":
                    variables[key] = "couleur neutre"
                elif key == "details":
                    variables[key] = "Article de qualité"
        
        # Générer la description
        try:
            description = template.format(**variables)
            # Nettoyer les doubles espaces
            description = " ".join(description.split())
            return description[:250]
        except Exception as e:
            print(f"⚠️ Template erreur : {e}")
            return f"{variables['type']} {variables['couleur']} en {etat_fr}. Envoi rapide ! 📦"
    
    def create_full_listing(self, product_info, price_info):
        """Crée l'annonce complète"""
        title = self.generate_title(product_info)
        description = self.generate_description(product_info, price_info)
        
        return {
            "titre": title,
            "description": description,
            "prix": price_info['prix_recommande'],
            "prix_min": price_info['prix_min'],
            "prix_max": price_info['prix_max']
        }


# Test
if __name__ == "__main__":
    generator = DescriptionGenerator()
    
    test_product = {
        "type": "maillot",
        "marque": "Adidas",
        "couleur": "blanc",
        "taille": "M",
        "etat": "Bon",
        "matiere": "polyester",
        "details": "Maillot Real Madrid"
    }
    
    test_price = {
        "prix_recommande": 25.0,
        "prix_min": 20.0,
        "prix_max": 30.0
    }
    
    # result = generator.create_full_listing(test_product, test_price)
    # print(json.dumps(result, indent=2, ensure_ascii=False))
