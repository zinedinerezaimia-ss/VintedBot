"""
Bot Vinted IA - Version finale avec modules
"""

from flask import Flask, request, jsonify, render_template_string
from werkzeug.utils import secure_filename
import os
import sys
from pathlib import Path

# Ajouter le dossier modules au path
sys.path.insert(0, str(Path(__file__).parent / "modules"))

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Import des modules
try:
    from modules import analyze_image, detect_brand, get_price_range, generate_listing, TRANSLATIONS
    MODULES_LOADED = True
    print("✅ Modules chargés avec succès !")
except ImportError as e:
    print(f"❌ Erreur import modules: {e}")
    MODULES_LOADED = False

@app.route('/')
def index():
    """Page d'accueil"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyse les photos uploadées"""
    if not MODULES_LOADED:
        return jsonify({"error": "Modules non chargés"}), 500
    
    try:
        files = request.files.getlist('photos')
        language = request.form.get('language', 'fr')
        
        if not files or not files[0].filename:
            return jsonify({"error": "Aucune photo"}), 400
        
        print(f"📸 Analyse de {len(files)} photos...")
        
        results = []
        for i, file in enumerate(files):
            if file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                print(f"  - Photo {i+1}/{len(files)}: {filename}")
                
                # Analyse de l'image
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
                
                # Nettoyer le fichier
                os.remove(filepath)
                print(f"    ✓ Détecté: {item_type}, couleurs: {colors}, prix: {price_min}-{price_max}€")
        
        # Prendre le premier résultat comme principal
        main = results[0] if results else {}
        
        # Générer titre et description (avec le prix)
        price_range = main.get('price', '')
        title, description = generate_listing(
            main.get('type', 't-shirt'),
            main.get('colors', ['noir']),
            main.get('condition', 'bon'),
            main.get('brand'),
            language,
            price_range  # On passe le prix
        )
        
        print(f"✅ Analyse terminée: {main.get('type')} {main.get('colors')}")
        
        return jsonify({
            'type': main.get('type'),
            'brand': main.get('brand'),
            'colors': main.get('colors'),
            'condition': main.get('condition'),
            'price': main.get('price'),
            'title': title,
            'description': description
        })
        
    except Exception as e:
        print(f"❌ Erreur analyse: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/generate_text', methods=['POST'])
def generate_text():
    """Régénère titre et description sans reanalyser les photos"""
    if not MODULES_LOADED:
        return jsonify({"error": "Modules non chargés"}), 500
    
    try:
        data = request.json
        item_type = data.get('type', 't-shirt')
        brand = data.get('brand') or None
        color = data.get('color', 'noir')
        condition = data.get('condition', 'bon')
        language = data.get('language', 'fr')
        
        # Recalculer le prix
        price_min, price_max = get_price_range(item_type, brand, condition)
        price_range = f"{price_min}€ - {price_max}€"
        
        title, description = generate_listing(
            item_type,
            [color],
            condition,
            brand,
            language,
            price_range  # On passe le prix
        )
        
        return jsonify({
            'title': title,
            'description': description,
            'price': price_range
        })
        
    except Exception as e:
        print(f"❌ Erreur génération: {e}")
        return jsonify({"error": str(e)}), 500

# ===== HTML TEMPLATE =====
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
            font-family: 'Segoe UI', sans-serif;
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
        .language-selector {
            margin-bottom: 20px;
        }
        .language-selector label {
            display: block;
            font-weight: bold;
            margin-bottom: 5px;
            color: #333;
        }
        .language-selector select {
            width: 100%;
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
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
            background: #f8f9ff;
        }
        .upload-zone:hover {
            background: #f0f0ff;
            border-color: #764ba2;
            transform: scale(1.02);
        }
        .upload-zone.dragover {
            background: #e8e9ff;
            border-color: #764ba2;
            transform: scale(1.05);
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
        .results {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9ff;
            border-radius: 15px;
            display: none;
        }
        .results.show {
            display: block;
            animation: slideIn 0.3s ease;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
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
            min-height: 150px;
            resize: vertical;
            font-family: inherit;
        }
        .price-badge {
            display: inline-block;
            background: #4ade80;
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 16px;
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
            <select id="language">
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

        <input type="file" id="fileInput" multiple accept="image/*" style="display: none;">

        <div class="photos-preview" id="photosPreview"></div>

        <button class="btn btn-primary" id="analyzeBtn" disabled>
            🔍 Analyser
        </button>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="margin-top: 10px; color: #667eea; font-weight: bold;">Analyse en cours...</p>
        </div>

        <div class="results" id="results">
            <h3 style="margin-bottom: 15px; color: #667eea;">✨ Résultats</h3>
            
            <div class="field">
                <label>💰 Prix suggéré:</label>
                <span class="price-badge" id="priceResult">-</span>
            </div>

            <div class="field">
                <label>Type détecté:</label>
                <select id="typeInput">
                    <option value="pull">Pull</option>
                    <option value="t-shirt">T-shirt</option>
                    <option value="sweat">Sweat</option>
                    <option value="pantalon">Pantalon</option>
                    <option value="jean">Jean</option>
                    <option value="veste">Veste</option>
                    <option value="chaussures">Chaussures</option>
                    <option value="sac">Sac</option>
                    <option value="maillot">Maillot</option>
                </select>
            </div>

            <div class="field">
                <label>Marque (si détectée):</label>
                <input type="text" id="brandInput" placeholder="Nike, Adidas...">
            </div>

            <div class="field">
                <label>Couleur:</label>
                <select id="colorInput">
                    <option value="noir">Noir</option>
                    <option value="blanc">Blanc</option>
                    <option value="gris">Gris</option>
                    <option value="bleu">Bleu</option>
                    <option value="rouge">Rouge</option>
                    <option value="vert">Vert</option>
                    <option value="marron">Marron</option>
                    <option value="beige">Beige</option>
                </select>
            </div>

            <div class="field">
                <label>État:</label>
                <select id="conditionInput">
                    <option value="neuf">Neuf avec étiquette</option>
                    <option value="très bon">Très bon état</option>
                    <option value="bon">Bon état</option>
                    <option value="satisfaisant">Satisfaisant</option>
                </select>
            </div>

            <div class="field">
                <label>📝 Titre généré:</label>
                <input type="text" id="titleResult" readonly style="background: white; font-weight: bold;">
            </div>

            <div class="field">
                <label>📄 Description générée:</label>
                <textarea id="descriptionResult" readonly style="background: white;"></textarea>
            </div>

            <button class="btn btn-primary" id="copyBtn">
                📋 Copier tout
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

        // Click sur zone
        uploadZone.addEventListener('click', (e) => {
            e.preventDefault();
            fileInput.click();
        });

        // Drag & Drop
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
            if (e.dataTransfer.files.length > 0) {
                handleFiles(e.dataTransfer.files);
            }
        });

        // Sélection de fichiers
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFiles(e.target.files);
            }
        });

        function handleFiles(files) {
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

        // Analyser
        analyzeBtn.addEventListener('click', async () => {
            loading.classList.add('show');
            results.classList.remove('show');
            analyzeBtn.disabled = true;

            const formData = new FormData();
            selectedFiles.forEach(file => formData.append('photos', file));
            formData.append('language', document.getElementById('language').value);

            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Erreur serveur');
                }

                const data = await response.json();
                
                // Remplir les champs
                document.getElementById('priceResult').textContent = data.price;
                document.getElementById('typeInput').value = data.type;
                document.getElementById('brandInput').value = data.brand || '';
                document.getElementById('colorInput').value = data.colors[0] || 'noir';
                document.getElementById('conditionInput').value = data.condition;
                document.getElementById('titleResult').value = data.title;
                document.getElementById('descriptionResult').value = data.description;
                
                loading.classList.remove('show');
                results.classList.add('show');
                analyzeBtn.disabled = false;
                
            } catch (error) {
                alert('❌ Erreur: ' + error.message);
                loading.classList.remove('show');
                analyzeBtn.disabled = false;
            }
        });

        // Régénérer quand on modifie les champs
        ['typeInput', 'brandInput', 'colorInput', 'conditionInput'].forEach(id => {
            document.getElementById(id).addEventListener('change', regenerateDescription);
        });

        async function regenerateDescription() {
            const type = document.getElementById('typeInput').value;
            const brand = document.getElementById('brandInput').value;
            const color = document.getElementById('colorInput').value;
            const condition = document.getElementById('conditionInput').value;
            const language = document.getElementById('language').value;

            // Régénérer localement (sans renvoyer les photos)
            try {
                const response = await fetch('/generate_text', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ type, brand, color, condition, language })
                });

                if (response.ok) {
                    const data = await response.json();
                    document.getElementById('titleResult').value = data.title;
                    document.getElementById('descriptionResult').value = data.description;
                    if (data.price) {
                        document.getElementById('priceResult').textContent = data.price;
                    }
                }
            } catch (error) {
                console.error('Erreur régénération:', error);
            }
        }

        // Copier
        document.getElementById('copyBtn').addEventListener('click', () => {
            const title = document.getElementById('titleResult').value;
            const description = document.getElementById('descriptionResult').value;
            const text = `${title}

${description}`;
            
            navigator.clipboard.writeText(text).then(() => {
                alert('✅ Copié dans le presse-papier !');
            }).catch(() => {
                alert('📋 Impossible de copier automatiquement. Copiez manuellement.');
            });
        });
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
