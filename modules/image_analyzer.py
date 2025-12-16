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
        """Classifie un pixel AVEC PRÉCISION"""
        
        # NOIR (très sombre)
        if r < 60 and g < 60 and b < 60:
            return 'noir'
        
        # BLANC (très clair)
        if r > 210 and g > 210 and b > 210:
            return 'blanc'
        
        # GRIS (nuances proches mais pas noir/blanc)
        if abs(r - g) < 40 and abs(g - b) < 40:
            if 60 <= r <= 210:
                return 'gris'
        
        # ROUGE (rouge doit être DOMINANT)
        if r > g + 80 and r > b + 80:
            return 'rouge'
        
        # BLEU (bleu doit être DOMINANT)
        if b > r + 70 and b > g + 50:
            return 'bleu'
        
        # VERT
        if g > r + 70 and g > b + 70:
            return 'vert'
        
        # JAUNE
        if r > 190 and g > 190 and b < 110:
            return 'jaune'
        
        # ORANGE
        if r > 190 and 90 < g < 180 and b < 80:
            return 'orange'
        
        # ROSE
        if r > 160 and b > 130 and g < 140:
            return 'rose'
        
        # VIOLET
        if r > 110 and b > 110 and g < 90:
            return 'violet'
        
        # MARRON (rouge-brun)
        if r > g + 30 and g > b + 20 and 70 < r < 160:
            return 'marron'
        
        # BEIGE (tons chair/crème)
        if 160 < r < 235 and 140 < g < 215 and 100 < b < 180:
            return 'beige'
        
        # OR (jaune-doré)
        if r > 195 and 150 < g < 210 and b < 90:
            return 'or'
        
        # Par défaut
        return 'multicolore'
    
    def _detect_brand(self, colors):
        """Détecte la marque STRICTEMENT"""
        try:
            color_set = set(colors)
            
            # RÈGLE STRICTE : Ne détecter une marque QUE si les couleurs matchent EXACTEMENT
            
            # Barcelona = BLEU + ROUGE ensemble (pas juste bleu ou rouge seul)
            if 'bleu' in colors and 'rouge' in colors:
                # Vérifier que ce sont les 2 couleurs dominantes
                if colors[0] in ['bleu', 'rouge'] and colors[1] in ['bleu', 'rouge']:
                    return 'Barcelona'
            
            # PSG = BLEU dominant + ROUGE (mais PSG a plus de bleu)
            if 'bleu' in colors and colors[0] == 'bleu':
                if 'rouge' in colors:
                    return 'Psg'
            
            # Bayern = ROUGE dominant (et pas d'autres couleurs vives)
            if 'rouge' in colors and colors[0] == 'rouge':
                if 'bleu' not in colors:  # Pas de bleu sinon = Barça
                    return 'Bayern'
            
            # Real Madrid = BLANC dominant + OR/JAUNE
            if 'blanc' in colors and colors[0] == 'blanc':
                if 'or' in colors or 'jaune' in colors:
                    return 'Real Madrid'
            
            # France = BLEU dominant seul (sans rouge ni jaune vif)
            if 'bleu' in colors and colors[0] == 'bleu':
                if 'rouge' not in colors:  # Pas de rouge sinon = Barça/PSG
                    return 'France'
            
            # Marseille = BLANC + BLEU
            if 'blanc' in colors and 'bleu' in colors:
                return 'Marseille'
            
            # AUCUNE MARQUE DÉTECTÉE = Ne pas inventer !
            return "À préciser"
            
        except:
            return "À préciser"
    
    def _detect_type(self, ratio, colors, marque):
        """Détecte le type - Version RÉALISTE"""
        
        # PRIORITÉ 1 : Maillots d'équipes (SI marque équipe détectée avec certitude)
        team_brands = ['Real Madrid', 'Barcelona', 'Psg', 'Bayern', 'France', 'Marseille']
        if marque in team_brands:
            return "maillot"
        
        # PRIORITÉ 2 : Détection STRICTE par RATIO uniquement
        # (On ne peut PAS différencier sac/t-shirt/maillot juste avec couleurs)
        
        # Très horizontal = Chaussures
        if ratio < 0.6:
            return "chaussures"
        
        # Horizontal = Pantalon
        elif 0.6 <= ratio < 0.85:
            return "pantalon"
        
        # Carré = Peut être T-SHIRT, MAILLOT ou SAC
        # IMPOSSIBLE de différencier sans IA avancée !
        # Par DÉFAUT = t-shirt (le plus courant)
        elif 0.85 <= ratio <= 1.4:
            # Si couleurs TRÈS vives (sport typique) = PEUT-ÊTRE maillot
            sport_colors = ['rouge', 'bleu', 'vert', 'jaune', 'orange']
            if len([c for c in colors if c in sport_colors]) >= 2:
                # Au moins 2 couleurs sport vives = probablement maillot
                return "maillot"
            
            # Sinon, on met t-shirt par défaut
            # L'utilisateur pourra corriger en "sac" ou "maillot" manuellement
            return "t-shirt"
        
        # Vertical = Pull
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
