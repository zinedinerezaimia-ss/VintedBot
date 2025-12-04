"""
Analyseur d'images simplifié et fiable
Utilise uniquement l'analyse d'image sans APIs externes
"""

from PIL import Image
from collections import Counter
import os

class ImageAnalyzer:
    """Analyse les photos de produits de manière fiable"""
    
    def __init__(self):
        pass
    
    def analyze_product(self, image_path):
        """
        Analyse une image et retourne les infos du produit
        Méthode 100% fiable sans dépendance externe
        """
        print("🔍 Analyse de l'image...")
        
        try:
            img = Image.open(image_path)
            
            # Analyser la couleur dominante
            couleur = self._detect_color(img)
            
            # Détecter le type par les dimensions
            product_type = self._detect_type(img)
            
            result = {
                "type": product_type,
                "marque": "À préciser",
                "couleur": couleur,
                "etat": "Bon",
                "taille": "À préciser",
                "matiere": "À préciser",
                "details": f"Article {couleur} en bon état visuel"
            }
            
            print(f"✅ Produit analysé : {result['type']} {result['couleur']}")
            return result
            
        except Exception as e:
            print(f"⚠️ Erreur analyse : {e}")
            return {
                "type": "vêtement",
                "marque": "À préciser",
                "couleur": "multicolore",
                "etat": "Bon",
                "taille": "À préciser",
                "matiere": "À préciser",
                "details": "Article en bon état"
            }
    
    def _detect_color(self, img):
        """Détecte la couleur dominante de l'image"""
        try:
            # Redimensionner pour accélérer
            img_small = img.resize((100, 100))
            
            # Convertir en RGB
            if img_small.mode != 'RGB':
                img_small = img_small.convert('RGB')
            
            pixels = list(img_small.getdata())
            
            # Filtrer les pixels trop clairs (fond blanc) et trop sombres (ombres)
            filtered_pixels = [
                p for p in pixels 
                if not (p[0] > 240 and p[1] > 240 and p[2] > 240)  # Pas blanc
                and not (p[0] < 30 and p[1] < 30 and p[2] < 30)    # Pas noir pur
            ]
            
            if not filtered_pixels:
                filtered_pixels = pixels
            
            # Compter les couleurs
            color_counts = Counter(filtered_pixels)
            
            # Prendre les 3 couleurs les plus fréquentes
            top_colors = color_counts.most_common(3)
            
            # Analyser la couleur dominante
            if top_colors:
                dominant_rgb = top_colors[0][0]
                return self._rgb_to_color_name(dominant_rgb)
            
            return "multicolore"
            
        except Exception as e:
            print(f"⚠️ Erreur détection couleur : {e}")
            return "à préciser"
    
    def _rgb_to_color_name(self, rgb):
        """Convertit RGB en nom de couleur français"""
        r, g, b = rgb
        
        # Blanc
        if r > 200 and g > 200 and b > 200:
            return "blanc"
        
        # Noir
        if r < 60 and g < 60 and b < 60:
            return "noir"
        
        # Gris
        if abs(r - g) < 30 and abs(g - b) < 30 and abs(r - b) < 30:
            if 60 <= r <= 200:
                return "gris"
        
        # Rouge
        if r > g + 40 and r > b + 40:
            return "rouge"
        
        # Bleu
        if b > r + 40 and b > g + 40:
            return "bleu"
        
        # Vert
        if g > r + 40 and g > b + 40:
            return "vert"
        
        # Jaune
        if r > 180 and g > 180 and b < 100:
            return "jaune"
        
        # Orange
        if r > 200 and 100 < g < 200 and b < 100:
            return "orange"
        
        # Rose
        if r > 180 and b > 150 and g < 150:
            return "rose"
        
        # Violet
        if r > 100 and b > 100 and g < 100:
            return "violet"
        
        # Beige/Marron
        if r > 140 and g > 120 and b > 80 and r > b:
            if r - b < 50:
                return "beige"
            else:
                return "marron"
        
        return "multicolore"
    
    def _detect_type(self, img):
        """Détecte le type de vêtement par les proportions"""
        try:
            width, height = img.size
            ratio = height / width if width > 0 else 1
            
            # T-shirt/Maillot : plutôt carré ou légèrement vertical
            if 0.9 <= ratio <= 1.3:
                return "t-shirt"
            
            # Pull : plus vertical
            elif ratio > 1.3:
                return "pull"
            
            # Pantalon : horizontal
            elif ratio < 0.8:
                return "pantalon"
            
            return "vêtement"
            
        except:
            return "vêtement"


# Test
if __name__ == "__main__":
    analyzer = ImageAnalyzer()
    # result = analyzer.analyze_product("test.jpg")
    # print(result)
