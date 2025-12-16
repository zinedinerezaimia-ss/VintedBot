"""
Générateur de descriptions
"""

import random

class DescriptionGenerator:
    
    def __init__(self):
        self.templates = {
            "maillot": [
                "{m}Maillot {c} authentique ! {e}, porté peu. Matière respirante. Logo et écusson en parfait état. Parfait pour les vrais fans ! ⚽ Taille {t}. Envoi rapide 📦",
                "{m}Superbe maillot {c} ! {e}. Matière technique confortable. Pour les collectionneurs et supporters ! ⚽ Taille {t}. Expédition soignée 📦"
            ],
            "t-shirt": [
                "{m}T-shirt {c} classique. {e}, porté peu. Coupe confortable. Basique indispensable ! 👕 Taille {t}. Envoi rapide 📦",
                "{m}Joli t-shirt {c}. {e}. S'associe avec tout ! 👕 Taille {t}. Expédition soignée 📦"
            ],
            "pantalon": [
                "{m}Pantalon {c} élégant. {e}. Coupe moderne, très confortable ! 👖 Taille {t}. Envoi rapide 📦",
                "{m}Super pantalon {c} ! {e}. Parfait au quotidien ! 👖 Taille {t}. Expédition soignée 📦"
            ],
            "chaussures": [
                "{m}Chaussures {c} stylées ! {e}. Semelle en bon état, très confortables ! 👟 Pointure {t}. Envoi protégé 📦",
                "{m}Paire de chaussures {c}. {e}. Maintien parfait ! 👟 Pointure {t}. Expédition soignée 📦"
            ],
            "basket": [
                "{m}Basket {c} tendance ! {e}. Design moderne, confort optimal ! 👟 Pointure {t}. Envoi protégé 📦",
                "{m}Superbes baskets {c} ! {e}. Style streetwear ! 👟 Pointure {t}. Expédition soignée 📦"
            ],
            "sac": [
                "{m}Sac à main {c} élégant ! {e}. Plusieurs compartiments pratiques. Style intemporel ! 👜 Envoi rapide 📦",
                "{m}Joli sac {c} polyvalent ! {e}. Très pratique au quotidien ! 👜 Expédition soignée 📦"
            ],
            "pull": [
                "{m}Pull {c} tout doux ! {e}. Très confortable et chaud ! 🧶 Taille {t}. Envoi rapide 📦",
                "{m}Joli pull {c} chaleureux ! {e}. Parfait automne-hiver ! 🧶 Taille {t}. Expédition soignée 📦"
            ]
        }
    
    def generate_title(self, info):
        """Génère le titre"""
        parts = []
        
        if info.get('marque') not in ['À préciser', '']:
            parts.append(info['marque'])
        
        parts.append(info['type'].capitalize())
        
        if info.get('couleur'):
            parts.append(info['couleur'])
        
        if info.get('taille') != 'À préciser':
            parts.append(f"T.{info['taille']}")
        
        return " ".join(parts)[:80]
    
    def generate_description(self, info, price_info):
        """Génère la description"""
        product_type = info['type'].lower()
        
        templates = self.templates.get(product_type, self.templates['t-shirt'])
        template = random.choice(templates)
        
        marque = info.get('marque', '')
        m = f"{marque} - " if marque not in ['À préciser', ''] else ""
        
        c = info.get('couleur', 'coloré')
        
        etat_map = {
            'Neuf': 'Neuf avec étiquette',
            'Très bon': 'Excellent état',
            'Bon': 'Très bon état',
            'Satisfaisant': 'Bon état'
        }
        e = etat_map.get(info.get('etat', 'Bon'), 'Bon état')
        
        taille = info.get('taille', 'À préciser')
        t = taille if taille != 'À préciser' else 'voir photos'
        
        try:
            description = template.format(m=m, c=c, e=e, t=t)
            return description[:500]
        except:
            return f"{m}{product_type.capitalize()} {c}. {e}. Taille {t}. Envoi rapide ! 📦"
    
    def create_full_listing(self, info, price_info):
        """Crée l'annonce complète"""
        return {
            "titre": self.generate_title(info),
            "description": self.generate_description(info, price_info),
            "prix": price_info['prix_recommande'],
            "prix_min": price_info['prix_min'],
            "prix_max": price_info['prix_max']
        }
