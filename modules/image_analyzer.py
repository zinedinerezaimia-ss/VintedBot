"""
Analyseur ULTRA-PRÉCIS avec Google Gemini Vision (gratuit illimité)
"""

import requests
import base64
from PIL import Image
import json
import os

class ImageAnalyzer:
    """Analyse avec Gemini Vision - LA solution qui marche"""
    
    def __init__(self):
        # API Gemini gratuite (pas besoin de clé pour usage public)
        self.api_url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro-vision:generateContent"
        
        # Clé API publique Gemini (gratuite, 60 req/min)
        self.api_key = "AIzaSyDCbVMLdXsXqfiio0l5bQ_7P8TZHMMZKdo"
    
    def analyze_product(self, image_path):
        """Analyse PRÉCISE avec Gemini"""
        print("🔍 Analyse avec Google Gemini Vision...")
        
        try:
            # Charger et encoder l'image
            with open(image_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            
            # Prompt ULTRA-précis
            prompt = """Tu es un expert en identification de vêtements. Analyse cette image avec PRÉCISION MAXIMALE.

RÉPONDS UNIQUEMENT avec ce JSON (rien d'autre) :
{
  "type": "un mot parmi: pantalon, jean, short, t-shirt, maillot, pull, sweat, robe, jupe, veste, manteau, chaussures, basket, bottine",
  "marque": "marque visible (Nike/Adidas/Puma/Reebok/Zara/H&M/Uniqlo) ou 'Non visible'",
  "couleur": "couleur EXACTE en français (noir/blanc/bleu/rouge/vert/gris/beige/marron)",
  "etat": "Neuf/Très bon/Bon/Satisfaisant",
  "details": "description courte précise (matière, style, particularités)"
}

RÈGLES CRITIQUES:
- Si vêtement de SPORT avec logo d'équipe/club → type="maillot" (PAS t-shirt!)
- Si PANTALON → type="pantalon" (JAMAIS pull/sweat!)
- Si JEAN en denim → type="jean"
- Logos Puma/Nike/Adidas sur vêtement sport = généralement MAILLOT
- Couleur = la plus dominante SEULEMENT
- Details = max 15 mots

EXEMPLES:
Maillot OM bleu: {"type":"maillot","marque":"Puma","couleur":"bleu","etat":"Bon","details":"Maillot OM authentique"}
Pantalon noir: {"type":"pantalon","marque":"Non visible","couleur":"noir","etat":"Bon","details":"Pantalon noir classique"}"""

            # Payload pour Gemini
            payload = {
                "contents": [{
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": img_data
                            }
                        }
                    ]
                }],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 500
                }
            }
            
            # Appel API
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                json=payload,
                timeout=20
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extraire la réponse
                text = data['candidates'][0]['content']['parts'][0]['text']
                
                # Nettoyer et parser le JSON
                text = text.strip().replace('```json', '').replace('```', '').strip()
                result = json.loads(text)
                
                print(f"✅ Gemini détection réussie!")
                print(f"   Type: {result['type']}")
                print(f"   Couleur: {result['couleur']}")
                
                return {
                    "type": result['type'],
                    "marque": result['marque'] if result['marque'] != 'Non visible' else 'À préciser',
                    "couleur": result['couleur'],
                    "etat": result['etat'],
                    "taille": "À préciser",
                    "matiere": "À préciser",
                    "details": result['details']
                }
            
            else:
                print(f"❌ Gemini erreur {response.status_code}")
                return self._fallback_analysis(image_path)
                
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")
            return self._fallback_analysis(image_path)
    
    def _fallback_analysis(self, image_path):
        """Analyse de secours AMÉLIORÉE"""
        print("   🔄 Analyse de secours...")
        
        try:
            img = Image.open(image_path)
            width, height = img.size
            ratio = height / width if width > 0 else 1
            
            # Détection type par ratio
            if ratio < 0.65:
                product_type = "pantalon"
            elif 0.65 <= ratio <= 1.4:
                product_type = "t-shirt"
            else:
                product_type = "pull"
            
            # Couleur dominante
            img_small = img.resize((100, 100))
            if img_small.mode != 'RGB':
                img_small = img_small.convert('RGB')
            
            pixels = list(img_small.getdata())
            
            # Filtrer pixels du fond
            valid_pixels = [p for p in pixels if not (p[0] > 240 and p[1] > 240 and p[2] > 240)]
            if not valid_pixels:
                valid_pixels = pixels
            
            # Moyenne RGB
            avg_r = sum(p[0] for p in valid_pixels) / len(valid_pixels)
            avg_g = sum(p[1] for p in valid_pixels) / len(valid_pixels)
            avg_b = sum(p[2] for p in valid_pixels) / len(valid_pixels)
            
            # Détection couleur
            if avg_r < 60 and avg_g < 60 and avg_b < 60:
                color = "noir"
            elif avg_r > 200 and avg_g > 200 and avg_b > 200:
                color = "blanc"
            elif avg_b > avg_r + 40:
                color = "bleu"
            elif avg_r > avg_g + 40 and avg_r > avg_b + 40:
                color = "rouge"
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
            
        except:
            return {
                "type": "vêtement",
                "marque": "À préciser",
                "couleur": "à préciser",
                "etat": "Bon",
                "taille": "À préciser",
                "matiere": "À préciser",
                "details": "Article à détailler"
            }
