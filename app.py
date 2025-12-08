"""
Interface Web Bot Vinted - Multi-photos
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
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB total
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
    <title>Bot Vinted IA</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 900px;
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
        .preview-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin: 20px 0;
        }
        .preview-item {
            position: relative;
            aspect-ratio: 1;
            border-radius: 10px;
            overflow: hidden;
            border: 3px solid #ddd;
        }
        .preview-item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .preview-item.main {
            border-color: #667eea;
            box-shadow: 0 0 15px rgba(102, 126, 234, 0.5);
        }
        .preview-label {
            position: absolute;
            top: 5px;
            left: 5px;
            background: #667eea;
            color: white;
            padding: 3px 8px;
            border-radius: 5px;
            font-size: 12px;
            font-weight: bold;
        }
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
        .result {
            display: none;
            margin-top: 30px;
            padding: 30px;
            background: #f8f9ff;
            border-radius: 15px;
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
        <p class="subtitle">Multi-photos • Analyse • Prix • Description</p>
        
        <form id="uploadForm" enctype="multipart/form-data">
            <div class="upload-zone" id="dropZone">
                <h2>📸 Déposez vos photos ici</h2>
                <p>Jusqu'à 8 photos • La 1ère sera analysée</p>
                <input type="file" id="fileInput" name="images" accept="image/*" multiple required>
            </div>
            
            <div id="previewContainer" style="display:none;">
                <h3 style="margin: 20px 0 10px 0;">📷 Vos photos :</h3>
                <div class="preview-grid" id="previewGrid"></div>
            </div>
            
            <button type="submit" class="btn" id="submitBtn">🔍 Analyser</button>
        </form>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Analyse en cours...</p>
        </div>
        
        <div class="edit-form" id="editForm">
            <h2>✏️ Vérifiez les infos</h2>
            
            <div class="info-box price-box" style="margin-bottom:20px;">
                <strong>💰 Prix suggéré :</strong>
                <p id="suggestedPrice"></p>
            </div>
            
            <div class="form-group">
                <label>Type *</label>
                <select id="productType" onchange="updateDesc()">
                    <option value="t-shirt">T-shirt</option>
                    <option value="maillot">Maillot</option>
                    <option value="pull">Pull</option>
                    <option value="sweat">Sweat</option>
                    <option value="pantalon">Pantalon</option>
                    <option value="jean">Jean</option>
                    <option value="short">Short</option>
                    <option value="robe">Robe</option>
                    <option value="veste">Veste</option>
                    <option value="chaussures">Chaussures</option>
                    <option value="basket">Basket</option>
                    <option value="bottine">Bottine</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Marque</label>
                <input type="text" id="brand" placeholder="Nike, Adidas, Zara..." oninput="updateDesc()">
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
                    <option value="XXL">XXL</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>État *</label>
                <select id="condition" onchange="updateDesc()">
                    <option value="Neuf">Neuf avec étiquette</option>
                    <option value="Très bon">Très bon état</option>
                    <option value="Bon" selected>Bon état</option>
                    <option value="Satisfaisant">Satisfaisant</option>
                </select>
            </div>
            
            <div class="info-box" style="background:#fff3cd;">
                <strong>📄 Aperçu description :</strong>
                <p id="descPreview" style="margin-top:10px;font-style:italic;"></p>
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
                <strong>💰 Prix recommandé :</strong>
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
        const previewContainer = document.getElementById('previewContainer');
        const previewGrid = document.getElementById('previewGrid');
        const form = document.getElementById('uploadForm');
        const loading = document.getElementById('loading');
        const editForm = document.getElementById('editForm');
        const result = document.getElementById('result');

        dropZone.onclick = () => fileInput.click();
        
        dropZone.ondragover = (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        };
        
        dropZone.ondragleave = () => dropZone.classList.remove('dragover');
        
        dropZone.ondrop = (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            
            const dt = new DataTransfer();
            Array.from(e.dataTransfer.files).slice(0, 8).forEach(file => dt.items.add(file));
            fileInput.files = dt.files;
            
            showPreviews();
        };

        fileInput.onchange = showPreviews;
        
        function showPreviews() {
            const files = Array.from(fileInput.files).slice(0, 8);
            
            if (files.length === 0) return;
            
            previewGrid.innerHTML = '';
            previewContainer.style.display = 'block';
            
            files.forEach((file, index) => {
                const div = document.createElement('div');
                div.className = 'preview-item' + (index === 0 ? ' main' : '');
                
                const img = document.createElement('img');
                img.src = URL.createObjectURL(file);
                
                const label = document.createElement('div');
                label.className = 'preview-label';
                label.textContent = index === 0 ? 'PRINCIPALE' : `Photo ${index + 1}`;
                
                div.appendChild(img);
                div.appendChild(label);
                previewGrid.appendChild(div);
            });
        }

        form.onsubmit = async (e) => {
            e.preventDefault();
            
            const formData = new FormData();
            Array.from(fileInput.files).forEach(file => {
                formData.append('images', file);
            });
            
            loading.style.display = 'block';
            editForm.style.display = 'none';
            result.style.display = 'none';
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
                            `${priceData.prix.prix_recommande}€ (Fourchette: ${priceData.prix.prix_min}€ - ${priceData.prix.prix_max}€)`;
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
            const marque = document.getElementById('brand').value || '';
            const couleur = document.getElementById('color').value || 'coloré';
            const etat = document.getElementById('condition').value;
            
            const marqueText = marque ? marque + ' - ' : '';
            const etatMap = {
                'Neuf': 'Neuf avec étiquette',
                'Très bon': 'Excellent état',
                'Bon': 'Très bon état',
                'Satisfaisant': 'Bon état'
            };
            
            const templates = {
                'maillot': `${marqueText}Maillot ${couleur} authentique ! ${etatMap[etat]}. Pour les vrais fans ! ⚽ Envoi rapide 📦`,
                'pantalon': `${marqueText}Pantalon ${couleur}. ${etatMap[etat]}. Coupe parfaite ! 👖 Envoi rapide 📦`,
                't-shirt': `${marqueText}T-shirt ${couleur}. ${etatMap[etat]} ! 👕 Envoi rapide 📦`,
                'pull': `${marqueText}Pull ${couleur} tout doux. ${etatMap[etat]} ! 🧶 Envoi rapide 📦`,
                'chaussures': `${marqueText}Chaussures ${couleur}. ${etatMap[etat]}. Très confortables ! 👟 Envoi rapide 📦`,
                'basket': `${marqueText}Basket ${couleur} stylée ! ${etatMap[etat]} ! 👟 Envoi rapide 📦`,
                'bottine': `${marqueText}Bottines ${couleur}. ${etatMap[etat]} ! 👢 Envoi rapide 📦`
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
                        `${data.annonce.prix}€ (Fourchette: ${data.annonce.prix_min}€ - ${data.annonce.prix_max}€)`;
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

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        files = request.files.getlist('images')
        
        if not files or len(files) == 0:
            return jsonify({'success': False, 'error': 'Aucune image'})
        
        print(f"🔥 {len(files)} photo(s) reçue(s)")
        
        # Sauvegarder TOUTES les photos temporairement
        image_paths = []
        for i, file in enumerate(files[:8]):  # Max 8 photos
            filename = secure_filename(f"temp_{i}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_paths.append(filepath)
        
        # Analyser TOUTES les photos ensemble
        product_info = image_analyzer.analyze_multiple_products(image_paths)
        
        # Supprimer les fichiers temporaires
        for path in image_paths:
            try:
                os.remove(path)
            except:
                pass
        
        return jsonify({
            'success': True,
            'produit': product_info,
            'nb_photos': len(files)
        })
        
    except Exception as e:
        print(f"❌ ERREUR: {str(e)}")
        import traceback
        traceback.print_exc()
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

