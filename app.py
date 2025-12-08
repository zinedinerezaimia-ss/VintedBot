"""
Interface Web améliorée avec correction manuelle
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
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #667eea;
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
                <h2>📸 Déposez vos photos ici</h2>
                <p>Jusqu'à 8 photos (comme Vinted)</p>
                <input type="file" id="fileInput" name="images" accept="image/*" multiple required>
            </div>
            
            <div id="previewContainer" style="display: none; margin: 20px 0;">
                <h3 style="margin-bottom: 10px;">Photos sélectionnées :</h3>
                <div id="previewGrid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 10px;"></div>
            </div>
            
            <button type="submit" class="btn" id="submitBtn">🔍 Analyser mon produit</button>
        </form>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Analyse en cours...</p>
        </div>
        
        <div class="edit-form" id="editForm">
            <h2>✏️ Vérifiez et corrigez les informations</h2>
            
            <div class="info-box price-box" style="margin-bottom: 20px;">
                <strong>💰 Prix suggéré :</strong>
                <p id="suggestedPrice"></p>
            </div>
            
            <div class="form-group">
                <label>Type de produit *</label>
                <select id="productType" onchange="updateDescription()">
                    <option value="t-shirt">T-shirt</option>
                    <option value="maillot">Maillot</option>
                    <option value="pull">Pull</option>
                    <option value="sweat">Sweat</option>
                    <option value="pantalon">Pantalon</option>
                    <option value="jean">Jean</option>
                    <option value="short">Short</option>
                    <option value="robe">Robe</option>
                    <option value="jupe">Jupe</option>
                    <option value="veste">Veste</option>
                    <option value="manteau">Manteau</option>
                    <option value="chaussures">Chaussures</option>
                    <option value="basket">Basket</option>
                    <option value="accessoire">Accessoire</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Marque</label>
                <input type="text" id="brand" placeholder="Nike, Adidas, Zara..." oninput="updateDescription()">
            </div>
            
            <div class="form-group">
                <label>Couleur principale *</label>
                <input type="text" id="color" placeholder="blanc, noir, rouge..." required oninput="updateDescription()">
            </div>
            
            <div class="form-group">
                <label>Taille</label>
                <select id="size" onchange="updateDescription()">
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
                <select id="condition" onchange="updateDescription()">
                    <option value="Neuf">Neuf avec étiquette</option>
                    <option value="Très bon">Très bon état</option>
                    <option value="Bon" selected>Bon état</option>
                    <option value="Satisfaisant">État satisfaisant</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Détails / Description courte</label>
                <input type="text" id="details" placeholder="Ex: Logo OM, motif fleuri..." oninput="updateDescription()">
            </div>
            
            <div class="info-box" style="background: #fff3cd; border-left-color: #ffc107; margin-top: 20px;">
                <strong>📄 Aperçu description :</strong>
                <p id="descriptionPreview" style="margin-top: 10px; font-style: italic;">La description se mettra à jour automatiquement...</p>
            </div>
            
            <button type="button" class="btn" onclick="generateListing()">✨ Générer l'annonce finale</button>
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
            
            <button class="btn" onclick="location.reload()">🔄 Nouvelle annonce</button>
        </div>
        
        <div class="footer">
            <p>Créé avec ❤️ • 100% Gratuit et Open Source</p>
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
        let selectedFiles = [];

        dropZone.onclick = () => fileInput.click();
        dropZone.ondragover = (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        };
        dropZone.ondragleave = () => dropZone.classList.remove('dragover');
        dropZone.ondrop = (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            fileInput.files = e.dataTransfer.files;
            showPreviews();
        };

        fileInput.onchange = showPreviews;
        
        function showPreviews() {
            const files = Array.from(fileInput.files).slice(0, 8); // Max 8 photos
            selectedFiles = files;
            
            if (files.length > 0) {
                previewGrid.innerHTML = '';
                previewContainer.style.display = 'block';
                
                files.forEach((file, index) => {
                    const img = document.createElement('img');
                    img.src = URL.createObjectURL(file);
                    img.style.width = '100%';
                    img.style.height = '120px';
                    img.style.objectFit = 'cover';
                    img.style.borderRadius = '10px';
                    img.style.border = index === 0 ? '3px solid #667eea' : '2px solid #ddd';
                    img.title = index === 0 ? 'Photo principale' : `Photo ${index + 1}`;
                    previewGrid.appendChild(img);
                });
            }
        }

        form.onsubmit = async (e) => {
            e.preventDefault();
            
            const formData = new FormData(form);
            
            loading.style.display = 'block';
            editForm.style.display = 'none';
            result.style.display = 'none';
            document.getElementById('submitBtn').disabled = true;

            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    // Afficher le prix suggéré
                    const priceInfo = await fetch('/get_price', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({product_info: data.produit})
                    }).then(r => r.json());
                    
                    if (priceInfo.success) {
                        document.getElementById('suggestedPrice').textContent = 
                            `${priceInfo.prix.prix_recommande}€ (Fourchette: ${priceInfo.prix.prix_min}€ - ${priceInfo.prix.prix_max}€)`;
                    }
                    
                    // Pré-remplir le formulaire
                    document.getElementById('productType').value = data.produit.type;
                    document.getElementById('brand').value = data.produit.marque !== 'À préciser' ? data.produit.marque : '';
                    document.getElementById('color').value = data.produit.couleur;
                    document.getElementById('size').value = data.produit.taille;
                    document.getElementById('condition').value = data.produit.etat;
                    document.getElementById('details').value = data.produit.details;
                    
                    editForm.style.display = 'block';
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

        async function updateDescription() {
            // Récupérer les valeurs actuelles
            const productInfo = {
                type: document.getElementById('productType').value,
                marque: document.getElementById('brand').value || 'À préciser',
                couleur: document.getElementById('color').value || 'multicolore',
                taille: document.getElementById('size').value,
                etat: document.getElementById('condition').value,
                details: document.getElementById('details').value || 'Article de qualité'
            };
            
            // Générer la description en temps réel (côté client, rapide)
            const desc = generateQuickDescription(productInfo);
            document.getElementById('descriptionPreview').textContent = desc;
        }
        
        function generateQuickDescription(info) {
            const marqueText = info.marque !== 'À préciser' ? `${info.marque} - ` : '';
            
            const etatMap = {
                'Neuf': 'Neuf avec étiquette',
                'Très bon': 'Excellent état',
                'Bon': 'Très bon état',
                'Satisfaisant': 'Bon état'
            };
            const etatText = etatMap[info.etat] || 'Bon état';
            
            // Templates simples par type
            const templates = {
                'maillot': `${marqueText}Maillot ${info.couleur} authentique ! ${etatText}. Pour les vrais fans ! ⚽ Envoi rapide 📦`,
                'pantalon': `${marqueText}Pantalon ${info.couleur} classique. ${etatText}, coupe parfaite ! 👖 Envoi rapide 📦`,
                'jean': `${marqueText}Jean ${info.couleur}. ${etatText}, très confortable ! 👖 Envoi rapide 📦`,
                't-shirt': `${marqueText}T-shirt ${info.couleur}. ${etatText}, parfait basique ! 👕 Envoi rapide 📦`,
                'pull': `${marqueText}Pull ${info.couleur} tout doux. ${etatText} ! 🧶 Envoi rapide 📦`,
                'sweat': `${marqueText}Sweat ${info.couleur} confortable. ${etatText} ! 👔 Envoi rapide 📦`
            };
            
            return templates[info.type] || `${marqueText}${info.type.charAt(0).toUpperCase() + info.type.slice(1)} ${info.couleur}. ${etatText} ! Envoi rapide 📦`;
        }

        async function generateListing() {
            loading.style.display = 'block';
            
            const productInfo = {
                type: document.getElementById('productType').value,
                marque: document.getElementById('brand').value || 'À préciser',
                couleur: document.getElementById('color').value,
                taille: document.getElementById('size').value,
                etat: document.getElementById('condition').value,
                matiere: 'À préciser',
                details: document.getElementById('details').value || 'Article de qualité'
            };
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({product_info: productInfo})
                });
                
                const data = await response.json();
                
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
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyse initiale de l'image"""
    try:
        print("=" * 50)
        print("🔥 DEBUT ANALYSE")
        
        if 'image' not in request.files:
            print("❌ Aucune image dans request.files")
            return jsonify({'success': False, 'error': 'Aucune image fournie'})
        
        file = request.files['image']
        if file.filename == '':
            print("❌ Filename vide")
            return jsonify({'success': False, 'error': 'Aucun fichier sélectionné'})
        
        print(f"✅ Fichier reçu: {file.filename}")
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        print(f"✅ Fichier sauvegardé: {filepath}")
        print("🚀 Appel de l'analyseur...")
        
        # Analyser l'image
        product_info = image_analyzer.analyze_product(filepath)
        
        print(f"✅ Résultat analyse: {product_info}")
        
        # Supprimer le fichier temporaire
        os.remove(filepath)
        print("✅ Fichier temporaire supprimé")
        
        print("=" * 50)
        
        return jsonify({
            'success': True,
            'produit': product_info
        })
        
    except Exception as e:
        print(f"❌❌❌ ERREUR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/generate', methods=['POST'])
def generate():
    """Génère l'annonce finale"""
    try:
        data = request.get_json()
        product_info = data['product_info']
        
        # Analyser les prix
        price_info = price_analyzer.calculate_optimal_price(product_info)
        
        # Générer l'annonce
        listing = desc_generator.create_full_listing(product_info, price_info)
        
        return jsonify({
            'success': True,
            'annonce': listing
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_price', methods=['POST'])
def get_price():
    """Calcule le prix suggéré"""
    try:
        data = request.get_json()
        product_info = data['product_info']
        
        # Analyser les prix
        price_info = price_analyzer.calculate_optimal_price(product_info)
        
        return jsonify({
            'success': True,
            'prix': price_info
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
