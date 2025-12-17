# modules/price_analyzer.py
"""
Analyse de prix basée sur le marché Vinted
"""

import random

def get_price_range(item_type, brand=None, condition='bon'):
    """
    Calcule une fourchette de prix réaliste
    
    Basé sur :
    - Le type d'article
    - La marque (si connue)
    - L'état
    - Les prix moyens du marché Vinted
    
    Args:
        item_type: Type de vêtement
        brand: Marque (optionnel)
        condition: État de l'article
        
    Returns:
        tuple: (price_min, price_max)
    """
    
    # Prix de base par type (en €)
    BASE_PRICES = {
        'pull': (12, 30),
        't-shirt': (5, 18),
        'sweat': (15, 40),
        'pantalon': (12, 35),
        'jean': (15, 40),
        'veste': (20, 60),
        'manteau': (30, 80),
        'robe': (12, 40),
        'jupe': (8, 25),
        'short': (8, 22),
        'chemise': (10, 28),
        'chaussures': (20, 70),
        'baskets': (25, 80),
        'sac': (15, 60),
        'accessoire': (5, 20),
        'maillot': (12, 45),
        'jogging': (15, 35)
    }
    
    # Prix par marque (multiplicateur)
    BRAND_MULTIPLIERS = {
        # Marques premium
        'Nike': 1.8,
        'Adidas': 1.7,
        'The North Face': 2.0,
        'Lacoste': 1.9,
        'Ralph Lauren': 2.0,
        'Tommy Hilfiger': 1.8,
        'Calvin Klein': 1.7,
        
        # Marques moyennes
        'Puma': 1.4,
        'Champion': 1.5,
        'Vans': 1.4,
        'Converse': 1.4,
        'New Balance': 1.5,
        
        # Marques fast fashion
        'Zara': 1.2,
        'H&M': 1.1,
        'Pull&Bear': 1.1,
        'Bershka': 1.1,
        'Mango': 1.2,
        
        # Marques luxe
        'Gucci': 3.5,
        'Louis Vuitton': 4.0,
        'Balenciaga': 3.2,
        'Dior': 3.8,
        'Chanel': 4.2
    }
    
    # Multiplicateurs par état
    CONDITION_MULTIPLIERS = {
        'neuf': 1.3,           # Neuf avec étiquette
        'très bon': 1.1,       # Très bon état
        'bon': 1.0,            # Bon état
        'satisfaisant': 0.7    # Satisfaisant
    }
    
    # Récupération du prix de base
    price_min, price_max = BASE_PRICES.get(item_type, (10, 30))
    
    # Application du multiplicateur de marque
    if brand and brand in BRAND_MULTIPLIERS:
        multiplier = BRAND_MULTIPLIERS[brand]
        price_min = int(price_min * multiplier)
        price_max = int(price_max * multiplier)
    elif brand:
        # Marque inconnue = léger bonus
        price_min = int(price_min * 1.2)
        price_max = int(price_max * 1.3)
    
    # Application du multiplicateur d'état
    condition_multiplier = CONDITION_MULTIPLIERS.get(condition, 1.0)
    price_min = int(price_min * condition_multiplier)
    price_max = int(price_max * condition_multiplier)
    
    # Arrondir à des valeurs esthétiques
    price_min = round_to_nice_number(price_min)
    price_max = round_to_nice_number(price_max)
    
    # S'assurer que max > min
    if price_max <= price_min:
        price_max = price_min + 5
    
    return price_min, price_max


def round_to_nice_number(price):
    """
    Arrondit un prix à un nombre 'joli'
    Ex: 17 -> 15, 23 -> 25, 48 -> 50
    """
    if price < 10:
        return max(5, price)
    elif price < 20:
        return round(price / 5) * 5  # Multiple de 5
    elif price < 50:
        return round(price / 5) * 5  # Multiple de 5
    else:
        return round(price / 10) * 10  # Multiple de 10


def get_suggested_price(item_type, brand=None, condition='bon'):
    """
    Retourne UN prix suggéré (au lieu d'une fourchette)
    
    Returns:
        int: Prix suggéré
    """
    price_min, price_max = get_price_range(item_type, brand, condition)
    
    # Retourne le milieu de la fourchette
    suggested = (price_min + price_max) // 2
    
    return round_to_nice_number(suggested)


def estimate_market_demand(item_type, brand=None):
    """
    Estime la demande du marché pour un article
    
    Returns:
        str: 'high', 'medium', 'low'
    """
    HIGH_DEMAND_ITEMS = ['chaussures', 'baskets', 'sac', 'jean', 'sweat']
    HIGH_DEMAND_BRANDS = ['Nike', 'Adidas', 'The North Face', 'Champion']
    
    if item_type in HIGH_DEMAND_ITEMS:
        return 'high'
    
    if brand in HIGH_DEMAND_BRANDS:
        return 'high'
    
    return 'medium'


def get_pricing_tips(item_type, brand=None, condition='bon'):
    """
    Donne des conseils de prix
    
    Returns:
        list: Liste de conseils
    """
    tips = []
    
    demand = estimate_market_demand(item_type, brand)
    
    if demand == 'high':
        tips.append("📈 Article très recherché ! Vous pouvez viser le haut de la fourchette.")
    
    if condition == 'neuf':
        tips.append("✨ Article neuf = valeur premium ! N'hésitez pas à augmenter le prix.")
    
    if brand in ['Nike', 'Adidas', 'The North Face']:
        tips.append("🏷️ Marque populaire ! Mentionnez-la bien dans le titre.")
    
    if item_type in ['chaussures', 'baskets']:
        tips.append("👟 Précisez bien la pointure dans le titre pour vendre plus vite.")
    
    return tips
