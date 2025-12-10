"""
Générateur de descriptions OPTIMISÉES algo Vinted
"""

import random

class DescriptionGenerator:
    
    def __init__(self):
        # Templates LONGS et SEO-friendly par type
        self.templates = {
            "maillot": [
                "{marque_txt}Maillot {couleur} officiel et authentique ! {etat_txt}, porté {freq}. Matière technique {tech} pour performances optimales. Logo et écusson en parfait état, sponsors intacts. Parfait pour supporter votre équipe favorite ou pour enrichir votre collection ! ⚽ Coupe {coupe}, taille {taille_txt}. Idéal match, entraînement ou casual. Envoi rapide et soigné en colis protégé 📦✨",
                
                "{marque_txt}Superbe maillot de football {couleur} ! {etat_txt}, peu porté. {tech} respirant, confortable même après plusieurs heures. Logo brodé, écusson thermocollé de qualité. Pour les vrais fans et collectionneurs ! ⚽ Coupe {coupe} moderne, taille {taille_txt}. S'associe parfaitement avec un short de sport. Envoi rapide en colis sécurisé 📦🏆",
                
                "{marque_txt}Magnifique maillot {couleur} collector ! {etat_txt}, conservé avec soin. Matière {tech} anti-transpiration. Tous les détails présents : logo officiel, sponsors, écusson. Indispensable pour tout supporter ! ⚽ Taille {taille_txt}, coupe {coupe}. Parfait pour les matchs au stade ou devant la TV. Expédition soignée 📦⭐"
            ],
            
            "t-shirt": [
                "{marque_txt}T-shirt {couleur} classique et intemporel. {etat_txt}, porté {freq}. Matière {matiere} douce et agréable, {poids}. Coupe {coupe} flatteuse qui tombe parfaitement. Col {col} renforcé, coutures soignées. Basique indispensable de toute garde-robe ! 👕 Taille {taille_txt}. S'associe avec tout : jean, pantalon, short. Idéal {saison}. Envoi rapide 📦",
                
                "{marque_txt}Joli t-shirt {couleur} polyvalent. {etat_txt}, excellent rapport qualité-prix. {matiere} respirant, {poids}. Design {style}, coupe {coupe}. Parfait pour un look {occasion} ! 👕 Couleur qui ne passe pas, lavage après lavage. Taille {taille_txt}. Confortable du matin au soir. Expédition soignée 📦✨"
            ],
            
            "pantalon": [
                "{marque_txt}Pantalon {couleur} élégant et confortable. {etat_txt}, peu porté. Matière {matiere} {qualite}, {poids}. Coupe {coupe} moderne qui affine la silhouette. Ceinture ajustable, poches fonctionnelles {poches}. Taille {taille_txt} qui correspond parfaitement ! 👖 Parfait pour {occasion}. S'associe avec chemise, t-shirt ou pull. Idéal {saison}. Envoi rapide et soigné 📦",
                
                "{marque_txt}Super pantalon {couleur} polyvalent ! {etat_txt}, conservé avec soin. {matiere} résistant et confortable. Coupe {coupe}, taille {taille_txt}. Finitions soignées, coutures renforcées. Parfait au quotidien, travail ou sorties ! 👖 Poches {poches}. Look {style}. Ne se froisse pas. Expédition protégée 📦👌"
            ],
            
            "jean": [
                "{marque_txt}Jean {couleur} authentique. {etat_txt}, denim de qualité {qualite}. Coupe {coupe} tendance, taille {taille_txt} fidèle. Délavage {delavage}, finitions soignées. Poches {poches} renforcées. Confort optimal grâce au tissu {stretch}. 👖 Indispensable garde-robe ! S'associe avec tout. Résiste aux lavages répétés. Envoi rapide 📦",
                
                "{marque_txt}Magnifique jean {couleur} ! {etat_txt}. Denim {qualite}, {poids}. Coupe {coupe} flatteuse. Taille {taille_txt}, délavage {delavage} stylé. Rivets et coutures de qualité. 👖 Parfait casual ou habillé. Confortable toute la journée. Expédition soignée 📦⭐"
            ],
            
            "chaussures": [
                "{marque_txt}Chaussures {couleur} stylées et confortables ! {etat_txt}, portées {freq}. Semelle {semelle} antidérapante en bon état. Intérieur {interieur} propre et bien entretenu. Lacets/fermeture en parfait état. 👟 Pointure {taille_txt}. Maintien optimal du pied, parfaites pour {occasion}. Design {style} intemporel. Envoi en colis renforcé avec papier bulle 📦",
                
                "{marque_txt}Paire de chaussures {couleur} de qualité ! {etat_txt}. Semelle {semelle}, intérieur {interieur}. Pointure {taille_txt} confortable. Très bon maintien, idéales pour marcher toute la journée ! 👟 Style {style} qui se marie avec tout. Aucune trace d'usure visible. Expédition soignée et protégée 📦✨"
            ],
            
            "basket": [
                "{marque_txt}Basket {couleur} tendance ! {etat_txt}, portées {freq}. Semelle {semelle} épaisse et confortable. Amorti optimal pour le confort. Design {style} moderne. 👟 Pointure {taille_txt}. Maintien parfait de la cheville. Lacets en bon état. Parfaites streetwear ou sport ! Envoi protégé en carton renforcé 📦",
                
                "{marque_txt}Superbes baskets {couleur} ! {etat_txt}. Semelle {semelle} antidérapante. Intérieur propre et frais. Pointure {taille_txt}. 👟 Look moderne qui fait tourner les têtes ! Confort testé et approuvé. Expédition rapide et soignée 📦⭐"
            ],
            
            "pull": [
                "{marque_txt}Pull {couleur} tout doux et chaud ! {etat_txt}, porté {freq}. Matière {matiere} {qualite}, {poids}. Coupe {coupe} confortable. Col {col}, manches longues. 🧶 Taille {taille_txt}. Parfait pour {saison} ! Aucun bouloche, aucun accroc. Idéal layering ou seul. Envoi rapide 📦",
                
                "{marque_txt}Joli pull {couleur} chaleureux ! {etat_txt}. {matiere} doux, {poids}. Coupe {coupe}. Taille {taille_txt}. 🧶 Indispensable automne-hiver ! Lave bien, ne rétrécit pas. Confortable et élégant. Expédition soignée 📦✨"
            ],
            
            "sweat": [
                "{marque_txt}Sweat {couleur} confortable ! {etat_txt}, peu porté. Molleton {qualite} tout doux intérieur. Coupe {coupe}, capuche/col {col}. 👔 Taille {taille_txt}. Parfait casual ou sport ! Bords côtelés, poche kangourou. Idéal {saison}. Envoi rapide 📦",
                
                "{marque_txt}Super sweat {couleur} ! {etat_txt}. Matière épaisse et chaude. Coupe {coupe}. Taille {taille_txt}. 👔 Look streetwear ! Très confortable. Expédition soignée 📦⭐"
            ]
        }
        
        # Variables enrichies
        self.variables = {
            "freq": ["peu", "occasionnellement", "avec soin", "quelques fois seulement"],
            "tech": ["Dri-FIT", "Climacool", "respirante", "anti-transpiration", "quick-dry"],
            "coupe": ["ajustée", "slim", "regular", "droite", "moderne", "athletic"],
            "matiere": ["coton", "polyester", "coton bio", "mélange coton-polyester"],
            "qualite": ["premium", "supérieure", "excellente", "haut de gamme"],
            "poids": ["léger", "mi-lourd", "épais"],
            "col": ["rond", "V", "montant", "standard"],
            "style": ["casual", "moderne", "classique", "tendance", "streetwear"],
            "occasion": ["quotidien", "travail", "sorties", "toutes occasions"],
            "saison": ["toute l'année", "été", "mi-saison", "automne-hiver"],
            "poches": ["zippées", "profondes", "latérales", "fonctionnelles"],
            "delavage": ["stone-washed", "brut", "clair", "foncé"],
            "stretch": ["élastique", "stretch confort", "flexible"],
            "semelle": ["gomme", "caoutchouc", "EVA", "composite"],
            "interieur": ["textile", "cuir", "synthétique respirant"],
            "interieur_etat": ["propre", "impeccable", "nickel"]
        }
        
        # États détaillés
        self.etat_texts = {
            "Neuf": "Neuf avec étiquette, jamais porté",
            "Très bon": "Excellent état comme neuf",
            "Bon": "Très bon état général",
            "Satisfaisant": "Bon état d'usage avec légères traces"
        }
    
    def generate_title(self, info):
        """Titre SEO optimisé"""
        parts = []
        
        # Marque en premier
        if info.get('marque') not in ['À préciser', 'Non visible', '']:
            marque_clean = info['marque'].replace('À préciser (logo détecté)', '').strip()
            if marque_clean:
                parts.append(marque_clean)
        
        # Type
        parts.append(info['type'].capitalize())
        
        # Couleur
        if info.get('couleur') and info['couleur'] != 'à préciser':
            parts.append(info['couleur'])
        
        # Taille
        if info.get('taille') not in ['À préciser', 'Non visible']:
            parts.append(f"T.{info['taille']}")
        
        # État court
        etat_map = {'Neuf': 'Neuf', 'Très bon': 'TBE', 'Bon': 'BE'}
        if info.get('etat') in etat_map:
            parts.append(etat_map[info['etat']])
        
        title = " ".join(parts)
        return title[:80]  # Limite Vinted
    
    def generate_description(self, info, price_info):
        """Description LONGUE et SEO"""
        
        product_type = info['type'].lower()
        
        # Choisir template
        if product_type in self.templates:
            templates = self.templates[product_type]
        else:
            templates = self.templates.get('t-shirt', [])
        
        template = random.choice(templates)
        
        # Préparer variables
        marque = info.get('marque', '')
        marque_clean = marque.replace('À préciser (logo détecté)', '').replace('À préciser', '').strip()
        marque_txt = f"{marque_clean} - " if marque_clean else ""
        
        couleur = info.get('couleur', 'coloré')
        etat_txt = self.etat_texts.get(info.get('etat', 'Bon'), 'Très bon état')
        
        taille = info.get('taille', 'À préciser')
        taille_txt = taille if taille != 'À préciser' else 'voir photos'
        
        # Variables aléatoires
        variables = {
            "marque_txt": marque_txt,
            "couleur": couleur,
            "etat_txt": etat_txt,
            "taille_txt": taille_txt,
            "freq": random.choice(self.variables['freq']),
            "tech": random.choice(self.variables['tech']),
            "coupe": random.choice(self.variables['coupe']),
            "matiere": random.choice(self.variables['matiere']),
            "qualite": random.choice(self.variables['qualite']),
            "poids": random.choice(self.variables['poids']),
            "col": random.choice(self.variables['col']),
            "style": random.choice(self.variables['style']),
            "occasion": random.choice(self.variables['occasion']),
            "saison": random.choice(self.variables['saison']),
            "poches": random.choice(self.variables['poches']),
            "delavage": random.choice(self.variables['delavage']),
            "stretch": random.choice(self.variables['stretch']),
            "semelle": random.choice(self.variables['semelle']),
            "interieur": random.choice(self.variables['interieur'])
        }
        
        # Générer
        try:
            description = template.format(**variables)
            return description[:500]  # Limite safe
        except Exception as e:
            print(f"Erreur template: {e}")
            # Fallback simple
            return f"{marque_txt}{product_type.capitalize()} {couleur}. {etat_txt}. Taille {taille_txt}. Envoi rapide ! 📦"
    
    def create_full_listing(self, info, price_info):
        """Annonce complète"""
        
        title = self.generate_title(info)
        description = self.generate_description(info, price_info)
        
        return {
            "titre": title,
            "description": description,
            "prix": price_info['prix_recommande'],
            "prix_min": price_info['prix_min'],
            "prix_max": price_info['prix_max']
        }
