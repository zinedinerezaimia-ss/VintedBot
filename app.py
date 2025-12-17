"""
Bot Vinted Multilingue - Version originale
"""

from flask import Flask, request, jsonify, render_template_string
from werkzeug.utils import secure_filename
import os
import sys
from pathlib import Path

# Ajouter modules au path
sys.path.insert(0, str(Path(__file__).parent / "modules"))

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Import des modules
try:
    from image_analyzer import analyze_image, detect_brand
    from price_analyzer import get_price_range
    from description_generator import generate_listing
    from translations import TRANSLATIONS
    MODULES_LOADED = True
except ImportError:
    print("⚠️ Modules introuvables, utilise fallback basique")
    MODULES_LOADED = False

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    if not MODULES_LOADED:
        return jsonify({"error": "Modules non chargés"}), 500
    
    files = request.files.getlist('photos')
    language = request.form.get('language', 'fr')
    
    if not files:
        return jsonify({"error": "Aucune photo"}), 400
    
    results = []
    for file in files:
        if file.filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(filepath)
            
            # Analyse
            item_type, colors, condition = analyze_image(filepath)
            brand = detect_brand(filepath)
            price_min, price_max = get_price_range(item_type, brand, condition)
            
            results.append({
                'type': item_type,
                'colors': colors,
                'condition': condition,
                'brand': brand,
                'price': f"{price_min}€ - {price_max}€"
            })
            
            os.remove(filepath)
    
    # Prend le premier résultat comme principal
    main = results[0] if results else {}
    title, description = generate_listing(
        main.get('type', 'vêtement'),
        main.get('colors', ['noir']),
        main.get('condition', 'bon'),
        main.get('brand'),
        language
    )
    
    return jsonify({
        'type': main.get('type'),
        'brand': main.get('brand'),
        'colors': main.get('colors'),
        'condition': main.get('condition'),
        'price': main.get('price'),
        'title': title,
        'description': description
    })

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
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #667eea;
            font-size: 32px;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #666;
            font-size: 14px;
        }
        .upload-zone {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 20px;
        }
        .upload-zone:hover {
            background: #f8f9ff;
            border-color: #764ba2;
        }
        .upload-zone.dragover {
            background: #f0f0ff;
            border-color: #764ba2;
        }
        .photos-preview {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
            gap: 10px;
            margin: 20px 0;
        }
        .photo-item {
            position: relative;
            aspect-ratio: 1;
            border-radius: 10px;
            overflow: hidden;
            border: 2px solid #eee;
        }
        .photo-item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .photo-item.main::before {
            content: 'PRINCIPALE';
            position: absolute;
            top: 5px;
            left: 5px;
            background: #667eea;
            color: white;
            padding: 3px 8px;
            border-radius: 5px;
            font-size: 10px;
            font-weight: bold;
            z-index: 1;
        }
        .btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            margin: 10px 0;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-primary:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .results {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9ff;
            border-radius: 15px;
            display: none;
        }
        .results.show {
            display: block;
        }
        .field {
            margin-bottom: 15px;
        }
        .field label {
            display: block;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
            font-size: 14px;
        }
        .field input, .field select, .field textarea {
            width: 100%;
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: border 0.3s;
        }
        .field input:focus, .field select:focus, .field textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        .field textarea {
            min-height: 100px;
            resize: vertical;
        }
        .price-badge {
            display: inline-block;
            background: #4ade80;
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
        }
        .language-selector {
            margin-bottom: 20px;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .loading.show {
            display: block;
        }
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Bot Vinted IA</h1>
            <p class="subtitle">Multi-photos • Analyse • Prix • Description</p>
        </div>

        <div class="language-selector">
            <label>🌍 Langue:</label>
            <select id="language" class="field">
                <option value="fr">🇫🇷 Français</option>
                <option value="en">🇬🇧 English</option>
                <option value="es">🇪🇸 Español</option>
                <option value="de">🇩🇪 Deutsch</option>
            </select>
        </div>

        <div class="upload-zone" id="uploadZone">
            <p style="font-size: 48px; margin-bottom: 10px;">📸</p>
            <p style="font-size: 18px; font-weight: bold; margin-bottom: 5px;">Déposez vos photos ici</p>
            <p style="color: #999; font-size: 13px;">Jusqu'à 8 photos • Toutes seront analysées</p>
        </div>

        <input type="file" id="fileInput" multiple accept="image/*" style="display: none;" tabindex="-1">

        <div class="photos-preview" id="photosPreview"></div>

        <button class="btn btn-primary" id="analyzeBtn" disabled>
            🔍 Analyser
        </button>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="margin-top: 10px; color: #667eea; font-weight: bold;">Analyse en cours...</p>
        </div>

        <div class="results" id="results">
            <h3 style="margin-bottom: 15px; color: #667eea;">✏️ Vérifiez les infos</h3>
            
            <div class="field">
                <label>💰 Prix suggéré:</label>
                <span class="price-badge" id="priceResult">-</span>
            </div>

            <div class="field">
                <label>Type *</label>
                <select id="typeInput">
                    <option value="pull">Pull</option>
                    <option value="t-shirt">T-shirt</option>
                    <option value="pantalon">Pantalon</option>
                    <option value="veste">Veste</option>
                    <option value="robe">Robe</option>
                    <option value="jupe">Jupe</option>
                    <option value="short">Short</option>
                    <option value="sweat">Sweat</option>
                    <option value="chemise">Chemise</option>
                    <option value="manteau">Manteau</option>
                    <option value="chaussures">Chaussures</option>
                    <option value="sac">Sac</option>
                    <option value="accessoire">Accessoire</option>
                </select>
            </div>

            <div class="field">
                <label>Marque</label>
                <input type="text" id="brandInput" placeholder="Nike, Adidas...">
            </div>

            <div class="field">
                <label>Couleur *</label>
                <select id="colorInput">
                    <option value="noir">Noir</option>
                    <option value="blanc">Blanc</option>
                    <option value="gris">Gris</option>
                    <option value="bleu">Bleu</option>
                    <option value="rouge">Rouge</option>
                    <option value="vert">Vert</option>
                    <option value="jaune">Jaune</option>
                    <option value="rose">Rose</option>
                    <option value="violet">Violet</option>
                    <option value="marron">Marron</option>
                    <option value="beige">Beige</option>
                    <option value="orange">Orange</option>
                    <option value="multicolore">Multicolore</option>
                </select>
            </div>

            <div class="field">
                <label>Taille</label>
                <select id="sizeInput">
                    <option value="">À préciser</option>
                    <option value="XS">XS</option>
                    <option value="S">S</option>
                    <option value="M">M</option>
                    <option value="L">L</option>
                    <option value="XL">XL</option>
                    <option value="XXL">XXL</option>
                </select>
            </div>

            <div class="field">
                <label>État *</label>
                <select id="conditionInput">
                    <option value="neuf">Neuf avec étiquette</option>
                    <option value="très bon">Très bon état</option>
                    <option value="bon">Bon état</option>
                    <option value="satisfaisant">Satisfaisant</option>
                </select>
            </div>

            <div class="field">
                <label>📝 Aperçu:</label>
                <p id="preview" style="background: white; padding: 15px; border-radius: 8px; color: #666; font-style: italic;">
                    -
                </p>
            </div>

            <button class="btn btn-primary" id="generateBtn">
                ✨ Générer
            </button>
        </div>
    </div>

    <script>
        const uploadZone = document.getElementById('uploadZone');
        const fileInput = document.getElementById('fileInput');
        const photosPreview = document.getElementById('photosPreview');
        const analyzeBtn = document.getElementById('analyzeBtn');
        const loading = document.getElementById('loading');
        const results = document.getElementById('results');
        let selectedFiles = [];

        uploadZone.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            fileInput.click();
            console.log('Zone cliquée, ouverture du sélecteur...');
        });

        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.classList.add('dragover');
        });

        uploadZone.addEventListener('dragleave', () => {
            uploadZone.classList.remove('dragover');
        });

        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.classList.remove('dragover');
            handleFiles(e.dataTransfer.files);
        });

        fileInput.addEventListener('change', (e) => {
            console.log('Fichiers sélectionnés:', e.target.files.length);
            if (e.target.files.length > 0) {
                handleFiles(e.target.files);
            }
        });

        function handleFiles(files) {
            if (!files || files.length === 0) return;
            
            selectedFiles = Array.from(files).slice(0, 8);
            photosPreview.innerHTML = '';
            
            selectedFiles.forEach((file, index) => {
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        const div = document.createElement('div');
                        div.className = 'photo-item' + (index === 0 ? ' main' : '');
                        div.innerHTML = `<img src="${e.target.result}" alt="Photo ${index + 1}">`;
                        photosPreview.appendChild(div);
                    };
                    reader.readAsDataURL(file);
                }
            });

            analyzeBtn.disabled = selectedFiles.length === 0;
        }

        analyzeBtn.addEventListener('click', async () => {
            loading.classList.add('show');
            results.classList.remove('show');

            const formData = new FormData();
            selectedFiles.forEach(file => formData.append('photos', file));
            formData.append('language', document.getElementById('language').value);

            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                
                document.getElementById('priceResult').textContent = data.price;
                document.getElementById('typeInput').value = data.type;
                document.getElementById('brandInput').value = data.brand || '';
                document.getElementById('colorInput').value = data.colors[0] || 'noir';
                document.getElementById('conditionInput').value = data.condition;
                
                updatePreview(data.title, data.description);
                
                loading.classList.remove('show');
                results.classList.add('show');
            } catch (error) {
                alert('Erreur: ' + error.message);
                loading.classList.remove('show');
            }
        });

        function updatePreview(title, description) {
            const preview = document.getElementById('preview');
            preview.innerHTML = `<strong>${title}</strong><br><br>${description}`;
        }

        document.getElementById('generateBtn').addEventListener('click', () => {
            const preview = document.getElementById('preview').innerText;
            alert('📋 Copié !\n\n' + preview);
        });
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
