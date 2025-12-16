"""
Analyseur de prix
"""

class PriceAnalyzer:
    
    def __init__(self):
        self.base_prices = {
            "t-shirt": 8,
            "maillot": 25,
            "pull": 15,
            "sweat": 18,
            "pantalon": 15,
            "jean": 20,
            "short": 10,
            "robe": 20,
            "jupe": 12,
            "veste": 30,
            "manteau": 40,
            "chaussures": 25,
            "basket": 30,
            "bottine": 35,
            "sac": 20,
            "accessoire": 5
        }
    
    def calculate_optimal_price(self, product_info):
        """Calcule le prix optimal"""
        
        product_type = product_info.get('type', 'vêtement').lower()
        base_price = self.base_prices.get(product_type, 15)
        
        # Ajustement marque
        marque = product_info.get('marque', '')
        known_brands = ['nike', 'adidas', 'puma', 'zara', 'h&m', 'psg', 'real madrid', 'barcelona', 'bayern']
        if any(brand in marque.lower() for brand in known_brands):
            base_price = int(base_price * 1.3)
        
        # Ajustement état
        etat = product_info.get('etat', 'Bon')
        etat_multipliers = {
            'Neuf': 1.2,
            'Très bon': 1.0,
            'Bon': 0.8,
            'Satisfaisant': 0.6
        }
        multiplier = etat_multipliers.get(etat, 0.8)
        
        prix_recommande = int(base_price * multiplier)
        prix_min = max(5, int(prix_recommande * 0.7))
        prix_max = int(prix_recommande * 1.5)
        
        return {
            "prix_recommande": prix_recommande,
            "prix_min": prix_min,
            "prix_max": prix_max
        }
