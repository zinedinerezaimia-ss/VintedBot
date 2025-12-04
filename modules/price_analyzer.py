import requests
from bs4 import BeautifulSoup
import statistics
import time

class PriceAnalyzer:
    """Analyse les prix du marché pour un produit donné"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def search_vinted_prices(self, product_type, brand=""):
        """
        Recherche les prix sur Vinted
        
        Args:
            product_type: Type de produit (t-shirt, pull, etc.)
            brand: Marque du produit (optionnel)
            
        Returns:
            list: Liste des prix trouvés
        """
        prices = []
        
        try:
            # Construction de la recherche
            search_query = f"{brand} {product_type}" if brand != "Non identifiée" else product_type
            url = f"https://www.vinted.fr/vetements?search_text={search_query.replace(' ', '+')}"
            
            print(f"🔍 Recherche sur Vinted : {search_query}")
            
            # Note : Vinted bloque souvent le scraping, une vraie implémentation
            # nécessiterait Selenium ou une API officielle
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Chercher les prix (à adapter selon la structure HTML réelle)
                price_elements = soup.find_all('div', class_='ItemBox_price')
                
                for elem in price_elements[:20]:  # Limiter à 20 résultats
                    try:
                        price_text = elem.get_text().strip()
                        # Extraire le nombre (ex: "15,00 €" -> 15.0)
                        price = float(price_text.replace('€', '').replace(',', '.').strip())
                        prices.append(price)
                    except:
                        continue
            
        except Exception as e:
            print(f"⚠️ Erreur Vinted : {str(e)}")
        
        return prices
    
    def search_leboncoin_prices(self, product_type, brand=""):
        """Recherche les prix sur Leboncoin"""
        prices = []
        
        try:
            search_query = f"{brand} {product_type}" if brand != "Non identifiée" else product_type
            url = f"https://www.leboncoin.fr/recherche?category=15&text={search_query.replace(' ', '%20')}"
            
            print(f"🔍 Recherche sur Leboncoin : {search_query}")
            
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Chercher les prix (structure à adapter)
                price_elements = soup.find_all('span', class_='_1F5u3')
                
                for elem in price_elements[:20]:
                    try:
                        price_text = elem.get_text().strip()
                        price = float(price_text.replace('€', '').replace(' ', '').replace(',', '.'))
                        prices.append(price)
                    except:
                        continue
        
        except Exception as e:
            print(f"⚠️ Erreur Leboncoin : {str(e)}")
        
        return prices
    
    def calculate_optimal_price(self, product_info):
        """
        Calcule le prix optimal basé sur l'analyse du marché
        
        Args:
            product_info: Dict avec les infos du produit
            
        Returns:
            dict: prix_min, prix_recommande, prix_max
        """
        all_prices = []
        
        # Collecter les prix de différentes sources
        vinted_prices = self.search_vinted_prices(
            product_info['type'], 
            product_info.get('marque', '')
        )
        all_prices.extend(vinted_prices)
        
        time.sleep(2)  # Pause pour ne pas surcharger les serveurs
        
        leboncoin_prices = self.search_leboncoin_prices(
            product_info['type'],
            product_info.get('marque', '')
        )
        all_prices.extend(leboncoin_prices)
        
        # Si pas de prix trouvés, utiliser des valeurs par défaut
        if not all_prices:
            print("⚠️ Aucun prix trouvé, utilisation des valeurs par défaut")
            return {
                "prix_min": 5.0,
                "prix_recommande": 10.0,
                "prix_max": 15.0,
                "nb_references": 0
            }
        
        # Calculer les statistiques
        prices_sorted = sorted(all_prices)
        
        # Ajustement selon l'état
        etat_multiplier = {
            "Neuf": 1.0,
            "Très bon": 0.8,
            "Bon": 0.6,
            "Satisfaisant": 0.4
        }
        
        multiplier = etat_multiplier.get(product_info.get('etat', 'Bon'), 0.7)
        
        median_price = statistics.median(prices_sorted) * multiplier
        
        return {
            "prix_min": round(median_price * 0.7, 2),
            "prix_recommande": round(median_price, 2),
            "prix_max": round(median_price * 1.3, 2),
            "nb_references": len(all_prices)
        }

# Test
if __name__ == "__main__":
    analyzer = PriceAnalyzer()
    test_product = {
        "type": "t-shirt",
        "marque": "Nike",
        "etat": "Bon"
    }
    # result = analyzer.calculate_optimal_price(test_product)
    # print(result)