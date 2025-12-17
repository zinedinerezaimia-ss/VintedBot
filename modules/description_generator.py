# modules/description_generator.py
"""
Génération de titres et descriptions attractifs pour Vinted
"""

import random
from .translations import TRANSLATIONS

def generate_listing(item_type, colors, condition, brand=None, language='fr', price=None):
    """
    Génère un titre et une description optimisés pour Vinted
    
    Args:
        item_type: Type de vêtement
        colors: Liste des couleurs
        condition: État
        brand: Marque (optionnel)
        language: Langue ('fr', 'en', 'es', 'de')
        price: Prix suggéré (optionnel)
        
    Returns:
        tuple: (title, description)
    """
    trans = TRANSLATIONS.get(language, TRANSLATIONS['fr'])
    
    # Traductions
    type_name = trans['types'].get(item_type, item_type)
    color_name = trans['colors'].get(colors[0], colors[0]) if colors else 'multicolore'
    condition_name = trans['conditions'].get(condition, condition)
    
    # ===== GÉNÉRATION DU TITRE =====
    title = generate_title(type_name, color_name, brand, trans)
    
    # ===== GÉNÉRATION DE LA DESCRIPTION =====
    description = generate_description(
        type_name, color_name, condition_name, brand, trans, price
    )
    
    return title, description


def generate_title(item_type, color, brand, trans):
    """
    Génère un titre accrocheur
    
    Format optimal pour Vinted :
    - Max 100 caractères
    - Inclut : Marque + Type + Couleur
    - Mots-clés importants au début
    """
    if brand:
        # Avec marque : "Nike Sweat noir" ou "Sweat Nike noir"
        templates = [
            f"{brand} {item_type} {color}",
            f"{item_type} {brand} {color}",
            f"{brand} - {item_type} {color}"
        ]
    else:
        # Sans marque : "Sweat noir" ou "Beau sweat noir"
        templates = [
            f"{item_type} {color}",
            f"{trans.get('adjectives', ['Beau'])[0]} {item_type} {color}",
            f"{item_type} {color} {trans.get('style_words', ['stylé'])[0]}"
        ]
    
    return random.choice(templates).strip()


def generate_description(item_type, color, condition, brand, trans, price=None):
    """
    Génère une description complète et engageante
    
    Structure optimale :
    1. Phrase d'accroche
    2. Détails du produit
    3. Prix (si fourni)
    4. État et entretien
    5. Informations pratiques
    6. Appel à l'action
    """
    
    # 1. PHRASE D'ACCROCHE
    intros = trans.get('intros', [
        "Magnifique {item} {color} en {condition}.",
        "Superbe {item} {color}, {condition}.",
        "{item} {color} en {condition}."
    ])
    
    intro_template = random.choice(intros)
    intro = intro_template.format(
        item=item_type,
        color=color,
        condition=condition
    )
    
    # 2. DÉTAILS MARQUE (correction: pas de répétition)
    if brand:
        brand_section = trans.get('brand_texts', {
            'with_brand': "Marque : {brand}.\nAuthentique et de qualité.",
        })['with_brand'].format(brand=brand)
    else:
        brand_section = None  # On ne met rien si pas de marque
    
    # 3. DÉTAILS SPÉCIFIQUES AU TYPE
    type_details = get_type_specific_details(item_type, trans)
    
    # 4. PRIX (si fourni)
    price_section = None
    if price:
        price_section = f"💰 Prix : {price}"
    
    # 5. ÉTAT ET ENTRETIEN
    condition_details = trans.get('condition_details', {
        'neuf': "État neuf avec étiquette. Jamais porté.",
        'très bon': "Très bon état. Porté avec soin.",
        'bon': "Bon état général. Quelques signes d'usage normaux.",
        'satisfaisant': "État satisfaisant. Traces d'utilisation visibles."
    }).get(condition, "Bon état général.")
    
    # 6. INFOS PRATIQUES
    practical_info = trans.get('practical_info', [
        "📦 Envoi rapide et soigné sous 24-48h.",
        "🚚 Expédition rapide et protégée.",
        "✅ Envoi le jour même si commande avant 14h."
    ])
    
    practical = random.choice(practical_info)
    
    # 7. APPEL À L'ACTION
    cta = trans.get('cta', [
        "N'hésitez pas à me contacter pour plus d'infos ou de photos ! 😊",
        "Des questions ? Contactez-moi, je réponds rapidement ! 💬",
        "Possibilité de négocier le prix, faites une offre ! 💰"
    ])
    
    closing = random.choice(cta)
    
    # ASSEMBLAGE (on filtre None pour éviter les sections vides)
    sections = [
        intro,
        brand_section,
        type_details,
        price_section,
        condition_details,
        practical,
        closing
    ]
    
    description = "\n\n".join(filter(None, sections))
    
    return description


def get_type_specific_details(item_type, trans):
    """
    Retourne des détails spécifiques selon le type d'article
    """
    details_map = {
        'pull': trans.get('type_details', {}).get('pull', "Parfait pour les saisons froides. Coupe confortable."),
        'sweat': trans.get('type_details', {}).get('sweat', "Idéal pour un look décontracté. Confortable et chaud."),
        't-shirt': trans.get('type_details', {}).get('t-shirt', "Basique indispensable. Facile à porter au quotidien."),
        'chaussures': trans.get('type_details', {}).get('chaussures', "Confortables et stylées. Semelle en bon état."),
        'sac': trans.get('type_details', {}).get('sac', "Pratique et élégant. Plusieurs compartiments."),
        'pantalon': trans.get('type_details', {}).get('pantalon', "Coupe moderne. S'adapte à toutes les morphologies."),
        'jean': trans.get('type_details', {}).get('jean', "Denim de qualité. Coupe tendance."),
        'veste': trans.get('type_details', {}).get('veste', "Pièce polyvalente. Parfaite pour la mi-saison."),
        'maillot': trans.get('type_details', {}).get('maillot', "Pièce collector pour les fans ! Floquage en bon état.")
    }
    
    return details_map.get(item_type, "Article de qualité.")


def generate_hashtags(item_type, brand, colors):
    """
    Génère des hashtags pertinents (pour Instagram ou description)
    
    Returns:
        str: Chaîne de hashtags
    """
    tags = []
    
    # Type
    tags.append(f"#{item_type}")
    
    # Marque
    if brand:
        tags.append(f"#{brand.replace(' ', '')}")
    
    # Couleurs
    for color in colors:
        tags.append(f"#{color}")
    
    # Tags génériques populaires
    generic_tags = [
        "#vinted", "#secondemain", "#vintedbelgique", "#vintedfrance",
        "#mode", "#fashion", "#stylé", "#tendance"
    ]
    
    tags.extend(random.sample(generic_tags, 3))
    
    return " ".join(tags)


def optimize_for_search(title, description):
    """
    Optimise le titre et la description pour le SEO Vinted
    
    Tips :
    - Mots-clés au début
    - Pas de caractères spéciaux excessifs
    - Longueur optimale
    
    Returns:
        tuple: (optimized_title, optimized_description)
    """
    # Nettoyer le titre
    title = title.strip()
    title = " ".join(title.split())  # Supprimer espaces multiples
    
    # Limiter à 100 caractères
    if len(title) > 100:
        title = title[:97] + "..."
    
    # Description : max 1000 caractères pour Vinted
    if len(description) > 1000:
        description = description[:997] + "..."
    
    return title, description
