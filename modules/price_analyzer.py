"""
Analyseur de prix INTELLIGENT avec scraping réel
"""

import requests
from bs4 import BeautifulSoup
import statistics
import time
import re

class PriceAnalyzer:
    """Analyse les prix RÉELS sur Vinted, eBay, Leboncoin"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
        }
    
    def calculate_optimal_price(self, product_info):
        """Calcule le prix optimal basé sur le marché RÉEL"""
        print(f"💰 Analyse des prix pour : {product_info['type']} {product_info['couleur']}")
        
        all_prices = []
        
        # 1. Chercher sur Vinted (via API non-officielle)
        vinted_prices = self._get_vinted_prices(product_info)
        all_prices.extend(vinted_prices)
        print(f"   Vinted: {len(vinted_prices)} prix trouvés")
        
        # 2. Chercher sur eBay
        ebay_prices = self._get_ebay_prices(product_info)
        all_prices.extend(ebay_prices)
        print(f"   eBay: {len(ebay_prices)} prix trouvés")
        
        # 3. Chercher sur Leboncoin (limité)
        lbc_prices = self._get_leboncoin_prices(product_info)
        all_prices.extend(lbc_prices)
        print(f"   Leboncoin: {len(lbc_prices)} prix trouvés")
        
        # Si on a trouvé des prix
        if all_prices:
            return self._calculate_statistics(all_prices, product_info)
        else:
            print("   ⚠️ Aucun prix trouvé, utilisation des prix par défaut")
            return self._default_prices(product_info)
    
    def _get_vinted_prices(self, product_info):
        """Scrape les prix Vinted via recherche"""
        prices = []
        
        try:
            # Construction de la recherche
            query = f"{product_info['type']} {product_info['couleur']}"
            if product_info['marque'] not in ['À préciser', 'Non visible']:
                query = f"{product_info['marque']} {query}"
            
            # URL de recherche Vinted
            search_url = f"https://www.vinted.fr/catalog?search_text={query.replace(' ', '+')}"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                # Parser avec regex car Vinted charge dynamiquement
                price_pattern = r'"price"\s*:\s*"?(\d+\.?\d*)"?'
                matches = re.findall(price_pattern, response.text)
                
                for match in matches[:15]:  # Max 15 résultats
                    try:
                        price = float(match)
                        if 1 <= price <= 500:  # Prix raisonnables
                            prices.append(price)
                    except:
                        continue
        
        except Exception as e:
            print(f"   ⚠️ Vinted: {str(e)[:50]}")
        
        return prices
    
    def _get_ebay_prices(self, product_info):
        """Scrape les prix eBay"""
        prices = []
        
        try:
            query = f"{product_info['type']} {product_info['couleur']}"
            if product_info['marque'] not in ['À préciser', 'Non visible']:
                query = f"{product_info['marque']} {query}"
            
            # URL eBay France
            search_url = f"https://www.ebay.fr/sch/i.html?_nkw={query.replace(' ', '+')}&_sop=15"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Chercher les prix (différentes classes possibles)
                price_elements = soup.find_all(['span', 'div'], class_=re.compile(r's-item__price|price'))
                
                for elem in price_elements[:15]:
                    try:
                        price_text = elem.get_text().strip()
                        # Extraire le nombre (ex: "25,50 EUR" -> 25.5)
                        price_match = re.search(r'(\d+)[,.]?(\d*)', price_text)
                        if price_match:
                            price = float(price_match.group(1) + '.' + (price_match.group(2) or '0'))
                            if 1 <= price <= 500:
                                prices.append(price)
                    except:
                        continue
        
        except Exception as e:
            print(f"   ⚠️ eBay: {str(e)[:50]}")
        
        return prices
    
    def _get_leboncoin_prices(self, product_info):
        """Scrape les prix Leboncoin"""
        prices = []
        
        try:
            query = f"{product_info['type']} {product_info['couleur']}"
            
            # URL Leboncoin (catégorie vêtements)
            search_url = f"https://www.leboncoin.fr/recherche?category=15&text={query.replace(' ', '%20')}"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                # Parser les prix
                price_pattern = r'"price"\s*:\s*\[(\d+)\]'
                matches = re.findall(price_pattern, response.text)
                
                for match in matches[:10]:
                    try:
                        price = float(match)
                        if 1 <= price <= 500:
                            prices.append(price)
                    except:
                        continue
        
        except Exception as e:
            print(f"   ⚠️ Leboncoin: {str(e)[:50]}")
        
        return prices
    
    def _calculate_statistics(self, prices, product_info):
        """Calcule les statistiques de prix"""
        
        if len(prices) < 3:
            print("   ⚠️ Pas assez de données, ajustement manuel")
            return self._default_prices(product_info)
        
        # Enlever les outliers (prix extrêmes)
        prices_sorted = sorted(prices)
        q1_idx = len(prices_sorted) // 4
        q3_idx = 3 * len(prices_sorted) // 4
        
        # Prendre le middle 50% (enlever 25% plus bas et 25% plus haut)
        clean_prices = prices_sorted[q1_idx:q3_idx] if len(prices_sorted) > 4 else prices_sorted
        
        if not clean_prices:
            clean_prices = prices_sorted
        
        # Calculer la médiane
        median_price = statistics.median(clean_prices)
        
        # Ajuster selon l'état
        etat_multiplier = {
            "Neuf": 1.0,
            "Très bon": 0.85,
            "Bon": 0.7,
            "Satisfaisant": 0.5
        }
        
        multiplier = etat_multiplier.get(product_info.get('etat', 'Bon'), 0.7)
        adjusted_price = median_price * multiplier
        
        print(f"   ✅ Prix médian trouvé: {median_price:.2f}€")
        print(f"   ✅ Ajusté pour état '{product_info['etat']}': {adjusted_price:.2f}€")
        
        return {
            "prix_min": round(adjusted_price * 0.75, 2),
            "prix_recommande": round(adjusted_price, 2),
            "prix_max": round(adjusted_price * 1.25, 2),
            "nb_references": len(prices)
        }
    
    def _default_prices(self, product_info):
        """Prix par défaut selon le type de produit"""
        
        # Prix de base par type
        base_prices = {
            "t-shirt": 8,
            "maillot": 20,
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
            "accessoire": 5
        }
        
        base_price = base_prices.get(product_info['type'], 10)
        
        # Bonus marque connue
        if product_info.get('marque') not in ['À préciser', 'Non visible']:
            known_brands = ['nike', 'adidas', 'zara', 'h&m', 'puma', 'reebok']
            if product_info['marque'].lower() in known_brands:
                base_price *= 1.3
        
        # Ajustement état
        etat_multiplier = {
            "Neuf": 1.2,
            "Très bon": 1.0,
            "Bon": 0.8,
            "Satisfaisant": 0.6
        }
        
        multiplier = etat_multiplier.get(product_info.get('etat', 'Bon'), 0.8)
        final_price = base_price * multiplier
        
        return {
            "prix_min": round(final_price * 0.7, 2),
            "prix_recommande": round(final_price, 2),
            "prix_max": round(final_price * 1.5, 2),
            "nb_references": 0
        }


# Test
if __name__ == "__main__":
    analyzer = PriceAnalyzer()
    
    test_product = {
        "type": "pantalon",
        "marque": "À préciser",
        "couleur": "noir",
        "etat": "Bon"
    }
    
    result = analyzer.calculate_optimal_price(test_product)
    print(f"\nRésultat: {result}")
