"""
Analyseur d'images multi-photos
"""

from PIL import Image
from collections import Counter

class ImageAnalyzer:
    
    def __init__(self):
        self.brand_patterns = {
            'real madrid': {'colors': ['blanc', 'or']},
            'barcelona': {'colors': ['bleu', 'rouge']},
            'psg': {'colors': ['bleu', 'rouge']},
            'bayern': {'colors': ['rouge']},
            'france': {'colors': ['bleu']},
            'marseille': {'colors': ['blanc', 'bleu']}
        }
    
    def analyze_multiple_products(self, image_paths):
        """Analyse toutes les photos"""
        print(f"🔍 Analyse de {len(image_paths)} photo(s)...")
        
        all_analyses = []
        
        for i, path in enumerate(image_paths):
            print(f"   📸 Photo {i+1}/{len(image_paths)}")
            analysis = self._analyze_single(path)
            if analysis:
                all_analyses.append(analysis)
        
        if not all_analyses:
            return self._default_result()
        
        return self._merge_analyses(all_analyses)
    
    def analyze_product(self, image_path):
        """Analyse une photo"""
        return self._analyze_single(image_path)
    
    def _analyze_single(self, image_path):
        """Analyse UNE photo"""
        try:
            img = Image.open(image_path)
            width, height = img.size
            ratio = height / width if width > 0 else 1
            
            colors = self._analyze_colors(img)
            main_color = colors[0] if colors else "noir"
            
            marque = self._detect_brand(colors)
            product_type = self._detect_type(ratio, colors, marque)
            etat = "Bon"
            
            return {
                "type": product_type,
                "marque": marque,
                "couleur": main_color,
                "etat": etat,
                "taille": "À préciser",
                "matiere": "À préciser",
                "details": f"{product_type} {main_color}",
                "colors_found": colors
            }
            
        except Exception as e:
            print(f"   ⚠️ Erreur: {e}")
            return None
    
    def _analyze_colors(self, img):
        """Analyse couleurs"""
        try:
            img_small = img.resize((150, 150))
            if img_small.mode != 'RGB':
                img_small = img_small.convert('RGB')
            
            pixels = list(img_small.getdata())
            
            valid_pixels = [
                p for p in pixels
                if not (p[0] > 225 and p[1] > 225 and p[2] > 225)
            ]
            
            if len(valid_pixels) < 100:
                valid_pixels = pixels
            
            color_counts = {}
            for r, g, b in valid_pixels:
                color = self._classify_color(r, g, b)
                color_counts[color] = color_counts.get(color, 0) + 1
            
            sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
            return [c[0] for c in sorted_colors[:3]]
            
        except:
            return ['noir']
    
    def _classify_color(self, r, g, b):
        """Classifie un pixel"""
        if r < 75 and g < 75 and b < 75:
            return 'noir'
        if r > 195 and g > 195 and b > 195:
            return 'blanc'
        if abs(r - g) < 45 and abs(g - b) < 45:
            return 'gris'
        if r > g + 65 and r > b + 65:
            return 'rouge'
        if b > r + 55 and b > g + 35:
            return 'bleu'
        if g > r + 55 and g > b + 55:
            return 'vert'
        if r > 175 and g > 175 and b < 125:
            return 'jaune'
        if r > 175 and 85 < g < 175 and b < 95:
            return 'orange'
        if r > 145 and b > 115 and g < 145:
            return 'rose'
        if r > g + 25 and g > b + 15 and 75 < r < 175:
            return 'marron'
        if 145 < r < 225 and 125 < g < 205 and 95 < b < 175:
            return 'beige'
        if r > 180 and 140 < g < 200 and b < 100:
            return 'or'
        return 'multicolore'
    
    def _detect_brand(self, colors):
        """Détecte la marque"""
        try:
            color_set = set(colors)
            
            for brand, pattern in self.brand_patterns.items():
                brand_colors = set(pattern['colors'])
                if color_set.intersection(brand_colors):
                    if brand == 'barcelona' and 'bleu' in colors and 'rouge' in colors:
                        return 'Barcelona'
                    elif brand == 'psg' and 'bleu' in colors and 'rouge' in colors:
                        return 'Psg'
                    elif brand == 'bayern' and 'rouge' in colors:
                        return 'Bayern'
                    elif brand == 'real madrid' and 'blanc' in colors:
                        return 'Real Madrid'
            
            return "À préciser"
        except:
            return "À préciser"
    
    def _detect_type(self, ratio, colors, marque):
        """Détecte le type"""
        team_brands = ['Real Madrid', 'Barcelona', 'Psg', 'Bayern', 'France', 'Marseille']
        
        if marque in team_brands:
            return "maillot"
        
        # Sac
        if 0.8 <= ratio <= 1.3:
            leather_colors = ['marron', 'beige', 'noir', 'or']
            if any(c in leather_colors for c in colors):
                return "sac"
        
        if ratio < 0.65:
            if any(c in ['noir', 'marron', 'beige'] for c in colors):
                return "chaussures"
            return "pantalon"
        elif 0.65 <= ratio <= 1.5:
            if any(c in ['rouge', 'bleu', 'vert', 'jaune'] for c in colors):
                return "maillot"
            return "t-shirt"
        else:
            return "pull"
    
    def _merge_analyses(self, analyses):
        """Fusionne les analyses"""
        types = [a['type'] for a in analyses]
        type_counter = Counter(types)
        best_type = type_counter.most_common(1)[0][0]
        
        marques = [a['marque'] for a in analyses if a['marque'] != 'À préciser']
        best_marque = marques[0] if marques else 'À préciser'
        
        all_colors = []
        for a in analyses:
            all_colors.extend(a.get('colors_found', []))
        color_counter = Counter(all_colors)
        best_color = color_counter.most_common(1)[0][0] if color_counter else "noir"
        
        etats = [a['etat'] for a in analyses]
        best_etat = "Bon"
        
        print(f"✅ Résultat: {best_type} {best_marque} {best_color}")
        
        return {
            "type": best_type,
            "marque": best_marque,
            "couleur": best_color,
            "etat": best_etat,
            "taille": "À préciser",
            "matiere": "À préciser",
            "details": f"{best_type} {best_color}"
        }
    
    def _default_result(self):
        return {
            "type": "vêtement",
            "marque": "À préciser",
            "couleur": "noir",
            "etat": "Bon",
            "taille": "À préciser",
            "matiere": "À préciser",
            "details": ""
        }
