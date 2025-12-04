"""
Analyseur d'images amélioré avec meilleure détection
"""

import requests
import base64
from PIL import Image
import json
import re

class ImageAnalyzer:
    """Analyse les photos avec plusieurs APIs gratuites"""
    
    def __init__(self):
        # URLs des APIs gratuites
        self.gpt4free_url = "https://api.airforce/v1/chat/completions"
        self.huggingface_url = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
    
    def analyze_product(self, image_path):
        """
        Analyse une image avec fallback intelligent
        """
        print("🔍 Analyse de l'image...")
        
        # Essayer plusieurs méthodes
        result = None
        
        # Méthode 1 : GPT4Free (meilleure qualité)
        result = self._analyze_with_gpt4free(image_path)
        
        # Si échec, utiliser analyse basique intelligente
        if not result or not self._is_valid_result(result):
            print("⚠️ IA non disponible, utilisation de l'analyse de base")
            result = self._smart_basic_analysis(image_path)
        
        # Nettoyer et valider le résultat
        result = self._clean_result(result)
        
        print(f"✅ Produit analysé : {result['type']}")
        return result
    
    def _analyze_with_gpt4free(self, image_path):
        """Analyse avec GPT4Free"""
        try:
            with open(image_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            
            prompt = """Analyse cette image de vêtement et réponds UNIQUEMENT avec un JSON (pas de texte avant/après) :
{
  "type": "t-shirt/pull/maillot/pantalon/robe/chaussures/veste",
  "marque": "marque visible (Adidas/Nike/Zara...) ou 'Non identifiée'",
  "couleur": "couleur principale exacte",
  "etat": "Neuf/Très bon/Bon/Satisfaisant",
  "taille": "taille si visible (S/M/L/XL) ou 'À préciser'",
  "matiere": "matière probable (coton/polyester/cuir...)",
  "details": "détails importants (logo, équipe, motif...)"
}

Exemples de bonnes réponses :
- Si c'est un maillot du Real Madrid : marque="Adidas", details="Maillot Real Madrid"
- Si c'est un t-shirt Nike noir : marque="Nike", couleur="noir"
"""
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": [{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_data}"}}
                    ]
                }],
                "max_tokens": 500,
                "temperature": 0.3
            }
            
            response = requests.post(self.gpt4free_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Extraire le JSON
                json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content, re.DOTALL)
                if json_match:
                    product_info = json.loads(json_match.group())
                    return product_info
            
        except Exception as e:
            print(f"⚠️ GPT4Free erreur : {e}")
        
        return None
    
    def _smart_basic_analysis(self, image_path):
        """
        Analyse basique mais intelligente en se basant sur :
        - Les couleurs dominantes de l'image
        - La forme générale
        - Patterns courants
        """
        try:
            img = Image.open(image_path)
            
            # Analyser les couleurs dominantes
            img_small = img.resize((150, 150))
            pixels = list(img_small.getdata())
            
            # Compter les couleurs
            from collections import Counter
            color_counts = Counter(pixels)
            dominant_colors = color_counts.most_common(5)
            
            # Déterminer la couleur principale
            main_color = self._get_color_name(dominant_colors[0][0])
            
            # Détection basique du type (par ratio d'image)
            width, height = img.size
            ratio = height / width
            
            if ratio > 1.3:
                product_type = "t-shirt"
            elif ratio > 1.0:
                product_type = "pull"
            elif ratio < 0.8:
                product_type = "pantalon"
            else:
                product_type = "vêtement"
            
            return {
                "type": product_type,
                "marque": "À préciser",
                "couleur": main_color,
                "etat": "Bon",
                "taille": "À préciser",
                "matiere": "À préciser",
                "details": f"Article {main_color} en bon état"
            }
            
        except Exception as e:
            print(f"⚠️ Analyse basique erreur : {e}")
            return self._default_result()
    
    def _get_color_name(self, rgb):
        """Convertit RGB en nom de couleur"""
        r, g, b = rgb[:3] if len(rgb) >= 3 else (128, 128, 128)
        
        # Détection de couleurs communes
        if r > 200 and g > 200 and b > 200:
            return "blanc"
        elif r < 50 and g < 50 and b < 50:
            return "noir"
        elif r > 150 and g < 100 and b < 100:
            return "rouge"
        elif r < 100 and g > 150 and b < 100:
            return "vert"
        elif r < 100 and g < 100 and b > 150:
            return "bleu"
        elif r > 150 and g > 150 and b < 100:
            return "jaune"
        elif r > 150 and g < 100 and b > 150:
            return "rose"
        elif r > 100 and g > 100 and b > 100:
            return "gris"
        else:
            return "multicolore"
    
    def _is_valid_result(self, result):
        """Vérifie si le résultat est valide"""
        if not result:
            return False
        
        required_fields = ["type", "marque", "couleur", "etat"]
        for field in required_fields:
            if field not in result or not result[field]:
                return False
        
        return True
    
    def _clean_result(self, result):
        """Nettoie et normalise le résultat"""
        if not result:
            return self._default_result()
        
        # Remplacer les valeurs vides
        defaults = {
            "type": "vêtement",
            "marque": "À préciser",
            "couleur": "À préciser",
            "etat": "Bon",
            "taille": "À préciser",
            "matiere": "À préciser",
            "details": "Article en bon état"
        }
        
        for key, default_value in defaults.items():
            if key not in result or not result[key] or result[key] == "Non identifiée":
                result[key] = default_value
        
        # Capitaliser
        result["type"] = result["type"].lower()
        result["couleur"] = result["couleur"].lower()
        
        return result
    
    def _default_result(self):
        """Résultat par défaut"""
        return {
            "type": "vêtement",
            "marque": "À préciser",
            "couleur": "À préciser",
            "etat": "Bon",
            "taille": "À préciser",
            "matiere": "À préciser",
            "details": "Article à détailler"
        }


# Test
if __name__ == "__main__":
    analyzer = ImageAnalyzer()
    # result = analyzer.analyze_product("chemin/vers/image.jpg")
    # print(json.dumps(result, indent=2, ensure_ascii=False))
