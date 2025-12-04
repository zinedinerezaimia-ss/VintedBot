"""
Analyseur d'images avec Hugging Face Vision API (gratuit)
"""

import requests
import base64
from PIL import Image
import json
import time

class ImageAnalyzer:
    """Analyse les photos avec Hugging Face Vision API"""
    
    def __init__(self):
        # API Hugging Face gratuite (pas besoin de token pour usage limité)
        self.caption_api = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
        self.vqa_api = "https://api-inference.huggingface.co/models/dandelin/vilt-b32-finetuned-vqa"
    
    def analyze_product(self, image_path):
        """Analyse complète d'un produit"""
        print("🔍 Analyse de l'image avec IA...")
        
        try:
            # Étape 1 : Obtenir une description générale
            description = self._get_image_caption(image_path)
            print(f"   Description IA : {description}")
            
            # Étape 2 : Poser des questions spécifiques
            product_type = self._ask_question(image_path, "What type of clothing is this? shirt, sweater, pants, dress, shoes, or jacket?")
            color = self._ask_question(image_path, "What is the main color?")
            brand = self._ask_question(image_path, "What brand logo is visible?")
            
            print(f"   Type détecté : {product_type}")
            print(f"   Couleur : {color}")
            print(f"   Marque : {brand}")
            
            # Étape 3 : Parser et nettoyer les résultats
            result = self._build_product_info(description, product_type, color, brand)
            
            print(f"✅ Analyse terminée : {result['type']} {result['couleur']}")
            return result
            
        except Exception as e:
            print(f"⚠️ Erreur IA, utilisation analyse basique : {e}")
            return self._fallback_analysis(image_path)
    
    def _get_image_caption(self, image_path):
        """Obtient une description de l'image"""
        try:
            with open(image_path, "rb") as f:
                data = f.read()
            
            response = requests.post(
                self.caption_api,
                headers={"Content-Type": "application/octet-stream"},
                data=data,
                timeout=30
            )
            
            if response.status_code == 503:
                # Modèle en chargement, attendre un peu
                print("   ⏳ Modèle en chargement, 2e tentative...")
                time.sleep(3)
                response = requests.post(
                    self.caption_api,
                    headers={"Content-Type": "application/octet-stream"},
                    data=data,
                    timeout=30
                )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '')
            
            return ""
            
        except Exception as e:
            print(f"   ⚠️ Caption API erreur : {e}")
            return ""
    
    def _ask_question(self, image_path, question):
        """Pose une question sur l'image (Visual Question Answering)"""
        try:
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            # Convertir en base64 pour l'API VQA
            image_b64 = base64.b64encode(image_data).decode()
            
            payload = {
                "inputs": {
                    "question": question,
                    "image": image_b64
                }
            }
            
            response = requests.post(
                self.vqa_api,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30
            )
            
            if response.status_code == 503:
                time.sleep(3)
                response = requests.post(
                    self.vqa_api,
                    headers={"Content-Type": "application/json"},
                    json=payload,
                    timeout=30
                )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('answer', '').lower()
            
            return ""
            
        except Exception as e:
            print(f"   ⚠️ VQA erreur : {e}")
            return ""
    
    def _build_product_info(self, description, product_type, color, brand):
        """Construit les infos produit à partir des réponses"""
        
        # Nettoyer et mapper le type
        type_mapping = {
            "shirt": "t-shirt",
            "t-shirt": "t-shirt",
            "tshirt": "t-shirt",
            "jersey": "maillot",
            "football jersey": "maillot",
            "soccer jersey": "maillot",
            "sweater": "pull",
            "pullover": "pull",
            "hoodie": "sweat",
            "pants": "pantalon",
            "trousers": "pantalon",
            "jeans": "jean",
            "dress": "robe",
            "shoes": "chaussures",
            "sneakers": "baskets",
            "jacket": "veste",
            "coat": "manteau"
        }
        
        detected_type = "vêtement"
        for keyword, french_type in type_mapping.items():
            if keyword in product_type.lower() or keyword in description.lower():
                detected_type = french_type
                break
        
        # Détecter "jersey" ou "football" dans la description
        if "jersey" in description.lower() or "football" in description.lower() or "soccer" in description.lower():
            detected_type = "maillot"
        
        # Nettoyer la couleur
        color_mapping = {
            "white": "blanc",
            "black": "noir",
            "red": "rouge",
            "blue": "bleu",
            "green": "vert",
            "yellow": "jaune",
            "gray": "gris",
            "grey": "gris",
            "pink": "rose",
            "purple": "violet",
            "orange": "orange",
            "brown": "marron",
            "beige": "beige"
        }
        
        detected_color = "à préciser"
        for eng, fr in color_mapping.items():
            if eng in color.lower() or eng in description.lower():
                detected_color = fr
                break
        
        # Nettoyer la marque
        common_brands = ["nike", "adidas", "zara", "h&m", "puma", "real madrid", "barcelona", "psg"]
        detected_brand = "À préciser"
        
        brand_lower = brand.lower()
        desc_lower = description.lower()
        
        for b in common_brands:
            if b in brand_lower or b in desc_lower:
                detected_brand = b.title()
                break
        
        return {
            "type": detected_type,
            "marque": detected_brand,
            "couleur": detected_color,
            "etat": "Bon",
            "taille": "À préciser",
            "matiere": "À préciser",
            "details": description[:100] if description else f"{detected_type} {detected_color}"
        }
    
    def _fallback_analysis(self, image_path):
        """Analyse de secours si l'IA ne marche pas"""
        try:
            img = Image.open(image_path)
            
            # Analyse basique de couleur
            img_small = img.resize((50, 50))
            pixels = list(img_small.getdata())
            
            # Moyenne RGB
            avg_r = sum(p[0] for p in pixels) / len(pixels)
            avg_g = sum(p[1] for p in pixels) / len(pixels)
            avg_b = sum(p[2] for p in pixels) / len(pixels)
            
            # Déterminer couleur
            if avg_r > 200 and avg_g > 200 and avg_b > 200:
                color = "blanc"
            elif avg_r < 80 and avg_g < 80 and avg_b < 80:
                color = "noir"
            elif avg_r > avg_g + 30 and avg_r > avg_b + 30:
                color = "rouge"
            elif avg_b > avg_r + 30 and avg_b > avg_g + 30:
                color = "bleu"
            else:
                color = "multicolore"
            
            return {
                "type": "vêtement",
                "marque": "À préciser",
                "couleur": color,
                "etat": "Bon",
                "taille": "À préciser",
                "matiere": "À préciser",
                "details": f"Article {color}"
            }
            
        except:
            return {
                "type": "vêtement",
                "marque": "À préciser",
                "couleur": "à préciser",
                "etat": "Bon",
                "taille": "À préciser",
                "matiere": "À préciser",
                "details": "Article à détailler"
            }


# Test
if __name__ == "__main__":
    analyzer = ImageAnalyzer()
    # result = analyzer.analyze_product("test.jpg")
    # print(json.dumps(result, indent=2, ensure_ascii=False))
