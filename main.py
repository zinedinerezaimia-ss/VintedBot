"""
Bot Vinted Automatisé avec IA
Analyse les photos, génère les descriptions et propose les prix
"""

import sys
import os
from pathlib import Path

# Ajouter le dossier modules au path
sys.path.append(str(Path(__file__).parent))

from modules.image_analyzer import ImageAnalyzer
from modules.price_analyzer import PriceAnalyzer
from modules.description_generator import DescriptionGenerator

def print_banner():
    """Affiche le logo du bot"""
    print("""
    ╔═══════════════════════════════════════════╗
    ║     🤖 BOT VINTED AUTOMATISÉ IA 🤖       ║
    ║                                           ║
    ║   Analyse • Prix • Description • Post    ║
    ╚═══════════════════════════════════════════╝
    """)

def process_image(image_path):
    """
    Traite une image complètement : analyse, prix, description
    
    Args:
        image_path: Chemin vers l'image du produit
        
    Returns:
        dict: Toutes les infos de l'annonce
    """
    print(f"\n📸 Traitement de l'image : {image_path}\n")
    
    # ÉTAPE 1 : Analyser l'image
    print("🔍 ÉTAPE 1/3 : Analyse de l'image avec IA...")
    analyzer = ImageAnalyzer()
    product_info = analyzer.analyze_product(image_path)
    
    if not product_info:
        print("❌ Impossible d'analyser l'image")
        return None
    
    print(f"\n   Type : {product_info['type']}")
    print(f"   Marque : {product_info['marque']}")
    print(f"   Couleur : {product_info['couleur']}")
    print(f"   État : {product_info['etat']}")
    print(f"   Taille : {product_info['taille']}")
    
    # ÉTAPE 2 : Analyser les prix du marché
    print("\n💰 ÉTAPE 2/3 : Analyse des prix du marché...")
    price_analyzer = PriceAnalyzer()
    price_info = price_analyzer.calculate_optimal_price(product_info)
    
    print(f"\n   Prix recommandé : {price_info['prix_recommande']}€")
    print(f"   Fourchette : {price_info['prix_min']}€ - {price_info['prix_max']}€")
    print(f"   Basé sur {price_info['nb_references']} références")
    
    # ÉTAPE 3 : Générer l'annonce
    print("\n✍️ ÉTAPE 3/3 : Génération de l'annonce...")
    desc_generator = DescriptionGenerator()
    listing = desc_generator.create_full_listing(product_info, price_info)
    
    print(f"\n   Titre : {listing['titre']}")
    print(f"\n   Description :\n   {listing['description']}")
    
    # Résultat complet
    result = {
        "produit": product_info,
        "prix": price_info,
        "annonce": listing,
        "image_path": image_path
    }
    
    return result

def save_draft(result, output_file="annonce_draft.txt"):
    """Sauvegarde le brouillon de l'annonce"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=" * 50 + "\n")
        f.write("BROUILLON ANNONCE VINTED\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"TITRE :\n{result['annonce']['titre']}\n\n")
        f.write(f"PRIX : {result['annonce']['prix']}€\n\n")
        f.write(f"DESCRIPTION :\n{result['annonce']['description']}\n\n")
        
        f.write("-" * 50 + "\n")
        f.write("INFORMATIONS PRODUIT :\n")
        f.write("-" * 50 + "\n")
        for key, value in result['produit'].items():
            f.write(f"{key.capitalize()} : {value}\n")
        
        f.write("\n" + "-" * 50 + "\n")
        f.write("ANALYSE DES PRIX :\n")
        f.write("-" * 50 + "\n")
        f.write(f"Prix minimum : {result['prix']['prix_min']}€\n")
        f.write(f"Prix recommandé : {result['prix']['prix_recommande']}€\n")
        f.write(f"Prix maximum : {result['prix']['prix_max']}€\n")
        f.write(f"Références analysées : {result['prix']['nb_references']}\n")
    
    print(f"\n✅ Brouillon sauvegardé dans '{output_file}'")

def main():
    """Fonction principale du programme"""
    print_banner()
    
    # Vérifier si une image est fournie
    if len(sys.argv) < 2:
        print("❌ Usage : python main.py chemin/vers/image.jpg")
        print("\nExemple : python main.py data/temp_images/tshirt.jpg")
        return
    
    image_path = sys.argv[1]
    
    # Vérifier que le fichier existe
    if not os.path.exists(image_path):
        print(f"❌ Erreur : Le fichier '{image_path}' n'existe pas")
        return
    
    # Traiter l'image
    try:
        result = process_image(image_path)
        
        if result:
            print("\n" + "=" * 50)
            print("✅ TRAITEMENT TERMINÉ AVEC SUCCÈS")
            print("=" * 50)
            
            # Sauvegarder le brouillon
            save_draft(result)
            
            # Proposer la publication
            print("\n📋 Prochaines étapes :")
            print("   1. Vérifie le brouillon dans 'annonce_draft.txt'")
            print("   2. Ajuste le prix si nécessaire")
            print("   3. Publie manuellement sur Vinted")
            print("\n💡 Astuce : Pour automatiser la publication, il faudra")
            print("   configurer Selenium avec tes identifiants Vinted")
        
    except Exception as e:
        print(f"\n❌ ERREUR : {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()