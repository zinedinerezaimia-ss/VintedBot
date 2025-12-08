"""
Générateur de descriptions SEO
"""

import random

class DescriptionGenerator:
    
    def __init__(self):
        self.templates = {
            "maillot": [
                "{m}Maillot {c} authentique ! {e}, porté peu. Technologie respirante. Pour les vrais fans ! ⚽ Logo et écusson parfaits. Collector ! Taille {t}. Envoi rapide 📦",
                "{m}Superbe maillot {c} ! {e}. Matière performance, confortable. Parfait pour supporter votre équipe ! ⚽ Taille {t}. Expédition soignée 📦"
            ],
            "t-shirt": [
                "{m}T-shirt {c}. {e}, coupe confortable. Basique indispensable ! S'associe avec tout. 👕 Taille {t}. Envoi rapide 📦",
                "{m}Tee-shirt {c} de qualité. {e}. Parfait au quotidien ! ✨ Taille {t}. Expédition soignée 📦"
            ],
            "pantalon": [
                "{m}Pantalon {c}. {e}, coupe moderne. Très confortable ! Taille parfaitement. 👖 Taille {t}. Envoi rapide 📦",
                "{m}Super pantalon {c} ! {e}. S'associe avec tout ! Indispensable. 👌 Taille {t}. Expédition soignée 📦"
            ],
            "chaussures": [
                "{m}Chaussures {c}. {e}, semelle en bon état. Très confortables ! Portées peu. 👟 Pointure {t}. Envoi protégé 📦",
                "{m}Paire de chaussures {c} ! {e}. Confort parfait. Style moderne ! 👞 Pointure {t}. Expédition soignée 📦"
            ]
        }
    
    def generate_title(self, info):
        parts = []
        if info.get('marque') not in ['À préciser', 'Non visible']:
            parts.append(info['marque'])
        parts.append(info['type'].capitalize())
        parts.append(info['couleur'])
        if info.get('taille') != 'À préciser':
            parts.append(f"T.{info['taille']}")
        return " ".join(parts)[:80]
    
    def generate_description(self, info, price_info):
        t = info['type'].lower()
        templates = self.templates.get(t, self.templates['t-shirt'])
        template = random.choice(templates)
        
        m = f"{info.get('marque')} - " if info.get('marque') not in ['À préciser', 'Non visible'] else ""
        c = info.get('couleur', 'coloré')
        e = {'Neuf': 'Neuf avec étiquette', 'Très bon': 'Excellent état', 'Bon': 'Très bon état', 'Satisfaisant': 'Bon état'}.get(info.get('etat', 'Bon'), 'Bon état')
        taille = info.get('taille', 'À préciser')
        t_txt = taille if taille != 'À préciser' else 'voir photos'
        
        return template.format(m=m, c=c, e=e, t=t_txt)[:300]
    
    def create_full_listing(self, info, price_info):
        return {
            "titre": self.generate_title(info),
            "description": self.generate_description(info, price_info),
            "prix": price_info['prix_recommande'],
            "prix_min": price_info['prix_min'],
            "prix_max": price_info['prix_max']
        }
