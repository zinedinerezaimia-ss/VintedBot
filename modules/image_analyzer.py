"""
Analyseur d'images 100% gratuit avec Hugging Face API
Pas besoin de clé API payante, fonctionne en cloud
"""

import requests
import base64
from PIL import Image
import json
import io

class ImageAnalyzer:
    """Analyse les photos avec Hugging Face (gratuit illimité)"""
    
    def __init__(self):
        # URL de l'API Hugging Face (gratuite)
        self.api_url_blip = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
        self.api_url_vit = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"
        
        # Token gratuit (optionnel mais recommandé pour éviter rate limit)
        # Créer un compte sur huggingface.co et obtenir un token gratuit
        self.headers = {
            "Authorization": "Bearer hf_votre_token_gratuit_ici"  # Optionnel
        }
    
    def query_image(self, image_path):
        """Envoie l'image à l'API Hugging Face"""
        with open(image_path, "rb") as f:
            data = f.read()
        
        response = requests.post(
            self.api_url_blip,
            headers=self.headers,
            data=data,
            timeout=30
        )
        return response.json()
    
    def analyze_with_gpt4free(self, image_path):
        """
        Alternative : utilise GPT4Free (gratuit, pas de clé API)
        Accès gratuit à plusieurs modèles IA
        """
        try:
            # Convertir l'image en base64
            with open(image_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            
            # GPT4Free - API gratuite qui donne accès à plusieurs modèles
            url = "https://api.airforce/v1/chat/completions"
            
            prompt = """Analyse cette image de vêtement/produit et donne-moi ces informations au format JSON strict (pas de texte avant ou après) :
{
  "type": "type exact (t-shirt/pull/pantalon/robe/chaussures/accessoire)",
  "marque": "marque visible ou 'Non identifiée'",
  "couleur": "couleur principale",
  "etat": "Neuf/Très bon/Bon/Satisfaisant",
  "taille": "taille visible ou 'Non visible'",
  "matiere": "matière probable",
  "details": "détails importants (motifs, style)"
}"""
            
            payload = {
                "model": "gpt-4o-mini",  # Modèle gratuit
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_data}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 500
            }
            
            response = requests.post(url, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Extraire le JSON
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    product_info = json.loads(json_match.group())
                    print(f"✅ Produit analysé avec GPT4Free : {product_info['type']}")
                    return product_info
            
        except Exception as e:
            print(f"⚠️ GPT4Free erreur : {e}")
        
        return None
    
    def analyze_product(self, image_path):
        """
        Analyse une image avec plusieurs méthodes gratuites
        Essaie GPT4Free d'abord, puis Hugging Face en fallback
        """
        print("🔍 Analyse de l'image avec IA gratuite...")
        
        # Méthode 1 : GPT4Free (meilleure qualité)
        result = self.analyze_with_gpt4free(image_path)
        if result:
            return result
        
        # Méthode 2 : Hugging Face Inference API
        print("🔄 Tentative avec Hugging Face...")
        try:
            description = self.query_image(image_path)
            
            if isinstance(description, list) and len(description) > 0:
                desc_text = description[0].get('generated_text', '')
                
                # Parser la description pour extraire les infos
                product_info = self._parse_description(desc_text)
                print(f"✅ Produit analysé avec HF : {product_info['type']}")
                return product_info
                
        except Exception as e:
            print(f"⚠️ Hugging Face erreur : {e}")
        
        # Méthode 3 : Fallback - analyse basique de l'image
        print("⚠️ Utilisation de l'analyse basique...")
        return self._basic_image_analysis(image_path)
    
    def _parse_description(self, description):
        """Parse une description textuelle pour extraire les infos"""
        desc_lower = description.lower()
        
        # Détecter le type
        types = {
            "t-shirt": ["shirt", "tshirt", "tee"],
            "pull": ["sweater", "pullover", "jumper"],
            "pantalon": ["pants", "trousers", "jeans"],
            "robe": ["dress"],
            "chaussures": ["shoes", "sneakers", "boots"],
            "veste": ["jacket", "coat"]
        }
        
        product_type = "vêtement"
        for french, keywords in types.items():
            if any(k in desc_lower for k in keywords):
                product_type = french
                break
        
        # Détecter couleurs
        colors = {
            "noir": ["black"],
            "blanc": ["white"],
            "rouge": ["red"],
            "bleu": ["blue"],
            "vert": ["green"],
            "jaune": ["yellow"],
            "gris": ["gray", "grey"]
        }
        
        color = "mixte"
        for french, keywords in colors.items():
            if any(k in desc_lower for k in keywords):
                color = french
                break
        
        return {
            "type": product_type,
            "marque": "Non identifiée",
            "couleur": color,
            "etat": "Bon",
            "taille": "Non visible",
            "matiere": "À préciser",
            "details": description[:100]
        }
    
    def _basic_image_analysis(self, image_path):
        """Analyse basique sans IA (fallback)"""
        return {
            "type": "vêtement",
            "marque": "Non identifiée",
            "couleur": "À préciser",
            "etat": "Bon",
            "taille": "À préciser",
            "matiere": "À préciser",
            "details": "Veuillez vérifier et compléter les informations"
        }


# Test
if __name__ == "__main__":
    import re
    analyzer = ImageAnalyzer()
    # result = analyzer.analyze_product("chemin/vers/image.jpg")
    # print(result)