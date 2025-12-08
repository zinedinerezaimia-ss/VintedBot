"""
Analyseur MULTI-PHOTOS intelligent
"""

from PIL import Image
import os

class ImageAnalyzer:
    
    def __init__(self):
        pass
    
    def analyze_multiple_products(self, image_paths):
        """Analyse TOUTES les photos pour meilleure précision"""
        print(f"🔍 Analyse de {len(image_paths)} photo(s)...")
        
        all_analyses = []
        
        # Analyser chaque photo
        for i, path in enumerate(image_paths):
            print(f"   📸 Photo {i+1}/{len(image_paths)}...")
            analysis = self._analyze_single(path)
            all_analyses.append(analysis)
        
        # Fusionner les résultats pour avoir le meilleur
        final_result = self._merge_analyses(all_analyses)
        
        print(f"✅ Résultat final: {final_result['type']} {final_result['couleur']}")
        return final_result
    
    def analyze_product(self, image_path):
        """Analyse une seule photo (legacy)"""
        return self._analyze_single(image_path)
    
    def _analyze_single(self, image_path):
        """Analyse UNE photo"""
        try:
            img = Image.open(image_path)
            width, height = img.size
            ratio = height / width if width > 0 else 1
            
            # Analyser couleurs
            colors = self._analyze_colors(img)
            main_color = colors[0] if colors else "multicolore"
            
            # Détecter type par ratio + couleur
            if ratio < 0.7:
                # Horizontal = chaussures ou pantalon
                if main_color in ['noir', 'marron', 'beige', 'blanc', 'gris']:
                    product_type = "chaussures"
                else:
                    product_type = "pantalon"
            elif 0.7 <= ratio <= 1.5:
                # Carré = t-shirt ou maillot
                if main_color in ['rouge', 'bleu', 'vert', 'jaune', 'orange']:
                    product_type = "maillot"
                else:
                    product_type = "t-shirt"
            else:
                # Vertical = pull ou robe
                product_type = "pull"
            
            # Détecter marque (basique - recherche de patterns)
            marque = self._detect_brand(img)
            
            # Évaluer l'état visuel
            etat = self._evaluate_condition(img)
            
            return {
                "type": product_type,
                "marque": marque,
                "couleur": main_color,
                "etat": etat,
                "taille": "À préciser",
                "matiere": "À préciser",
                "details": f"{product_type.capitalize()} {main_color}",
                "ratio": ratio,
                "colors_found": colors
            }
            
        except Exception as e:
            print(f"   ⚠️ Erreur photo: {e}")
            return None
    
    def _merge_analyses(self, analyses):
        """Fusionne les analyses de plusieurs photos pour le meilleur résultat"""
        
        # Filtrer les analyses valides
        valid = [a for a in analyses if a is not None]
        
        if not valid:
            return self._default_result()
        
        # Vote majoritaire pour le type
        types = [a['type'] for a in valid]
        type_votes = {}
        for t in types:
            type_votes[t] = type_votes.get(t, 0) + 1
        best_type = max(type_votes, key=type_votes.get)
        
        # Prendre la couleur la plus fréquente
        all_colors = []
        for a in valid:
            all_colors.extend(a.get('colors_found', []))
        color_votes = {}
        for c in all_colors:
            color_votes[c] = color_votes.get(c, 0) + 1
        best_color = max(color_votes, key=color_votes.get) if color_votes else "multicolore"
        
        # Prendre la marque si détectée
        marques = [a['marque'] for a in valid if a['marque'] != 'À préciser']
        best_marque = marques[0] if marques else 'À préciser'
        
        # État : prendre le meilleur
        etats_priority = {'Neuf': 4, 'Très bon': 3, 'Bon': 2, 'Satisfaisant': 1}
        etats = [a['etat'] for a in valid]
        best_etat = max(etats, key=lambda x: etats_priority.get(x, 0))
        
        print(f"   🧠 Fusion: {len(valid)} photos analysées")
        print(f"   🏆 Type gagnant: {best_type} ({type_votes[best_type]}/{len(valid)} votes)")
        
        return {
            "type": best_type,
            "marque": best_marque,
            "couleur": best_color,
            "etat": best_etat,
            "taille": "À préciser",
            "matiere": "À préciser",
            "details": f"{best_type.capitalize()} {best_color} analysé sur {len(valid)} photos"
        }
    
    def _analyze_colors(self, img):
        """Analyse couleurs dominantes"""
        try:
            img_small = img.resize((150, 150))
            if img_small.mode != 'RGB':
                img_small = img_small.convert('RGB')
            
            pixels = list(img_small.getdata())
            
            # Filtrer fond blanc
            valid_pixels = [p for p in pixels if not (p[0] > 230 and p[1] > 230 and p[2] > 230)]
            
            if len(valid_pixels) < 100:
                valid_pixels = pixels
            
            # Compter par zones de couleur
            color_counts = {}
            for r, g, b in valid_pixels:
                color_name = self._classify_color(r, g, b)
                color_counts[color_name] = color_counts.get(color_name, 0) + 1
            
            # Trier par fréquence
            sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
            
            # Retourner top 3
            return [c[0] for c in sorted_colors[:3] if c[1] > len(valid_pixels) * 0.03]
            
        except:
            return ['multicolore']
    
    def _classify_color(self, r, g, b):
        """Classifie un pixel en couleur"""
        
        # Noir
        if r < 70 and g < 70 and b < 70:
            return 'noir'
        
        # Blanc
        if r > 200 and g > 200 and b > 200:
            return 'blanc'
        
        # Gris
        if abs(r - g) < 40 and abs(g - b) < 40:
            if 70 <= r <= 200:
                return 'gris'
        
        # Rouge
        if r > g + 60 and r > b + 60:
            return 'rouge'
        
        # Bleu
        if b > r + 50 and b > g + 30:
            return 'bleu'
        
        # Vert
        if g > r + 50 and g > b + 50:
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
        
        # Marron
        if r > g + 20 and g > b + 10 and 80 < r < 180:
            return 'marron'
        
        # Beige
        if 150 < r < 230 and 130 < g < 210 and 100 < b < 180:
            return 'beige'
        
        return 'multicolore'
    
    def _detect_brand(self, img):
        """Détecte la marque (basique - cherche patterns sombres/clairs pour logos)"""
        try:
            # Convertir en niveau de gris
            gray = img.convert('L')
            gray_small = gray.resize((200, 200))
            pixels = list(gray_small.getdata())
            
            # Chercher zones très contrastées (logos)
            contrasts = []
            for i in range(len(pixels) - 1):
                contrast = abs(pixels[i] - pixels[i+1])
                contrasts.append(contrast)
            
            avg_contrast = sum(contrasts) / len(contrasts)
            
            # Si beaucoup de contraste = probablement un logo
            if avg_contrast > 40:
                # Chercher si c'est des marques connues (pattern matching basique)
                # On pourrait améliorer avec OCR ici
                return "À préciser (logo détecté)"
            
            return "À préciser"
            
        except:
            return "À préciser"
    
    def _evaluate_condition(self, img):
        """Évalue l'état visuel du produit"""
        try:
            # Calculer la netteté (plus c'est net = meilleur état)
            gray = img.convert('L')
            gray_small = gray.resize((300, 300))
            pixels = list(gray_small.getdata())
            
            # Calculer variance (netteté)
            mean = sum(pixels) / len(pixels)
            variance = sum((p - mean) ** 2 for p in pixels) / len(pixels)
            
            # Plus la variance est élevée = image nette = bon état
            if variance > 3000:
                return "Très bon"
            elif variance > 2000:
                return "Bon"
            else:
                return "Bon"  # Par défaut
            
        except:
            return "Bon"
    
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
