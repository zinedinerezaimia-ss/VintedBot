"""
Analyseur d'images ULTRA-PRÉCIS
Analyse pixel par pixel pour détecter couleurs et types
"""

from PIL import Image
from collections import Counter
import os

class ImageAnalyzer:
    """Analyse les photos avec précision maximale"""
    
    def __init__(self):
        pass
    
    def analyze_product(self, image_path):
        """Analyse complète d'un produit"""
        print("🔍 Analyse de l'image en cours...")
        
        try:
            img = Image.open(image_path)
            
            # 1. Analyser les couleurs dominantes
            colors = self._analyze_colors_advanced(img)
            print(f"   🎨 Couleurs détectées: {colors}")
            
            # 2. Détecter le type par les dimensions
            product_type = self._detect_type_from_shape(img)
            print(f"   📦 Type détecté: {product_type}")
            
            # 3. Essayer de détecter la marque (basique pour l'instant)
            brand = "À préciser"
            
            # 4. Construire le résultat
            main_color = colors[0] if colors else "multicolore"
            
            # Si bicolore, mentionner les deux couleurs
            if len(colors) >= 2 and colors[0] != colors[1]:
                color_desc = f"{colors[0]}/{colors[1]}"
            else:
                color_desc = main_color
            
            result = {
                "type": product_type,
                "marque": brand,
                "couleur": color_desc,
                "etat": "Bon",
                "taille": "À préciser",
                "matiere": "À préciser",
                "details": f"{product_type.capitalize()} {color_desc} en bon état"
            }
            
            print(f"✅ Analyse terminée: {result['type']} {result['couleur']}")
            return result
            
        except Exception as e:
            print(f"❌ Erreur analyse: {e}")
            return self._default_result()
    
    def _analyze_colors_advanced(self, img):
        """Analyse précise des couleurs pixel par pixel"""
        try:
            # Redimensionner pour performance (300x300 pixels = 90000 pixels à analyser)
            img_resized = img.resize((300, 300))
            
            # Convertir en RGB si nécessaire
            if img_resized.mode != 'RGB':
                img_resized = img_resized.convert('RGB')
            
            # Récupérer tous les pixels
            pixels = list(img_resized.getdata())
            
            # Filtrer les pixels du fond (blanc pur ou noir pur)
            valid_pixels = []
            for r, g, b in pixels:
                # Ignorer blanc pur (fond)
                if r > 240 and g > 240 and b > 240:
                    continue
                # Ignorer noir pur (ombres profondes)
                if r < 20 and g < 20 and b < 20:
                    continue
                valid_pixels.append((r, g, b))
            
            # Si tous les pixels sont filtrés, garder tous les pixels
            if len(valid_pixels) < 100:
                valid_pixels = pixels
            
            # Compter chaque couleur par catégorie
            color_counts = {
                'rouge': 0,
                'bleu': 0,
                'vert': 0,
                'jaune': 0,
                'blanc': 0,
                'noir': 0,
                'gris': 0,
                'orange': 0,
                'rose': 0,
                'violet': 0,
                'marron': 0,
                'beige': 0
            }
            
            # Classifier chaque pixel
            for r, g, b in valid_pixels:
                color_name = self._classify_pixel_color(r, g, b)
                if color_name in color_counts:
                    color_counts[color_name] += 1
            
            # Trier par fréquence
            sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
            
            # Retourner les 2 couleurs les plus présentes (minimum 5% des pixels)
            total_pixels = len(valid_pixels)
            main_colors = []
            
            for color, count in sorted_colors:
                percentage = (count / total_pixels) * 100
                if percentage > 5:  # Au moins 5% de présence
                    main_colors.append(color)
                if len(main_colors) >= 2:
                    break
            
            # Si aucune couleur dominante, prendre la première quand même
            if not main_colors:
                main_colors = [sorted_colors[0][0]]
            
            return main_colors
            
        except Exception as e:
            print(f"   ⚠️ Erreur couleurs: {e}")
            return ['multicolore']
    
    def _classify_pixel_color(self, r, g, b):
        """Classifie un pixel RGB en nom de couleur français"""
        
        # Blanc (très clair)
        if r > 220 and g > 220 and b > 220:
            return 'blanc'
        
        # Noir (très foncé)
        if r < 50 and g < 50 and b < 50:
            return 'noir'
        
        # Gris (nuances similaires RGB)
        if abs(r - g) < 30 and abs(g - b) < 30 and abs(r - b) < 30:
            if 50 <= r <= 220:
                return 'gris'
        
        # Rouge vif
        if r > 180 and g < 100 and b < 100:
            return 'rouge'
        
        # Rouge plus foncé / bordeaux
        if r > 100 and r > g * 1.5 and r > b * 1.5:
            return 'rouge'
        
        # Bleu vif / clair
        if b > 180 and r < 100 and g < 100:
            return 'bleu'
        
        # Bleu marine / foncé
        if b > 80 and b > r * 1.3 and b > g * 1.3:
            return 'bleu'
        
        # Bleu moyen
        if b > r + 40 and b > g + 20:
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
        
        # Violet / Mauve
        if r > 100 and b > 100 and g < 100:
            return 'violet'
        
        # Beige / Crème
        if 180 < r < 240 and 160 < g < 220 and 130 < b < 190:
            return 'beige'
        
        # Marron
        if 80 < r < 180 and 50 < g < 130 and 20 < b < 90:
            return 'marron'
        
        # Par défaut
        return 'multicolore'
    
    def _detect_type_from_shape(self, img):
        """Détecte le type de vêtement par la forme de l'image"""
        try:
            width, height = img.size
            ratio = height / width if width > 0 else 1
            
            # Maillot / T-shirt : plutôt carré ou légèrement vertical
            if 0.85 <= ratio <= 1.3:
                return 't-shirt'
            
            # Pull : plus vertical
            elif ratio > 1.3:
                return 'pull'
            
            # Pantalon : plus horizontal
            elif ratio < 0.85:
                return 'pantalon'
            
            return 'vêtement'
            
        except Exception as e:
            print(f"   ⚠️ Erreur type: {e}")
            return 'vêtement'
    
    def _default_result(self):
        """Résultat par défaut en cas d'erreur"""
        return {
            "type": "vêtement",
            "marque": "À préciser",
            "couleur": "à préciser",
            "etat": "Bon",
            "taille": "À préciser",
            "matiere": "À préciser",
            "details": "Article à détailler"
        }


# Test du module
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        analyzer = ImageAnalyzer()
        result = analyzer.analyze_product(sys.argv[1])
        
        import json
        print("\n" + "="*50)
        print("RÉSULTAT FINAL:")
        print("="*50)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Usage: python image_analyzer.py chemin/vers/image.jpg")
