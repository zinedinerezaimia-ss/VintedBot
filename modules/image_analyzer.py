"""
Analyseur ULTRA-INTELLIGENT avec détection marques
"""

from PIL import Image, ImageEnhance, ImageFilter
import os
from collections import Counter

class ImageAnalyzer:
    
    def __init__(self):
        # Patterns de marques connues (logos, couleurs typiques)
        self.brand_patterns = {
            'nike': {'colors': ['noir', 'blanc'], 'keywords': ['swoosh']},
            'adidas': {'colors': ['noir', 'blanc'], 'keywords': ['stripes', '3-bands']},
            'puma': {'colors': ['noir', 'blanc'], 'keywords': ['cat', 'puma']},
            'real madrid': {'colors': ['blanc', 'or'], 'keywords': ['real', 'madrid']},
            'barcelona': {'colors': ['bleu', 'rouge'], 'keywords': ['barca', 'fcb']},
            'psg': {'colors': ['bleu', 'rouge'], 'keywords': ['paris']},
            'bayern': {'colors': ['rouge', 'blanc'], 'keywords': ['fcb', 'bayern']},
            'marseille': {'colors': ['blanc', 'bleu'], 'keywords': ['om']},
            'france': {'colors': ['bleu', 'blanc', 'rouge'], 'keywords': ['fff', 'france']}
        }
    
    def analyze_multiple_products(self, image_paths):
        """Analyse TOUTES les photos pour détection ultra-précise"""
        print(f"🔍 Analyse intelligente de {len(image_paths)} photo(s)...")
        
        all_analyses = []
        
        for i, path in enumerate(image_paths):
            print(f"   📸 Photo {i+1}/{len(image_paths)}...")
            analysis = self._analyze_single(path)
            if analysis:
                all_analyses.append(analysis)
        
        if not all_analyses:
            return self._default_result()
        
        # Fusionner intelligemment
        final_result = self._smart_merge(all_analyses)
        
        print(f"✅ Résultat: {final_result['type']} {final_result['marque']} {final_result['couleur']}")
        return final_result
    
    def analyze_product(self, image_path):
        """Analyse une seule photo"""
        return self._analyze_single(image_path)
    
    def _analyze_single(self, image_path):
        """Analyse INTELLIGENTE d'une photo"""
        try:
            img = Image.open(image_path)
            width, height = img.size
            ratio = height / width if width > 0 else 1
            
            # 1. Analyser couleurs (précis)
            colors = self._analyze_colors_advanced(img)
            main_color = colors[0] if colors else "multicolore"
            
            # 2. Détecter marque (NOUVEAU - INTELLIGENT)
            marque = self._detect_brand_intelligent(img, colors)
            
            # 3. Détecter type avec contexte marque
            product_type = self._detect_type_contextual(ratio, colors, marque)
            
            # 4. Évaluer état (qualité image)
            etat = self._evaluate_condition_smart(img)
            
            # 5. Détecter si logo visible
            has_logo = self._detect_logo_presence(img)
            
            return {
                "type": product_type,
                "marque": marque,
                "couleur": main_color,
                "etat": etat,
                "taille": "À préciser",
                "matiere": "À préciser",
                "details": f"{product_type.capitalize()} {main_color}",
                "ratio": ratio,
                "colors_found": colors,
                "has_logo": has_logo,
                "confidence": self._calculate_confidence(marque, has_logo)
            }
            
        except Exception as e:
            print(f"   ⚠️ Erreur: {e}")
            return None
    
    def _analyze_colors_advanced(self, img):
        """Analyse couleurs ULTRA-PRÉCISE avec zones"""
        try:
            img_resized = img.resize((200, 200))
            if img_resized.mode != 'RGB':
                img_resized = img_resized.convert('RGB')
            
            pixels = list(img_resized.getdata())
            
            # Filtrer fond blanc/gris clair
            valid_pixels = [
                p for p in pixels
                if not (p[0] > 225 and p[1] > 225 and p[2] > 225)
                and not (p[0] < 30 and p[1] < 30 and p[2] < 30)
            ]
            
            if len(valid_pixels) < 100:
                valid_pixels = pixels
            
            # Compter par couleur
            color_counts = {}
            for r, g, b in valid_pixels:
                color_name = self._classify_color_precise(r, g, b)
                color_counts[color_name] = color_counts.get(color_name, 0) + 1
            
            # Top 3 couleurs
            sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
            top_colors = [c[0] for c in sorted_colors[:3] if c[1] > len(valid_pixels) * 0.05]
            
            return top_colors if top_colors else ['multicolore']
            
        except:
            return ['multicolore']
    
    def _classify_color_precise(self, r, g, b):
        """Classification couleur PRÉCISE"""
        
        # Noir
        if r < 75 and g < 75 and b < 75:
            return 'noir'
        
        # Blanc
        if r > 195 and g > 195 and b > 195:
            return 'blanc'
        
        # Gris
        if abs(r - g) < 45 and abs(g - b) < 45:
            if 75 <= r <= 195:
                return 'gris'
        
        # Rouge (large spectre)
        if r > g + 65 and r > b + 65:
            return 'rouge'
        if r > 140 and g < 90 and b < 90:
            return 'rouge'
        
        # Bleu (marine, clair, etc.)
        if b > r + 55 and b > g + 35:
            return 'bleu'
        if b > 100 and b > r * 1.3 and b > g * 1.2:
            return 'bleu'
        
        # Vert
        if g > r + 55 and g > b + 55:
            return 'vert'
        
        # Jaune
        if r > 175 and g > 175 and b < 125:
            return 'jaune'
        
        # Orange
        if r > 175 and 85 < g < 175 and b < 95:
            return 'orange'
        
        # Rose
        if r > 145 and b > 115 and g < 145:
            return 'rose'
        
        # Marron
        if r > g + 25 and g > b + 15 and 75 < r < 175:
            return 'marron'
        
        # Beige
        if 145 < r < 225 and 125 < g < 205 and 95 < b < 175:
            return 'beige'
        
        # Or (pour logos Real Madrid, etc.)
        if r > 180 and 140 < g < 200 and b < 100:
            return 'or'
        
        return 'multicolore'
    
    def _detect_brand_intelligent(self, img, colors):
        """Détection INTELLIGENTE de marque par patterns"""
        try:
            # Convertir couleurs en set
            color_set = set(colors)
            
            # Scores par marque
            brand_scores = {}
            
            for brand, pattern in self.brand_patterns.items():
                score = 0
                
                # Vérifier couleurs typiques
                brand_colors = set(pattern['colors'])
                matching_colors = color_set.intersection(brand_colors)
                score += len(matching_colors) * 30
                
                # Bonus si couleurs exactes de l'équipe
                if brand == 'real madrid' and 'blanc' in colors and len(colors) >= 2:
                    score += 50
                elif brand == 'barcelona' and 'bleu' in colors and 'rouge' in colors:
                    score += 50
                elif brand == 'psg' and 'bleu' in colors and 'rouge' in colors:
                    score += 50
                elif brand == 'bayern' and 'rouge' in colors:
                    score += 50
                elif brand == 'marseille' and 'blanc' in colors and 'bleu' in colors:
                    score += 50
                elif brand == 'france' and 'bleu' in colors:
                    score += 50
                
                brand_scores[brand] = score
            
            # Meilleure marque
            best_brand = max(brand_scores, key=brand_scores.get)
            best_score = brand_scores[best_brand]
            
            # Si score > 60, on a confiance
            if best_score >= 60:
                print(f"   🏷️ Marque détectée: {best_brand.upper()} (score: {best_score})")
                return best_brand.title()
            
            # Sinon, analyser les contrastes pour logos
            has_logo = self._detect_logo_presence(img)
            if has_logo:
                return "À préciser (logo détecté)"
            
            return "À préciser"
            
        except Exception as e:
            print(f"   ⚠️ Détection marque erreur: {e}")
            return "À préciser"
    
    def _detect_logo_presence(self, img):
        """Détecte si un logo est présent (zones contrastées)"""
        try:
            # Convertir en niveaux de gris
            gray = img.convert('L')
            
            # Améliorer contraste
            enhancer = ImageEnhance.Contrast(gray)
            gray = enhancer.enhance(2.0)
            
            # Détecter contours
            edges = gray.filter(ImageFilter.FIND_EDGES)
            
            # Compter pixels de contours
            edge_pixels = list(edges.getdata())
            edge_count = sum(1 for p in edge_pixels if p > 50)
            edge_ratio = edge_count / len(edge_pixels)
            
            # Si beaucoup de contours = logo probable
            if edge_ratio > 0.15:
                return True
            
            return False
            
        except:
            return False
    
    def _detect_type_contextual(self, ratio, colors, marque):
        """Détecte le type avec CONTEXTE (marque + couleurs)"""
        
        # Si marque d'équipe détectée → probablement maillot
        team_brands = ['real madrid', 'barcelona', 'psg', 'bayern', 'marseille', 'france']
        if any(team in marque.lower() for team in team_brands):
            return "maillot"
        
        # Sinon, détection par ratio + couleurs
        if ratio < 0.65:
            # Horizontal
            if any(c in ['noir', 'marron', 'beige'] for c in colors):
                return "chaussures"
            return "pantalon"
        
        elif 0.65 <= ratio <= 1.5:
            # Carré
            sport_colors = ['rouge', 'bleu', 'vert', 'jaune', 'orange']
            if any(c in sport_colors for c in colors):
                return "maillot"
            return "t-shirt"
        
        else:
            # Vertical
            return "pull"
    
    def _evaluate_condition_smart(self, img):
        """Évalue l'état par netteté + luminosité"""
        try:
            gray = img.convert('L')
            gray_small = gray.resize((300, 300))
            pixels = list(gray_small.getdata())
            
            # Variance = netteté
            mean = sum(pixels) / len(pixels)
            variance = sum((p - mean) ** 2 for p in pixels) / len(pixels)
            
            # Luminosité moyenne
            brightness = mean
            
            # Scoring
            if variance > 3500 and brightness > 80:
                return "Très bon"
            elif variance > 2500:
                return "Bon"
            else:
                return "Bon"
                
        except:
            return "Bon"
    
    def _calculate_confidence(self, marque, has_logo):
        """Calcule le niveau de confiance"""
        confidence = 50
        
        if marque not in ['À préciser', 'À préciser (logo détecté)']:
            confidence += 40
        
        if has_logo:
            confidence += 10
        
        return min(confidence, 100)
    
    def _smart_merge(self, analyses):
        """Fusion INTELLIGENTE multi-photos"""
        
        # Vote type
        types = [a['type'] for a in analyses]
        type_counter = Counter(types)
        best_type = type_counter.most_common(1)[0][0]
        
        # Meilleure marque (celle avec meilleur confidence)
        marques_with_conf = [(a['marque'], a.get('confidence', 0)) for a in analyses]
        best_marque = max(marques_with_conf, key=lambda x: x[1])[0]
        
        # Couleurs fusionnées
        all_colors = []
        for a in analyses:
            all_colors.extend(a.get('colors_found', []))
        color_counter = Counter(all_colors)
        best_color = color_counter.most_common(1)[0][0] if color_counter else "multicolore"
        
        # Meilleur état
        etats = [a['etat'] for a in analyses]
        etat_priority = {'Neuf': 4, 'Très bon': 3, 'Bon': 2, 'Satisfaisant': 1}
        best_etat = max(etats, key=lambda x: etat_priority.get(x, 0))
        
        # Vérifier si logo détecté sur au moins une photo
        has_any_logo = any(a.get('has_logo', False) for a in analyses)
        
        print(f"   🧠 Fusion: Type={best_type} ({type_counter[best_type]}/{len(analyses)}), Marque={best_marque}")
        
        return {
            "type": best_type,
            "marque": best_marque,
            "couleur": best_color,
            "etat": best_etat,
            "taille": "À préciser",
            "matiere": "À préciser",
            "details": f"{best_type.capitalize()} {best_color} - Analysé sur {len(analyses)} photos"
        }
    
    def _default_result(self):
        return {
            "type": "vêtement",
            "marque": "À préciser",
            "couleur": "à préciser",
            "etat": "Bon",
            "taille": "À préciser",
            "matiere": "À préciser",
            "details": "Article à détailler"
        }
