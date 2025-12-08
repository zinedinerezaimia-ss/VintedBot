"""
Analyseur d'images intelligent
"""

import requests
import base64
from PIL import Image
import json
import os

class ImageAnalyzer:
    
    def __init__(self):
        pass
    
    def analyze_product(self, image_path):
        print("🔍 Analyse de l'image...")
        
        try:
            img = Image.open(image_path)
            width, height = img.size
            ratio = height / width if width > 0 else 1
            
            # Couleur dominante
            colors = self._analyze_colors(img)
            main_color = colors[0] if colors else "multicolore"
            
            # Type par ratio + couleur
            if ratio < 0.7:
                if main_color in ['noir', 'marron', 'beige', 'gris']:
                    product_type = "chaussures"
                else:
                    product_type = "pantalon"
            elif 0.7 <= ratio <= 1.5:
                if main_color in ['rouge', 'bleu', 'vert', 'jaune']:
                    product_type = "maillot"
                else:
                    product_type = "t-shirt"
            else:
                product_type = "pull"
            
            print(f"✅ Détecté: {product_type} {main_color}")
            
            return {
                "type": product_type,
                "marque": "À préciser",
                "couleur": main_color,
                "etat": "Bon",
                "taille": "À préciser",
                "matiere": "À préciser",
                "details": f"{product_type.capitalize()} {main_color}"
            }
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return {
                "type": "vêtement",
                "marque": "À préciser",
                "couleur": "à préciser",
                "etat": "Bon",
                "taille": "À préciser",
                "matiere": "À préciser",
                "details": ""
            }
    
    def _analyze_colors(self, img):
        try:
            img_small = img.resize((100, 100))
            if img_small.mode != 'RGB':
                img_small = img_small.convert('RGB')
            
            pixels = list(img_small.getdata())
            valid_pixels = [p for p in pixels if not (p[0] > 235 and p[1] > 235 and p[2] > 235)]
            
            if not valid_pixels:
                valid_pixels = pixels
            
            avg_r = sum(p[0] for p in valid_pixels) / len(valid_pixels)
            avg_g = sum(p[1] for p in valid_pixels) / len(valid_pixels)
            avg_b = sum(p[2] for p in valid_pixels) / len(valid_pixels)
            
            if avg_r < 60 and avg_g < 60 and avg_b < 60:
                return ['noir']
            elif avg_r > 200 and avg_g > 200 and avg_b > 200:
                return ['blanc']
            elif avg_r > avg_g + 50 and avg_r > avg_b + 50:
                return ['rouge']
            elif avg_b > avg_r + 40 and avg_b > avg_g + 30:
                return ['bleu']
            elif avg_g > avg_r + 40 and avg_g > avg_b + 40:
                return ['vert']
            elif avg_r > 100 and avg_g > 70 and avg_b < 60:
                return ['marron']
            else:
                return ['gris']
        except:
            return ['multicolore']
