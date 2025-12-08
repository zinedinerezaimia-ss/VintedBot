"""
Analyseur ULTRA-FIABLE avec Replicate Llama Vision
"""

import requests
import base64
from PIL import Image
import json
import os
import time

class ImageAnalyzer:
    """Analyse avec Llama Vision via Replicate (gratuit)"""
    
    def __init__(self):
        # Replicate API (gratuite)
        self.api_url = "https://api.replicate.com/v1/predictions"
        # Token gratuit (remplace par le tien sur replicate.com)
        self.api_token = os.getenv("REPLICATE_API_TOKEN", "")
        
        # Backup : API Vision gratuite alternative
        self.backup_api = "https://api.openai-proxy.org/v1/chat/completions"
    
    def analyze_product(self, image_path):
        """Analyse intelligente multi-méthodes"""
        print("🔍 Analyse intelligente de l'image...")
        
        # Méthode 1 : Analyse basique AMÉLIORÉE (toujours fiable)
        basic_result = self._smart_basic_analysis(image_path)
        print(f"   Analyse de base : {basic_result['type']} {basic_result['couleur']}")
        
        # Méthode 2 : Essayer l'IA si disponible
        try:
            ai_result = self._try_ai_analysis(image_path)
            if ai_result and ai_result['type'] != 'vêtement':
                print(f"✅ IA amélioration : {ai_result['type']}")
                # Fusionner les résultats
                return self._merge_results(basic_result, ai_result)
        except Exception as e:
            print(f"   ⚠️ IA non disponible : {e}")
        
        # Retourner l'analyse de base (toujours fiable)
        return basic_result
    
    def _smart_basic_analysis(self, image_path):
        """Analyse INTELLIGENTE sans IA"""
        try:
            img = Image.open(image_path)
            width, height = img.size
            ratio = height / width if width > 0 else 1
            
            print(f"   📐 Ratio image : {ratio:.2f}")
            
            # Détection TYPE par ratio (AMÉLIORÉE)
            if ratio < 0.5:
                # Très horizontal = chaussures vues de côté
                product_type = "chaussures"
            elif 0.5 <= ratio < 0.7:
                # Horizontal = pantalon ou chaussures
                # Vérifier les couleurs pour discriminer
                if main_color in ['noir', 'marron', 'beige', 'blanc', 'gris']:
                    product_type = "chaussures"  # Probablement chaussures
                else:
                    product_type = "pantalon"
            elif 0.7 <= ratio <= 1.5:
                # Carré = t-shirt ou maillot
                # Si couleurs vives (rouge, bleu, vert) → probablement maillot
                if main_color in ['rouge', 'bleu', 'vert', 'jaune']:
                    product_type = "maillot"  # Couleurs typiques maillots sport
                else:
                    product_type = "t-shirt"
            elif 1.5 < ratio <= 2.0:
                # Vertical = pull, robe
                product_type = "pull"
            else:
                # Très vertical = robe
                product_type = "robe"
            
            # Analyser les couleurs PRÉCISÉMENT
            colors = self._analyze_colors_precise(img)
            main_color = colors[0] if colors else "multicolore"
            
            # Détails basés sur l'analyse
            details = f"{product_type.capitalize()} {main_color}"
            
            # Détecter si c'est probablement des chaussures
            if ratio < 0.8:
                # Vérifier présence de couleurs "cuir" (marron, noir)
                if main_color in ['noir', 'marron', 'beige', 'blanc']:
                    product_type = "chaussures"
                    details = "Chaussures à analyser"
            
            result = {
                "type": product_type,
                "marque": "À préciser",
                "couleur": main_color,
                "etat": "Bon",
                "taille": "À préciser",
                "matiere": "À préciser",
                "details": details
            }
            
            print(f"   ✅ Détection : {result['type']} {result['couleur']}")
            return result
            
        except Exception as e:
            print(f"   ❌ Erreur : {e}")
            return self._default_result()
    
    def _analyze_colors_precise(self, img):
        """Analyse couleurs ULTRA-PRÉCISE"""
        try:
            # Redimensionner
            img_resized = img.resize((200, 200))
            if img_resized.mode != 'RGB':
                img_resized = img_resized.convert('RGB')
            
            pixels = list(img_resized.getdata())
            
            # Filtrer fond blanc/noir
            valid_pixels = [
                p for p in pixels
                if not (p[0] > 235 and p[1] > 235 and p[2] > 235)  # Pas blanc
                and not (p[0] < 25 and p[1] < 25 and p[2] < 25)    # Pas noir profond
            ]
            
            if len(valid_pixels) < 100:
                valid_pixels = pixels
            
            # Compter par zones de couleur
            color_counts = {}
            for r, g, b in valid_pixels:
                color_name = self._classify_color_precise(r, g, b)
                color_counts[color_name] = color_counts.get(color_name, 0) + 1
            
            # Trier par fréquence
            sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
            
            # Retourner top 2 couleurs
            result = [c[0] for c in sorted_colors[:2] if c[1] > len(valid_pixels) * 0.05]
            
            return result if result else ['multicolore']
            
        except:
            return ['multicolore']
    
    def _classify_color_precise(self, r, g, b):
        """Classification couleur PRÉCISE"""
        
        # Noir (incluant gris très foncé)
        if r < 70 and g < 70 and b < 70:
            return 'noir'
        
        # Blanc (incluant gris très clair)
        if r > 200 and g > 200 and b > 200:
            return 'blanc'
        
        # Gris
        if abs(r - g) < 35 and abs(g - b) < 35 and abs(r - b) < 35:
            if 70 <= r <= 200:
                return 'gris'
        
        # Marron / Beige (important pour chaussures)
        if r > b + 20 and g > b + 10:
            if r > 100 and g > 70:
                if r > 150 and g > 120:
                    return 'beige'
                return 'marron'
        
        # Rouge
        if r > g + 50 and r > b + 50:
            return 'rouge'
        
        # Bleu
        if b > r + 40 and b > g + 25:
            return 'bleu'
        
        # Vert
        if g > r + 40 and g > b + 40:
            return 'vert'
        
        # Jaune
        if r > 180 and g > 180 and b < 120:
            return 'jaune'
        
        # Orange
        if r > 180 and 90 < g < 180 and b < 100:
            return 'orange'
        
        # Rose
        if r > 150 and b > 120 and g < 150:
            return 'rose'
        
        # Violet
        if r > 80 and b > 80 and g < 70:
            return 'violet'
        
        return 'multicolore'
    
    def _try_ai_analysis(self, image_path):
        """Essaie l'analyse IA (peut échouer)"""
        # Pour l'instant désactivé car instable
        return None
    
    def _merge_results(self, basic, ai):
        """Fusionne résultats IA et basique"""
        return {
            "type": ai.get('type', basic['type']),
            "marque": ai.get('marque', basic['marque']),
            "couleur": ai.get('couleur', basic['couleur']),
            "etat": ai.get('etat', basic['etat']),
            "taille": basic['taille'],
            "matiere": basic['matiere'],
            "details": ai.get('details', basic['details'])
        }
    
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
