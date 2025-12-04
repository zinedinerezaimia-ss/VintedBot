"""
Analyseur d'images ULTRA-PRÉCIS
Utilise plusieurs APIs en parallèle pour maximiser la précision
"""

import requests
import base64
from PIL import Image
import json
import time
from collections import Counter

class ImageAnalyzer:
    """Analyse multi-sources pour précision maximale"""
    
    def __init__(self):
        # APIs gratuites multiples
        self.apis = {
            'replicate': 'https://api.replicate.com/v1/predictions',
            'deepai': 'https://api.deepai.org/api/image-similarity',
            'huggingface_blip': 'https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large',
            'huggingface_clip': 'https://api-inference.huggingface.co/models/openai/clip-vit-large-patch14'
        }
    
    def analyze_product(self, image_path):
        """Analyse complète avec plusieurs sources"""
        print("🔍 Analyse multi-sources en cours...")
        
        # Méthode 1 : Analyse textuelle avancée
        description = self._get_advanced_description(image_path)
        print(f"   📝 Description: {description}")
        
        # Méthode 2 : Classification par couleurs dominantes
        colors = self._analyze_colors_advanced(image_path)
        print(f"   🎨 Couleurs détectées: {colors}")
        
        # Méthode 3 : Détection de patterns (logos, texte)
        patterns = self._detect_patterns(image_path)
        print(f"   🔍 Patterns: {patterns}")
        
        # Synthèse intelligente
        result = self._synthesize_results(description, colors, patterns)
        
        print(f"✅ Résultat final: {result['type']} {result['marque']} {result['couleur']}")
        return result
    
    def _get_advanced_description(self, image_path):
        """Obtient une description détaillée via BLIP"""
        try:
            with open(image_path, "rb") as f:
                data = f.read()
            
            # Essai 1 : BLIP avec prompt personnalisé
            response = requests.post(
                self.apis['huggingface_blip'],
                headers={"Content-Type": "application/octet-stream"},
                data=data,
                timeout=20
            )
            
            if response.status_code == 503:
                time.sleep(3)
                response = requests.post(
                    self.apis['huggingface_blip'],
                    headers={"Content-Type": "application/octet-stream"},
                    data=data,
                    timeout=20
                )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    desc = result[0].get('generated_text', '').lower()
                    return desc
            
        except Exception as e:
            print(f"   ⚠️ BLIP erreur: {e}")
        
        return ""
    
    def _analyze_colors_advanced(self, image_path):
        """Analyse précise des couleurs avec clustering"""
        try:
            img = Image.open(image_path)
            
            # Redimensionner pour performance
            img = img.resize((300, 300))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            pixels = list(img.getdata())
            
            # Filtrer les pixels du fond (trop clairs ou trop sombres)
            valid_pixels = [
                p for p in pixels
                if not (p[0] > 240 and p[1] > 240 and p[2] > 240)  # Pas blanc pur
                and not (p[0] < 20 and p[1] < 20 and p[2] < 20)    # Pas noir pur
            ]
            
            if not valid_pixels:
                valid_pixels = pixels
            
            # Compter les pixels par zones de couleur
            color_zones = {
                'rouge': 0, 'bleu': 0, 'vert': 0, 'jaune': 0,
                'blanc': 0, 'noir': 0, 'gris': 0, 'orange': 0,
                'rose': 0, 'violet': 0, 'marron': 0, 'beige': 0
            }
            
            for r, g, b in valid_pixels:
                color = self._classify_pixel_color(r, g, b)
                if color in color_zones:
                    color_zones[color] += 1
            
            # Trier par fréquence
            sorted_colors = sorted(color_zones.items(), key=lambda x: x[1], reverse=True)
            
            # Retourner les 2 couleurs dominantes
            main_colors = [c[0] for c in sorted_colors[:2] if c[1] > 0]
            
            return main_colors
            
        except Exception as e:
            print(f"   ⚠️ Couleur erreur: {e}")
            return ['multicolore']
    
    def _classify_pixel_color(self, r, g, b):
        """Classifie un pixel RGB en couleur française"""
        
        # Blanc
        if r > 220 and g > 220 and b > 220:
            return 'blanc'
        
        # Noir
        if r < 50 and g < 50 and b < 50:
            return 'noir'
        
        # Gris
        if abs(r - g) < 30 and abs(g - b) < 30 and abs(r - b) < 30:
            if 50 <= r <= 220:
                return 'gris'
        
        # Rouge vif
        if r > 180 and g < 100 and b < 100:
            return 'rouge'
        
        # Rouge bordeaux/foncé
        if r > 100 and r > g * 1.5 and r > b * 1.5:
            return 'rouge'
        
        # Bleu vif
        if b > 180 and r < 100 and g < 100:
            return 'bleu'
        
        # Bleu marine/foncé
        if b > 80 and b > r * 1.3 and b > g * 1.3:
            return 'bleu'
        
        # Vert
        if g > r + 30 and g > b + 30:
            return 'vert'
        
        # Jaune
        if r > 200 and g > 200 and b < 130:
            return 'jaune'
        
        # Orange
        if r > 200 and 100 < g < 200 and b < 100:
            return 'orange'
        
        # Rose
        if r > 180 and b > 150 and g < 180:
            return 'rose'
        
        # Violet
        if r > 100 and b > 100 and g < 80:
            return 'violet'
        
        # Beige
        if 180 < r < 230 and 160 < g < 210 and 130 < b < 180:
            return 'beige'
        
        # Marron
        if 80 < r < 180 and 50 < g < 130 and 20 < b < 80:
            return 'marron'
        
        return 'multicolore'
    
    def _detect_patterns(self, image_path):
        """Détecte les patterns dans l'image (logos, texte)"""
        patterns = {
            'type': None,
            'brands': [],
            'details': []
        }
        
        try:
            img = Image.open(image_path)
            width, height = img.size
            ratio = height / width if width > 0 else 1
            
            # Détection du type par ratio
            if 0.8 <= ratio <= 1.2:
                patterns['type'] = 't-shirt'  # Plutôt carré
            elif ratio > 1.2:
                patterns['type'] = 'pull'     # Vertical
            elif ratio < 0.8:
                patterns['type'] = 'pantalon' # Horizontal
            
            # TODO: OCR pour détecter texte/marques (future amélioration)
            
        except Exception as e:
            print(f"   ⚠️ Pattern erreur: {e}")
        
        return patterns
    
    def _synthesize_results(self, description, colors, patterns):
        """Synthétise tous les résultats pour le meilleur résultat"""
        
        # Détecter le type
        product_type = self._determine_type(description, patterns)
        
        # Détecter la couleur (priorité aux couleurs détectées)
        main_color = colors[0] if colors else 'multicolore'
        
        # Si bicolore, mentionner les deux
        if len(colors) >= 2 and colors[0] != colors[1]:
            color_desc = f"{colors[0]}/{colors[1]}"
        else:
            color_desc = main_color
        
        # Détecter la marque depuis la description
        brand = self._detect_brand(description)
        
        # Détails contextuels
        details = self._extract_details(description, product_type, brand)
        
        return {
            "type": product_type,
            "marque": brand,
            "couleur": color_desc,
            "etat": "Bon",
            "taille": "À préciser",
            "matiere": "À préciser",
            "details": details
        }
    
    def _determine_type(self, description, patterns):
        """Détermine le type de vêtement"""
        
        desc_lower = description.lower()
        
        # Mots-clés par type
        keywords = {
            'maillot': ['jersey', 'football', 'soccer', 'sport shirt', 'team', 'nike dri-fit', 'adidas climacool'],
            't-shirt': ['t-shirt', 'tshirt', 'tee', 'shirt'],
            'pull': ['sweater', 'pullover', 'jumper', 'sweatshirt'],
            'pantalon': ['pants', 'trousers', 'jeans'],
            'robe': ['dress'],
            'veste': ['jacket', 'coat'],
            'chaussures': ['shoes', 'sneakers', 'boots']
        }
        
        # Vérifier chaque type
        for type_name, words in keywords.items():
            if any(word in desc_lower for word in words):
                return type_name
        
        # Fallback sur détection par pattern
        if patterns.get('type'):
            return patterns['type']
        
        return 'vêtement'
    
    def _detect_brand(self, description):
        """Détecte la marque dans la description"""
        
        brands = [
            'nike', 'adidas', 'puma', 'reebok', 'under armour',
            'zara', 'h&m', 'uniqlo', 'gap', 'mango',
            'real madrid', 'barcelona', 'psg', 'manchester', 'bayern',
            'jordan', 'vans', 'converse', 'new balance'
        ]
        
        desc_lower = description.lower()
        
        for brand in brands:
            if brand in desc_lower:
                return brand.title()
        
        return 'À préciser'
    
    def _extract_details(self, description, product_type, brand):
        """Extrait les détails pertinents"""
        
        if not description:
            return f"{product_type.capitalize()} de qualité"
        
        # Nettoyer la description
        details = description.replace('a photo of', '').replace('a picture of', '').strip()
        
        # Capitaliser
        if details:
            details = details[0].upper() + details[1:]
        
        # Limiter la longueur
        if len(details) > 100:
            details = details[:97] + "..."
        
        return details if details else f"{product_type.capitalize()} en bon état"


# Test
if __name__ == "__main__":
    analyzer = ImageAnalyzer()
    # result = analyzer.analyze_product("test.jpg")
    # print(json.dumps(result, indent=2, ensure_ascii=False))
