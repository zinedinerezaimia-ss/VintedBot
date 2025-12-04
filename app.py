"""
Interface Web pour le Bot Vinted
À déployer gratuitement sur Render.com ou Railway.app
"""

from flask import Flask, request, jsonify, render_template_string
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import sys

# Importer nos modules
sys.path.append(str(Path(__file__).parent))
from modules.image_analyzer import ImageAnalyzer
from modules.price_analyzer import PriceAnalyzer
from modules.description_generator import DescriptionGenerator

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['UPLOAD_FOLDER'] = 'uploads'

# Créer le dossier uploads
os.makedirs('uploads', exist_ok=True)

# Initialiser les analyseurs
image_analyzer = ImageAnalyzer()
price_analyzer = PriceAnalyzer()
desc_generator = DescriptionGenerator()

# Template HTML simple
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot Vinted IA - Gratuit</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            text-align: center;
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .upload-zone {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 60px 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            background: #f8f9ff;
        }
        .upload-zone:hover {
            border-color: #764ba2;
            background: #f0f1ff;
        }
        .upload-zone.dragover {
            background: #e8e9ff;
            border-color: #764ba2;
        }
        input[type="file"] { display: none; }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 50px;
            font-size: 18px;
            cursor: pointer;
            margin-top: 20px;
            width: 100%;
            font-weight: bold;
            transition: transform 0.2s;
        }
        .btn:hover { transform: scale(1.05); }
        .btn:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        #preview {
            max-width: 100%;
            max-height: 400px;
            margin: 20px auto;
            display: none;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .result {
            display: none;
            margin-top: 30px;
            padding: 30px;
            background: #f8f9ff;
            border-radius: 15px;
        }
        .result h2 {
            color: #667eea;
            margin-bottom: 20px;
        }
        .info-box {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        .price-box {
            background: #e8fff3;
            border-left-color: #00b894;
        }
        .copy-btn {
            background: #00b894;
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
        }
        .copy-btn:hover { background: #00a085; }
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Bot Vinted IA</h1>
        <p class="subtitle">100% Gratuit • Analyse • Prix • Description</p>
        
        <form id="uploadForm" enctype="multipart/form-data">
            <div class="upload-zone" id="dropZone">
                <h2>📸 Déposez votre photo ici</h2>
                <p>ou cliquez pour sélectionner</p>
                <input type="file" id="fileInput" name="image" accept="image/*" required>
            </div>
            
            <img id="preview" alt="Aperçu">
            
            <button type="submit" class="btn" id="submitBtn">🚀 Analyser mon produit</button>
        </form>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Analyse en cours... Cela peut prendre 10-30 secondes</p>
        </div>
        
        <div class="result" id="result">
            <h2>✅ Annonce générée</h2>
            
            <div class="info-box">
                <strong>📝 Titre :</strong>
                <p id="titre"></p>
                <button class="copy-btn" onclick="copyText('titre')">Copier</button>
            </div>
            
            <div class="info-box price-box">
                <strong>💰 Prix recommandé :</strong>
                <p id="prix"></p>
            </div>
            
            <div class="info-box">
                <strong>📄 Description :</strong>
                <p id="description"></p>
                <button class="copy-btn" onclick="copyText('description')">Copier</button>
            </div>
            
            <div class="info-box">
                <strong>ℹ️ Détails du produit :</strong>
                <div id="details"></div>
            </div>
        </div>
        
        <div class="footer">
            <p>Créé avec ❤️ • 100% Gratuit et Open Source</p>
        </div>
    </div>

    <script>
        const dropZone = document.getElementById('dropZone');
        const fileInput = document.getElementById('fileInput');
        const preview = document.getElementById('preview');
        const form = document.getElementById('uploadForm');
        const loading = document.getElementById('loading');
        const result = document.getElementById('result');

        // Click to upload
        dropZone.onclick = () => fileInput.click();

        // Drag & drop
        dropZone.ondragover = (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        };
        dropZone.ondragleave = () => dropZone.classList.remove('dragover');
        dropZone.ondrop = (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            fileInput.files = e.dataTransfer.files;
            showPreview();
        };

        // Preview
        fileInput.onchange = showPreview;
        function showPreview() {
            const file = fileInput.files[0];
            if (file) {
                preview.src = URL.createObjectURL(file);
                preview.style.display = 'block';
            }
        }

        // Submit
        form.onsubmit = async (e) => {
            e.preventDefault();
            
            const formData = new FormData(form);
            
            loading.style.display = 'block';
            result.style.display = 'none';
            document.getElementById('submitBtn').disabled = true;

            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    document.getElementById('titre').textContent = data.annonce.titre;
                    document.getElementById('prix').textContent = 
                        `${data.annonce.prix}€ (Fourchette: ${data.annonce.prix_min}€ - ${data.annonce.prix_max}€)`;
                    document.getElementById('description').textContent = data.annonce.description;
                    
                    const details = `
                        Type: ${data.produit.type}<br>
                        Marque: ${data.produit.marque}<br>
                        Couleur: ${data.produit.couleur}<br>
                        État: ${data.produit.etat}<br>
                        Taille: ${data.produit.taille}<br>
                        Matière: ${data.produit.matiere}
                    `;
                    document.getElementById('details').innerHTML = details;
                    
                    result.style.display = 'block';
                } else {
                    alert('Erreur: ' + data.error);
                }
            } catch (error) {
                alert('Erreur de connexion: ' + error);
            } finally {
                loading.style.display = 'none';
                document.getElementById('submitBtn').disabled = false;
            }
        };

        function copyText(id) {
            const text = document.getElementById(id).textContent;
            navigator.clipboard.writeText(text);
            alert('✅ Copié !');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Page d'accueil"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    """Endpoint pour analyser une image"""
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'Aucune image fournie'})
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Aucun fichier sélectionné'})
        
        # Sauvegarder temporairement
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analyser l'image
        product_info = image_analyzer.analyze_product(filepath)
        if not product_info:
            return jsonify({'success': False, 'error': 'Impossible d\'analyser l\'image'})
        
        # Analyser les prix
        price_info = price_analyzer.calculate_optimal_price(product_info)
        
        # Générer l'annonce
        listing = desc_generator.create_full_listing(product_info, price_info)
        
        # Supprimer le fichier temporaire
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'produit': product_info,
            'prix': price_info,
            'annonce': listing
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Pour le développement local
    app.run(debug=True, host='0.0.0.0', port=5000)