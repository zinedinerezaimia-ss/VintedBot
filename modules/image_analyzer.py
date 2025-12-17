# modules/image_analyzer.py
"""
Analyse d'images pour détecter le type de vêtement et les couleurs
"""

from PIL import Image
from collections import Counter
import re

def analyze_image(filepath):
    """
    Analyse une image pour déterminer le type, les couleurs et l'état
    
    Returns:
        tuple: (item_type, colors, condition)
    """
    try:
        img = Image.open(filepath)
        img = img.convert('RGB')
        width, height = img.size
        ratio = height / width if width > 0 else 1
        
        # Échantillonnage des couleurs (50x50 pixels)
        img_small = img.resize((50, 50))
        pixels = list(img_small.getdata())
        
        # Détection des couleurs
        colors_detected = []
        color_categories = {
            'leather': 0,  # Couleurs cuir (marron, beige, camel)
            'sport': 0,    # Couleurs sport vives
            'dark': 0,     # Couleurs sombres
            'white': 0     # Blanc
        }
        
        for r, g, b in pixels:
            # Classification des couleurs
            if r > 200 and g > 200 and b > 200:
                colors_detected.append('blanc')
                color_categories['white'] += 1
            elif r < 50 and g < 50 and b < 50:
                colors_detected.append('noir')
                color_categories['dark'] += 1
            elif 80 < r < 150 and 80 < g < 150 and 80 < b < 150:
                colors_detected.append('gris')
                color_categories['dark'] += 1
            elif b > r + 40 and b > g + 40:
                colors_detected.append('bleu')
                color_categories['sport'] += 1
            elif r > g + 40 and r > b + 40:
                if g > 100:  # Orange
                    colors_detected.append('orange')
                    color_categories['sport'] += 1
                else:  # Rouge
                    colors_detected.append('rouge')
                    color_categories['sport'] += 1
            elif g > r + 30 and g > b + 30:
                colors_detected.append('vert')
                color_categories['sport'] += 1
            elif 100 < r < 180 and 60 < g < 140 and b < 80:
                # Couleurs cuir/marron
                colors_detected.append('marron')
                color_categories['leather'] += 1
            elif 180 < r < 230 and 160 < g < 210 and 130 < b < 180:
                # Beige/camel
                colors_detected.append('beige')
                color_categories['leather'] += 1
        
        # Couleur dominante
        if not colors_detected:
            colors_detected = ['noir']
        
        color_counts = Counter(colors_detected)
        dominant_colors = [color for color, _ in color_counts.most_common(2)]
        
        # DÉTECTION DU TYPE basée sur ratio + couleurs
        total_pixels = len(pixels)
        leather_ratio = color_categories['leather'] / total_pixels
        sport_ratio = color_categories['sport'] / total_pixels
        dark_ratio = color_categories['dark'] / total_pixels
        
        # Logique de détection améliorée
        if ratio < 0.65:
            # Format horizontal = probablement chaussures
            item_type = 'chaussures'
            
        elif ratio > 1.4:
            # Format vertical = sweat ou veste
            if dark_ratio > 0.6 and leather_ratio < 0.1:
                item_type = 'sweat'
            else:
                item_type = 'pull'
                
        elif 0.85 <= ratio <= 1.15:
            # Format carré = sac OU t-shirt
            if leather_ratio > 0.4:
                # Beaucoup de couleurs cuir = probablement un sac
                item_type = 'sac'
            elif sport_ratio > 0.3 and len(set(colors_detected)) > 3:
                # Couleurs variées = possiblement un maillot
                item_type = 'maillot'
            else:
                # Par défaut = t-shirt
                item_type = 't-shirt'
                
        else:
            # Ratio intermédiaire
            if leather_ratio > 0.3:
                item_type = 'sac'
            else:
                item_type = 't-shirt'
        
        # État (simulation basique)
        condition = 'bon'
        
        return item_type, dominant_colors, condition
        
    except Exception as e:
        print(f"❌ Erreur analyse image: {e}")
        return 't-shirt', ['noir'], 'bon'


def detect_brand(filepath):
    """
    Détecte la marque sur l'image (simulation pour l'instant)
    
    Dans une version avancée, on utiliserait :
    - OCR (pytesseract) pour lire le texte
    - Détection de logos (OpenCV + modèle ML)
    
    Returns:
        str or None: Nom de la marque détectée
    """
    # Liste des marques populaires (à étendre)
    COMMON_BRANDS = [
        'Nike', 'Adidas', 'Zara', 'H&M', 'Puma', 
        'The North Face', 'Lacoste', 'Ralph Lauren',
        'Tommy Hilfiger', 'Calvin Klein', 'Levi\'s',
        'Champion', 'Vans', 'Converse', 'New Balance'
    ]
    
    # Pour l'instant, retourne None
    # TODO: Implémenter OCR avec pytesseract
    # TODO: Implémenter détection de logo
    
    return None


def analyze_multiple_photos(filepaths):
    """
    Analyse plusieurs photos et retourne un consensus
    
    Args:
        filepaths: Liste de chemins vers les images
        
    Returns:
        tuple: (item_type, colors, condition, brand)
    """
    if not filepaths:
        return 't-shirt', ['noir'], 'bon', None
    
    types = []
    all_colors = []
    conditions = []
    brands = []
    
    for filepath in filepaths:
        item_type, colors, condition = analyze_image(filepath)
        brand = detect_brand(filepath)
        
        types.append(item_type)
        all_colors.extend(colors)
        conditions.append(condition)
        if brand:
            brands.append(brand)
    
    # Consensus sur le type
    type_counts = Counter(types)
    final_type = type_counts.most_common(1)[0][0]
    
    # Couleurs les plus fréquentes
    color_counts = Counter(all_colors)
    final_colors = [color for color, _ in color_counts.most_common(2)]
    
    # État le plus fréquent
    condition_counts = Counter(conditions)
    final_condition = condition_counts.most_common(1)[0][0]
    
    # Marque (si détectée)
    final_brand = brands[0] if brands else None
    
    return final_type, final_colors, final_condition, final_brand
