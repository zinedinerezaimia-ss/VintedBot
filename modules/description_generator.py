"""
Générateur de descriptions 100% gratuit
Utilise GPT4Free et d'autres APIs gratuites
"""

import requests
import json

class DescriptionGenerator:
    """Génère des descriptions attractives avec APIs gratuites"""
    
    def __init__(self):
        self.api_url = "https://api.airforce/v1/chat/completions"
    
    def generate_title(self, product_info):
        """Génère un titre accrocheur"""
        parts = []
        
        if product_info.get('marque') and product_info['marque'] != "Non identifiée":
            parts.append(product_info['marque'])
        
        parts.append(product_info['type'].capitalize())
        
        if product_info.get('taille') and product_info['taille'] != "Non visible":
            parts.append(f"taille {product_info['taille']}")
        
        if product_info.get('couleur'):
            parts.append(product_info['couleur'])
        
        if product_info.get('etat'):
            parts.append(f"- {product_info['etat']}")
        
        return " ".join(parts)
    
    def generate_description(self, product_info, price_info):
        """
        Génère une description avec GPT4Free (gratuit)
        """
        try:
            prompt = f"""Tu es un expert en rédaction d'annonces Vinted. 
            
Crée une description attractive et vendeuse pour ce produit :

Type : {product_info.get('type', 'Vêtement')}
Marque : {product_info.get('marque', 'Non spécifiée')}
Couleur : {product_info.get('couleur', 'Non spécifiée')}
Taille : {product_info.get('taille', 'Non spécifiée')}
État : {product_info.get('etat', 'Bon')}
Matière : {product_info.get('matiere', 'Non spécifiée')}
Détails : {product_info.get('details', 'Aucun')}
Prix : {price_info.get('prix_recommande', 'À définir')}€

Règles strictes :
- Maximum 250 caractères
- Ton amical et naturel
- Mets en avant les points forts
- Sois honnête sur l'état
- 2-3 emojis pertinents maximum
- Termine par "Envoi rapide ! 📦"
- Pas de phrases marketing lourdes

Réponds UNIQUEMENT avec la description, sans guillemets."""

            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 300,
                "temperature": 0.7
            }
            
            response = requests.post(self.api_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                description = result['choices'][0]['message']['content'].strip()
                description = description.replace('"', '').replace("'", "'")
                
                print(f"✅ Description générée ({len(description)} caractères)")
                return description
            else:
                print(f"⚠️ API erreur : {response.status_code}")
                return self._generate_basic_description(product_info)
                
        except Exception as e:
            print(f"⚠️ Erreur génération : {e}")
            return self._generate_basic_description(product_info)
    
    def _generate_basic_description(self, product_info):
        """Génère une description basique sans IA"""
        desc = f"{product_info['type'].capitalize()}"
        
        if product_info.get('marque') != "Non identifiée":
            desc += f" {product_info['marque']}"
        
        desc += f" {product_info.get('couleur', 'coloris mixte')}. "
        desc += f"État : {product_info.get('etat', 'Bon')}. "
        
        if product_info.get('taille') not in ["Non visible", "À préciser"]:
            desc += f"Taille {product_info['taille']}. "
        
        desc += "Parfait pour compléter votre garde-robe ! Envoi rapide ! 📦"
        
        return desc
    
    def create_full_listing(self, product_info, price_info):
        """
        Crée l'annonce complète (titre + description)
        """
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
        "marque": "Nike",
        "couleur": "noir",
        "taille": "M",
        "etat": "Très bon",
        "matiere": "coton",
        "details": "logo swoosh blanc"
    }
    
    test_price = {
        "prix_recommande": 12.0,
        "prix_min": 8.0,
        "prix_max": 15.0
    }
    
    # result = generator.create_full_listing(test_product, test_price)
    # print(result)