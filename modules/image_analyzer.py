"""
Analyseur d'images INTELLIGENT avec GPT-4 Vision gratuit
"""

import requests
import base64
from PIL import Image
import json
import time

class ImageAnalyzer:
    """Analyse précise avec vraie IA Vision"""
    
    def __init__(self):
        # API gratuite GPT-4 Vision via proxy
        self.vision_apis = [
            "https://api.airforce/v1/chat/completions",  # GPT-4 Vision gratuit
            "https://free.gpt.ge/api/generate",          # Backup
        ]
    
    def analyze_product(self, image_path):
        """Analyse avec GPT-4 Vision"""
        print("🔍 Analyse avec IA Vision avancée...")
        
        try:
            # Convertir l'image en base64
            with open(image_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            
            # Prompt ultra-précis pour GPT-4 Vision
            prompt = """Analyse cette image de vêtement/produit avec PRÉCISION MAXIMALE.

Tu DOIS répondre UNIQUEMENT avec un JSON strict (pas de texte avant/après) :

{
  "type": "un seul mot parmi: t-shirt, maillot, pull, sweat, pantalon, jean, short, robe, jupe, veste, manteau, chaussures, basket, bottine, accessoire",
  "marque": "marque visible (Nike/Adidas/Zara/H&M/Puma/Uniqlo/Gap...) ou 'Non visible'",
  "couleur_principale": "couleur EXACTE dominante en français (noir/blanc/bleu/rouge/vert/gris/beige/marron/rose/violet/orange/jaune)",
  "couleur_secondaire": "2e couleur si bicolore, sinon 'aucune'",
  "etat_visuel": "Neuf/Très bon/Bon/Satisfaisant selon l'aspect",
  "details": "détails importants (logo, motif, style, matière visible, particularités)"
}

RÈGLES STRICTES :
- Si c'est un PANTALON : type = "pantalon" (jamais pull/sweat !)
- Si c'est un T-SHIRT : type = "t-shirt" 
- Si c'est un MAILLOT DE SPORT : type = "maillot"
- La couleur doit être EXACTE (pas d'approximation)
- Si plusieurs couleurs : indiquer la dominante en "couleur_principale"

RÉPONDS UNIQUEMENT LE JSON, RIEN D'AUTRE."""

            # Appel à l'API
            result = self._call_vision_api(img_data, prompt)
            
            if result:
                print(f"✅ Détection IA réussie !")
                print(f"   Type: {result['type']}")
                print(f"   Marque: {result['marque']}")
                print(f"   Couleur: {result['couleur_principale']}")
                return self._format_result(result)
            else:
                print("⚠️ IA Vision indisponible, analyse basique...")
                return self._fallback_analysis(image_path)
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return self._fallback_analysis(image_path)
    
    def _call_vision_api(self, img_data, prompt):
        """Appelle l'API Vision avec retry"""
        
        for api_url in self.vision_apis:
            try:
                print(f"   🔄 Tentative avec {api_url.split('/')[2]}...")
                
                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{img_data}"
                                    }
                                }
                            ]
                        }
                    ],
                    "max_tokens": 500,
                    "temperature": 0.1  # Précision maximale
                }
                
                response = requests.post(
                    api_url,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    content = data['choices'][0]['message']['content']
                    
                    # Extraire le JSON
                    json_match = content.strip()
                    # Nettoyer les éventuels backticks
                    json_match = json_match.replace('```json', '').replace('```', '').strip()
                    
                    result = json.loads(json_match)
                    return result
                
                print(f"   ❌ Erreur {response.status_code}")
                
            except Exception as e:
                print(f"   ⚠️ {str(e)[:50]}...")
                continue
        
        return None
    
    def _format_result(self, api_result):
        """Formate le résultat API au format attendu"""
        
        # Construire la couleur finale
        couleur = api_result['couleur_principale']
        if api_result.get('couleur_secondaire') and api_result['couleur_secondaire'] != 'aucune':
            couleur = f"{api_result['couleur_principale']}/{api_result['couleur_secondaire']}"
        
        return {
            "type": api_result['type'],
            "marque": api_result['marque'] if api_result['marque'] != 'Non visible' else 'À préciser',
            "couleur": couleur,
            "etat": api_result.get('etat_visuel', 'Bon'),
            "taille": "À préciser",
            "matiere": "À préciser",
            "details": api_result.get('details', '')
        }
    
    def _fallback_analysis(self, image_path):
        """Analyse de secours si l'IA échoue"""
        print("   🔄 Analyse basique de secours...")
        
        try:
            img = Image.open(image_path)
            width, height = img.size
            ratio = height / width if width > 0 else 1
            
            # Détecter le type par ratio
            if ratio < 0.7:
                product_type = "pantalon"
            elif 0.7 <= ratio <= 1.3:
                product_type = "t-shirt"
            else:
                product_type = "pull"
            
            # Couleur dominante basique
            img_small = img.resize((50, 50))
            if img_small.mode != 'RGB':
                img_small = img_small.convert('RGB')
            
            pixels = list(img_small.getdata())
            avg_r = sum(p[0] for p in pixels) / len(pixels)
            avg_g = sum(p[1] for p in pixels) / len(pixels)
            avg_b = sum(p[2] for p in pixels) / len(pixels)
            
            # Détection couleur simple
            if avg_r > 200 and avg_g > 200 and avg_b > 200:
                color = "blanc"
            elif avg_r < 80 and avg_g < 80 and avg_b < 80:
                color = "noir"
            elif avg_r > avg_g + 30 and avg_r > avg_b + 30:
                color = "rouge"
            elif avg_b > avg_r + 30 and avg_b > avg_g + 30:
                color = "bleu"
            else:
                color = "multicolore"
            
            return {
                "type": product_type,
                "marque": "À préciser",
                "couleur": color,
                "etat": "Bon",
                "taille": "À préciser",
                "matiere": "À préciser",
                "details": f"{product_type.capitalize()} {color}"
            }
            
        except Exception as e:
            print(f"   ❌ Erreur fallback: {e}")
            return self._default_result()
    
    def _default_result(self):
        """Résultat par défaut"""
        return {
            "type": "vêtement",
            "marque": "À préciser",
            "couleur": "à préciser",
            "etat": "Bon",
            "taille": "À préciser",
            "matiere": "À préciser",
            "details": "Article à détailler"
        }


# Test
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        analyzer = ImageAnalyzer()
        result = analyzer.analyze_product(sys.argv[1])
        print("\n" + "="*50)
        print(json.dumps(result, indent=2, ensure_ascii=False))
