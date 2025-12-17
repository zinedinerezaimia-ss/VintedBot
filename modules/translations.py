# modules/translations.py
"""
Traductions multilingues pour le bot Vinted
"""

TRANSLATIONS = {
    'fr': {
        # Types de vêtements
        'types': {
            'pull': 'Pull',
            't-shirt': 'T-shirt',
            'sweat': 'Sweat',
            'pantalon': 'Pantalon',
            'jean': 'Jean',
            'veste': 'Veste',
            'manteau': 'Manteau',
            'robe': 'Robe',
            'jupe': 'Jupe',
            'short': 'Short',
            'chemise': 'Chemise',
            'chaussures': 'Chaussures',
            'baskets': 'Baskets',
            'sac': 'Sac',
            'accessoire': 'Accessoire',
            'maillot': 'Maillot',
            'jogging': 'Jogging'
        },
        
        # Couleurs
        'colors': {
            'noir': 'noir',
            'blanc': 'blanc',
            'gris': 'gris',
            'bleu': 'bleu',
            'rouge': 'rouge',
            'vert': 'vert',
            'jaune': 'jaune',
            'rose': 'rose',
            'violet': 'violet',
            'marron': 'marron',
            'beige': 'beige',
            'orange': 'orange',
            'multicolore': 'multicolore'
        },
        
        # États
        'conditions': {
            'neuf': 'neuf avec étiquette',
            'très bon': 'très bon état',
            'bon': 'bon état',
            'satisfaisant': 'satisfaisant'
        },
        
        # Phrases d'introduction
        'intros': [
            "Magnifique {item} {color} en {condition}.",
            "Superbe {item} {color}, {condition}.",
            "{item} {color} impeccable, {condition}.",
            "Très beau {item} {color} en {condition}.",
            "{item} {color} en excellent état, {condition}."
        ],
        
        # Détails par type
        'type_details': {
            'pull': "Parfait pour les saisons froides. Coupe confortable et moderne.",
            'sweat': "Idéal pour un look décontracté. Confortable et chaud.",
            't-shirt': "Basique indispensable. Facile à porter au quotidien.",
            'chaussures': "Confortables et stylées. Semelle en bon état.",
            'sac': "Pratique et élégant. Plusieurs compartiments.",
            'pantalon': "Coupe moderne. S'adapte à toutes les morphologies.",
            'jean': "Denim de qualité. Coupe tendance.",
            'veste': "Pièce polyvalente. Parfaite pour la mi-saison.",
            'maillot': "Pièce collector pour les fans ! Floquage en bon état.",
            'robe': "Coupe flatteuse et élégante. Parfaite pour toute occasion.",
            'short': "Idéal pour l'été. Coupe confortable."
        },
        
        # Textes marque
        'brand_texts': {
            'with_brand': "Marque : {brand}.\nAuthentique et de qualité.",
            'no_brand': "Article de qualité."
        },
        
        # Détails état
        'condition_details': {
            'neuf': "État neuf avec étiquette. Jamais porté.",
            'très bon': "Très bon état. Porté avec soin, aucun défaut visible.",
            'bon': "Bon état général. Quelques signes d'usage normaux.",
            'satisfaisant': "État satisfaisant. Traces d'utilisation visibles mais portable."
        },
        
        # Infos pratiques
        'practical_info': [
            "📦 Envoi rapide et soigné sous 24-48h.",
            "🚚 Expédition rapide et protégée.",
            "✅ Envoi le jour même si commande avant 14h.",
            "📮 Colis préparé avec soin et envoyé rapidement."
        ],
        
        # Call to action
        'cta': [
            "N'hésitez pas à me contacter pour plus d'infos ou de photos ! 😊",
            "Des questions ? Contactez-moi, je réponds rapidement ! 💬",
            "Possibilité de négocier le prix, faites une offre ! 💰",
            "Plus de photos sur demande. N'hésitez pas ! 📸"
        ],
        
        # Adjectifs
        'adjectives': ['Magnifique', 'Superbe', 'Beau', 'Joli', 'Élégant'],
        
        # Mots de style
        'style_words': ['stylé', 'tendance', 'mode', 'fashion', 'cool']
    },
    
    'en': {
        'types': {
            'pull': 'Sweater',
            't-shirt': 'T-shirt',
            'sweat': 'Sweatshirt',
            'pantalon': 'Pants',
            'jean': 'Jeans',
            'veste': 'Jacket',
            'manteau': 'Coat',
            'robe': 'Dress',
            'jupe': 'Skirt',
            'short': 'Shorts',
            'chemise': 'Shirt',
            'chaussures': 'Shoes',
            'baskets': 'Sneakers',
            'sac': 'Bag',
            'accessoire': 'Accessory',
            'maillot': 'Jersey',
            'jogging': 'Joggers'
        },
        
        'colors': {
            'noir': 'black',
            'blanc': 'white',
            'gris': 'gray',
            'bleu': 'blue',
            'rouge': 'red',
            'vert': 'green',
            'jaune': 'yellow',
            'rose': 'pink',
            'violet': 'purple',
            'marron': 'brown',
            'beige': 'beige',
            'orange': 'orange',
            'multicolore': 'multicolor'
        },
        
        'conditions': {
            'neuf': 'brand new with tags',
            'très bon': 'excellent condition',
            'bon': 'good condition',
            'satisfaisant': 'satisfactory condition'
        },
        
        'intros': [
            "Beautiful {color} {item} in {condition}.",
            "Gorgeous {color} {item}, {condition}.",
            "Amazing {color} {item} in {condition}.",
            "Lovely {color} {item}, {condition}."
        ],
        
        'type_details': {
            'pull': "Perfect for cold seasons. Comfortable fit.",
            'sweat': "Great for a casual look. Comfortable and warm.",
            't-shirt': "Essential basic. Easy to wear daily.",
            'chaussures': "Comfortable and stylish. Sole in good condition.",
            'sac': "Practical and elegant. Multiple compartments.",
            'pantalon': "Modern cut. Fits all body types.",
            'jean': "Quality denim. Trendy cut.",
            'veste': "Versatile piece. Perfect for mid-season.",
            'maillot': "Collector's item for fans! Flocking in good condition."
        },
        
        'brand_texts': {
            'with_brand': "Brand: {brand}.\nAuthentic and quality.",
            'no_brand': "Quality item."
        },
        
        'condition_details': {
            'neuf': "Brand new with tags. Never worn.",
            'très bon': "Excellent condition. Worn with care.",
            'bon': "Good overall condition. Normal signs of use.",
            'satisfaisant': "Satisfactory condition. Visible signs of use."
        },
        
        'practical_info': [
            "📦 Fast and careful shipping within 24-48h.",
            "🚚 Quick and protected shipping.",
            "✅ Same-day shipping if ordered before 2pm."
        ],
        
        'cta': [
            "Feel free to contact me for more info or photos! 😊",
            "Questions? Contact me, I respond quickly! 💬",
            "Price negotiable, make an offer! 💰"
        ],
        
        'adjectives': ['Beautiful', 'Gorgeous', 'Lovely', 'Amazing', 'Great'],
        'style_words': ['stylish', 'trendy', 'fashionable', 'cool']
    },
    
    'es': {
        'types': {
            'pull': 'Jersey',
            't-shirt': 'Camiseta',
            'sweat': 'Sudadera',
            'pantalon': 'Pantalón',
            'jean': 'Vaqueros',
            'veste': 'Chaqueta',
            'manteau': 'Abrigo',
            'robe': 'Vestido',
            'jupe': 'Falda',
            'short': 'Pantalón corto',
            'chemise': 'Camisa',
            'chaussures': 'Zapatos',
            'baskets': 'Zapatillas',
            'sac': 'Bolso',
            'accessoire': 'Accesorio',
            'maillot': 'Camiseta',
            'jogging': 'Pantalón deportivo'
        },
        
        'colors': {
            'noir': 'negro',
            'blanc': 'blanco',
            'gris': 'gris',
            'bleu': 'azul',
            'rouge': 'rojo',
            'vert': 'verde',
            'jaune': 'amarillo',
            'rose': 'rosa',
            'violet': 'morado',
            'marron': 'marrón',
            'beige': 'beige',
            'orange': 'naranja',
            'multicolore': 'multicolor'
        },
        
        'conditions': {
            'neuf': 'nuevo con etiqueta',
            'très bon': 'muy buen estado',
            'bon': 'buen estado',
            'satisfaisant': 'estado satisfactorio'
        },
        
        'intros': [
            "Precioso {item} {color} en {condition}.",
            "Magnífico {item} {color}, {condition}.",
            "{item} {color} impecable, {condition}."
        ],
        
        'type_details': {
            'pull': "Perfecto para las estaciones frías. Corte cómodo.",
            'sweat': "Ideal para un look casual. Cómodo y caliente.",
            't-shirt': "Básico indispensable. Fácil de llevar.",
            'chaussures': "Cómodos y elegantes. Suela en buen estado.",
            'sac': "Práctico y elegante. Varios compartimentos."
        },
        
        'brand_texts': {
            'with_brand': "Marca: {brand}.\nAuténtico y de calidad.",
            'no_brand': "Artículo de calidad."
        },
        
        'condition_details': {
            'neuf': "Nuevo con etiqueta. Nunca usado.",
            'très bon': "Muy buen estado. Usado con cuidado.",
            'bon': "Buen estado general. Signos normales de uso.",
            'satisfaisant': "Estado satisfactorio. Signos de uso visibles."
        },
        
        'practical_info': [
            "📦 Envío rápido y cuidadoso en 24-48h.",
            "🚚 Envío rápido y protegido."
        ],
        
        'cta': [
            "¡No dudes en contactarme para más info o fotos! 😊",
            "¿Preguntas? ¡Contáctame, respondo rápido! 💬"
        ],
        
        'adjectives': ['Precioso', 'Magnífico', 'Bonito'],
        'style_words': ['estiloso', 'moderno', 'trendy']
    },
    
    'de': {
        'types': {
            'pull': 'Pullover',
            't-shirt': 'T-Shirt',
            'sweat': 'Sweatshirt',
            'pantalon': 'Hose',
            'jean': 'Jeans',
            'veste': 'Jacke',
            'manteau': 'Mantel',
            'robe': 'Kleid',
            'jupe': 'Rock',
            'short': 'Shorts',
            'chemise': 'Hemd',
            'chaussures': 'Schuhe',
            'baskets': 'Sneakers',
            'sac': 'Tasche',
            'accessoire': 'Accessoire',
            'maillot': 'Trikot',
            'jogging': 'Jogginghose'
        },
        
        'colors': {
            'noir': 'schwarz',
            'blanc': 'weiß',
            'gris': 'grau',
            'bleu': 'blau',
            'rouge': 'rot',
            'vert': 'grün',
            'jaune': 'gelb',
            'rose': 'rosa',
            'violet': 'lila',
            'marron': 'braun',
            'beige': 'beige',
            'orange': 'orange',
            'multicolore': 'mehrfarbig'
        },
        
        'conditions': {
            'neuf': 'neu mit Etikett',
            'très bon': 'sehr guter Zustand',
            'bon': 'guter Zustand',
            'satisfaisant': 'zufriedenstellender Zustand'
        },
        
        'intros': [
            "Wunderschönes {item} in {color}, {condition}.",
            "Tolles {item} in {color}, {condition}.",
            "{item} in {color}, {condition}."
        ],
        
        'type_details': {
            'pull': "Perfekt für kalte Jahreszeiten. Bequemer Schnitt.",
            'sweat': "Ideal für einen lässigen Look. Bequem und warm.",
            't-shirt': "Unverzichtbares Basic. Einfach zu tragen.",
            'chaussures': "Bequem und stylish. Sohle in gutem Zustand.",
            'sac': "Praktisch und elegant. Mehrere Fächer."
        },
        
        'brand_texts': {
            'with_brand': "Marke: {brand}.\nAuthentisch und hochwertig.",
            'no_brand': "Qualitätsartikel."
        },
        
        'condition_details': {
            'neuf': "Neu mit Etikett. Nie getragen.",
            'très bon': "Sehr guter Zustand. Sorgfältig getragen.",
            'bon': "Guter Gesamtzustand. Normale Gebrauchsspuren.",
            'satisfaisant': "Zufriedenstellender Zustand. Sichtbare Gebrauchsspuren."
        },
        
        'practical_info': [
            "📦 Schneller und sorgfältiger Versand innerhalb 24-48h.",
            "🚚 Schneller und geschützter Versand."
        ],
        
        'cta': [
            "Kontaktieren Sie mich gerne für weitere Infos oder Fotos! 😊",
            "Fragen? Kontaktieren Sie mich, ich antworte schnell! 💬"
        ],
        
        'adjectives': ['Wunderschön', 'Toll', 'Schön'],
        'style_words': ['stylish', 'trendy', 'modern']
    }
}
