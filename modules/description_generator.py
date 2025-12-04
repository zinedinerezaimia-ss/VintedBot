"""
Générateur de descriptions 100% fiable avec templates
Pas d'appels API externes
"""

import random

class DescriptionGenerator:
    """Génère des descriptions attractives avec templates"""
    
    def __init__(self):
        # Templates de descriptions par couleur et type
        self.templates = {
            "t-shirt": {
                "blanc": [
                    "T-shirt blanc classique et intemporel. Parfait pour toutes les occasions ! Très bon état. Envoi rapide 📦",
                    "Joli t-shirt blanc tout simple. Idéal pour un look casual ! État impeccable. Envoi soigné ✨",
                    "T-shirt blanc basique et essentiel. S'associe avec tout ! Bon état. Envoi rapide 👕"
                ],
                "noir": [
                    "T-shirt noir élégant et polyvalent. Parfait au quotidien ! Très bon état. Envoi rapide 📦",
                    "Super t-shirt noir indémodable. Coupe classique, état nickel ! Envoi soigné ✨",
                    "T-shirt noir basic mais efficace. Un incontournable ! Bon état. Envoi rapide 👕"
                ],
                "default": [
                    "Joli t-shirt en {couleur}. Parfait pour un look décontracté ! Bon état. Envoi rapide 📦",
                    "T-shirt {couleur} sympa et confortable. État nickel ! Envoi soigné ✨",
                    "Super t-shirt couleur {couleur}. Idéal au quotidien ! Envoi rapide 👕"
                ]
            },
            "pull": {
                "default": [
                    "Pull {couleur} tout doux et confortable. Parfait pour l'hiver ! Bon état. Envoi rapide 📦",
                    "Joli pull couleur {couleur}. Chaud et agréable à porter ! État nickel. Envoi soigné ✨",
                    "Super pull {couleur} bien chaud. Un indispensable ! Très bon état. Envoi rapide 🧶"
                ]
            },
            "pantalon": {
                "default": [
                    "Pantalon {couleur} confortable. Coupe classique, très bon état ! Envoi rapide 📦",
                    "Joli pantalon couleur {couleur}. Style et confort assurés ! État impeccable. Envoi soigné ✨",
                    "Super pantalon {couleur} polyvalent. Parfait au quotidien ! Bon état. Envoi rapide 👖"
                ]
            },
            "default": {
                "default": [
                    "Article {couleur} de qualité. Bon état général ! Envoi rapide et soigné 📦",
                    "Joli vêtement couleur {couleur}. État nickel ! Envoi rapide ✨",
                    "Article {couleur} sympa. Très bon état ! Envoi soigné 👌"
                ]
            }
        }
        
        # Emojis par type
        self.emojis = {
            "t-shirt": "👕",
            "pull": "🧶",
            "pantalon": "👖",
            "veste": "🧥",
            "robe": "👗",
            "chaussures": "👟"
        }
    
    def generate_title(self, product_info):
        """Génère un titre optimisé pour Vinted"""
        parts = []
        
        # Type de produit
        type_name = product_info['type'].capitalize()
        parts.append(type_name)
        
        # Couleur
        couleur = product_info.get('couleur', '')
        if couleur and couleur != "À préciser":
            parts.append(couleur)
        
        # Taille si disponible
        taille = product_info.get('taille', '')
        if taille and taille not in ["À préciser", "Non visible"]:
            parts.append(f"T.{taille}")
        
        # Marque si disponible
        marque = product_info.get('marque', '')
        if marque and marque not in ["À préciser", "Non identifiée"]:
            parts.insert(0, marque)
        
        # État
        etat = product_info.get('etat', 'Bon')
        parts.append(f"- {etat}")
        
        title = " ".join(parts)
        
        # Limiter à 80 caractères (limite Vinted)
        if len(title) > 80:
            title = title[:77] + "..."
        
        return title
    
    def generate_description(self, product_info, price_info):
        """Génère une description attractive"""
        
        product_type = product_info['type'].lower()
        couleur = product_info.get('couleur', 'neutre').lower()
        
        # Récupérer les templates appropriés
        type_templates = self.templates.get(product_type, self.templates['default'])
        
        # Chercher par couleur spécifique, sinon utiliser default
        color_templates = type_templates.get(couleur, type_templates.get('default', []))
        
        # Si pas de templates, utiliser le default général
        if not color_templates:
            color_templates = self.templates['default']['default']
        
        # Choisir un template aléatoire
        template = random.choice(color_templates)
        
        # Remplacer les variables
        description = template.format(
            couleur=couleur,
            type=product_type
        )
        
        # Ajouter un emoji si pertinent
        emoji = self.emojis.get(product_type, "")
        if emoji and emoji not in description:
            description = description.replace("📦", f"{emoji} 📦")
        
        return description
    
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
        "type": "t-shirt",
        "marque": "À préciser",
        "couleur": "blanc",
        "taille": "M",
        "etat": "Bon",
        "matiere": "coton",
        "details": "Article en bon état"
    }
    
    test_price = {
        "prix_recommande": 10.0,
        "prix_min": 7.0,
        "prix_max": 13.0
    }
    
    result = generator.create_full_listing(test_product, test_price)
    print(result)
