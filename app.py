"""
Interface Web Bot Vinted - Version finale
"""

from flask import Flask, request, jsonify, render_template_string
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))
from modules.image_analyzer import ImageAnalyzer
from modules.price_analyzer import PriceAnalyzer
from modules.description_generator import DescriptionGenerator

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs('uploads', exist_ok=True)

image_analyzer = ImageAnalyzer()
price_analyzer = PriceAnalyzer()
desc_generator = DescriptionGenerator()

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
        .edit-form {
            display: none;
            margin-top: 30px;
            padding: 30px;
            background: #f8f9ff;
            border-radius: 15px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            font-weight: bold;
            margin-bottom: 5px;
            color: #333;
        }
        .form-group input, .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }
        .result {
            display: none;
            margin-top: 30px;
            padding: 30px;
            background: #f8f9ff;
            border-radius: 15px;
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
            
            <button type="submit" class="btn" id="submitBtn">🔍 Analyser mon produit</button>
        </form>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Analyse en cours...</p>
        </div>
        
        <div class="edit-form" id="editForm">
            <h2>✏️ Vérifiez et corrigez</h2>
            
            <div class="info-box price-box" style="margin-bottom: 20px;">
                <strong>💰 Prix suggéré :</strong>
                <p id="suggestedPrice"></p>
            </div>
            
            <div class="form-group">
                <label>Type *</label>
                <select id="productType" onchange="updateDesc()">
                    <option value="t-shirt">T-shirt</option>
                    <option value="maillot">Maillot</option>
                    <option value="pull">Pull</option>
                    <option value="pantalon">Pantalon</option>
                    <option value="chaussures">Chaussures</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Marque</label>
                <input type="text" id="brand" placeholder="Nike, Adidas..." oninput="updateDesc()">
            </div>
            
            <div class="form-group">
                <label>Couleur *</label>
                <input type="text" id="color" required oninput="updateDesc()">
            </div>
            
            <div class="form-group">
                <label>Taille</label>
                <select id="size" onchange="updateDesc()">
                    <option value="À préciser">À préciser</option>
                    <option value="XS">XS</option>
                    <option value="S">S</option>
                    <option value="M">M</option>
                    <option value="L">L</option>
                    <option value="XL">XL</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>État *</label>
                <select id="condition" onchange="updateDesc()">
                    <option value="Neuf">Neuf</option>
                    <option value="Très bon">Très bon</option>
                    <option value="Bon" selected>Bon</option>
                    <option value="Satisfaisant">Satisfaisant</option>
                </select>
            </div>
            
            <div class="info-box" style="background: #fff3cd;">
                <strong>📄 Aperçu :</strong>
                <p id="descPreview" style="margin-top:10px; font-style:italic;">La description se met à jour...</p>
            </div>
            
            <button type="button" class="btn" onclick="generateFinal()">✨ Générer l'annonce</button>
        </div>
        
        <div class="result" id="result">
            <h2>✅ Annonce générée</h2>
            
            <div class="info-box">
                <strong>📝 Titre :</strong>
                <p id="titre"></p>
                <button class="copy-btn" onclick="copy('titre')">Copier</button>
            </div>
            
            <div class="info-box price-box">
                <strong>💰 Prix :</strong>
                <p id="prix"></p>
            </div>
            
            <div class="info-box">
                <strong>📄 Description :</strong>
                <p id="description"></p>
                <button class="copy-btn" onclick="copy('description')">Copier</button>
            </div>
            
            <button class="btn" onclick="location.reload()">🔄 Nouvelle annonce</button>
        </div>
    </div>

    <script>
        const dropZone = document.getElementById('dropZone');
        const fileInput = document.getElementById('fileInput');
        const preview = document.getElementById('preview');
        const form = document.getElementById('uploadForm');
        const loading = document.getElementById('loading');
        const editForm = document.getElementById('editForm');
        const result = document.getElementById('result');

        dropZone.onclick = () => fileInput.click();
        fileInput.onchange = () => {
            const file = fileInput.files[0];
            if (file) {
                preview.src = URL.createObjectURL(file);
                preview.style.display = 'block';
            }
        };

        form.onsubmit = async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            
            loading.style.display = 'block';
            editForm.style.display = 'none';
            document.getElementById('submitBtn').disabled = true;

            try {
                const res = await fetch('/analyze', {method: 'POST', body: formData});
                const data = await res.json();

                if (data.success) {
                    const priceRes = await fetch('/get_price', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({product_info: data.produit})
                    });
                    const priceData = await priceRes.json();
                    
                    if (priceData.success) {
                        document.getElementById('suggestedPrice').textContent = 
                            `${priceData.prix.prix_recommande}€ (${priceData.prix.prix_min}€ - ${priceData.prix.prix_max}€)`;
                    }
                    
                    document.getElementById('productType').value = data.produit.type;
                    document.getElementById('brand').value = data.produit.marque !== 'À préciser' ? data.produit.marque : '';
                    document.getElementById('color').value = data.produit.couleur;
                    document.getElementById('size').value = data.produit.taille;
                    document.getElementById('condition').value = data.produit.etat;
                    
                    updateDesc();
                    editForm.style.display = 'block';
                } else {
                    alert('Erreur: ' + data.error);
                }
            } catch (error) {
                alert('Erreur: ' + error);
            } finally {
                loading.style.display = 'none';
                document.getElementById('submitBtn').disabled = false;
            }
        };

        function updateDesc() {
            const type = document.getElementById('productType').value;
            const marque = document.getElementById('brand').value || 'À préciser';
            const couleur = document.getElementById('color').value || 'multicolore';
            const etat = document.getElementById('condition').value;
            
            const templates = {
                'maillot': `${marque !== 'À préciser' ? marque + ' - ' : ''}Maillot ${couleur} authentique ! Excellent état. Pour les vrais fans ! ⚽ Envoi rapide 📦`,
                'pantalon': `${marque !== 'À préciser' ? marque + ' - ' : ''}Pantalon ${couleur}. ${etat}. Coupe parfaite ! 👖 Envoi rapide 📦`,
                't-shirt': `${marque !== 'À préciser' ? marque + ' - ' : ''}T-shirt ${couleur}. ${etat} ! 👕 Envoi rapide 📦`,
                'chaussures': `${marque !== 'À préciser' ? marque + ' - ' : ''}Chaussures ${couleur}. ${etat}. Confortables ! 👟 Envoi rapide 📦`
            };
            
            document.getElementById('descPreview').textContent = templates[type] || templates['t-shirt'];
        }

        async function generateFinal() {
            loading.style.display = 'block';
            
            const productInfo = {
                type: document.getElementById('productType').value,
                marque: document.getElementById('brand').value || 'À préciser',
                couleur: document.getElementById('color').value,
                taille: document.getElementById('size').value,
                etat: document.getElementById('condition').value,
                matiere: 'À préciser',
                details: 'Article de qualité'
            };
            
            try {
                const res = await fetch('/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({product_info: productInfo})
                });
                
                const data = await res.json();
                
                if (data.success) {
                    document.getElementById('titre').textContent = data.annonce.titre;
                    document.getElementById('prix').textContent = 
                        `${data.annonce.prix}€ (${data.annonce.prix_min}€ - ${data.annonce.prix_max}€)`;
                    document.getElementById('description').textContent = data.annonce.description;
                    
                    editForm.style.display = 'none';
                    result.style.display = 'block';
                }
            } catch (error) {
                alert('Erreur: ' + error);
            } finally {
                loading.style.display = 'none';
            }
        }

        function copy(id) {
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
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'Aucune image'})
        
        file = request.files['image']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        product_info = image_analyzer.analyze_product(filepath)
        os.remove(filepath)
        
        return jsonify({'success': True, 'produit': product_info})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_price', methods=['POST'])
def get_price():
    try:
        data = request.get_json()
        product_info = data['product_info']
        price_info = price_analyzer.calculate_optimal_price(product_info)
        return jsonify({'success': True, 'prix': price_info})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        product_info = data['product_info']
        price_info = price_analyzer.calculate_optimal_price(product_info)
        listing = desc_generator.create_full_listing(product_info, price_info)
        return jsonify({'success': True, 'annonce': listing})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
