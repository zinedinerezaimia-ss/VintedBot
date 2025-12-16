"""
Bot Vinted Multilingue - Version finale stable
"""

from flask import Flask, request, jsonify, render_template_string
from werkzeug.utils import secure_filename
import os
import sys
from pathlib import Path

# Ajouter modules au path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from modules.image_analyzer import ImageAnalyzer
    from modules.price_analyzer import PriceAnalyzer
    from modules.description_generator import DescriptionGenerator
    from modules.translations import get_translation
except ImportError:
    print("⚠️ Modules introuvables, utilise fallback basique")
    ImageAnalyzer = None
    PriceAnalyzer = None
    DescriptionGenerator = None
    def get_translation(lang): return {}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'

# Créer le dossier uploads
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vinted Bot - Auto-Listing</title>
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
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .lang-selector {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 30px;
        }
        .lang-btn {
            padding: 10px 20px;
            border: 2px solid #667eea;
            background: white;
            color: #667eea;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
        }
        .lang-btn.active {
            background: #667eea;
            color: white;
        }
        .lang-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
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
            background: #e8ebff;
            border-color: #764ba2;
        }
        input[type="file"] { display: none; }
        .preview-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .preview-item {
            position: relative;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        .preview-item img {
            width: 100%;
            height: 150px;
            object-fit: cover;
        }
        .remove-btn {
            position: absolute;
            top: 5px;
            right: 5px;
            background: #ff4757;
            color: white;
            border: none;
            border-radius: 50%;
            width: 25px;
            height: 25px;
            cursor: pointer;
            font-weight: bold;
        }
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.3s;
        }
        button:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }
        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .result {
            margin-top: 30px;
            padding: 25px;
            background: #f8f9ff;
            border-radius: 15px;
            border-left: 5px solid #667eea;
        }
        .result h3 {
            color: #667eea;
            margin-bottom: 15px;
        }
        .result-item {
            margin: 10px 0;
            padding: 10px;
            background: white;
            border-radius: 8px;
        }
        .result-item strong {
            color: #764ba2;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
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
        .error {
            background: #ff4757;
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Vinted Bot</h1>
        <p class="subtitle" id="subtitle">Téléchargez vos photos, le bot s'occupe du reste !</p>
        
        <div class="lang-selector">
            <button class="lang-btn active" data-lang="fr" onclick="changeLang('fr')">🇫🇷 Français</button>
            <button class="lang-btn" data-lang="en" onclick="changeLang('en')">🇬🇧 English</button>
            <button class="lang-btn" data-lang="es" onclick="changeLang('es')">🇪🇸 Español</button>
            <button class="lang-btn" data-lang="de" onclick="changeLang('de')">🇩🇪 Deutsch</button>
        </div>

        <div class="upload-zone" id="uploadZone" onclick="document.getElementById('fileInput').click()">
            <p style="font-size: 48px; margin-bottom: 10px;">📸</p>
            <p style="font-size: 18px; color: #667eea; font-weight: bold;" id="uploadText">
                Cliquez ou glissez vos photos ici
            </p>
            <p style="color: #999; margin-top: 10px;" id="uploadSubtext">
                Plusieurs photos acceptées (PNG, JPG, JPEG, WEBP)
            </p>
        </div>

        <input type="file" id="fileInput" multiple accept="image/*" onchange="handleFiles(this.files)">

        <div class="preview-container" id="previewContainer"></div>

        <button id="analyzeBtn" onclick="analyzeImages()" disabled>
            <span id="btnText">🚀 Analyser et créer l'annonce</span>
        </button>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="margin-top: 15px; color: #667eea;" id="loadingText">Analyse en cours...</p>
        </div>

        <div class="error" id="error"></div>

        <div class="result" id="result" style="display: none;">
            <h3 id="resultTitle">📋 Résultat de l'analyse</h3>
            <div id="resultContent"></div>
        </div>
    </div>

    <script>
        let selectedFiles = [];
        let currentLang = 'fr';

        const translations = {
            fr: {
                subtitle: "Téléchargez vos photos, le bot s'occupe du reste !",
                uploadText: "Cliquez ou glissez vos photos ici",
                uploadSubtext: "Plusieurs photos acceptées (PNG, JPG, JPEG, WEBP)",
                btnText: "🚀 Analyser et créer l'annonce",
                loadingText: "Analyse en cours...",
                resultTitle: "📋 Résultat de l'analyse",
                type: "Type",
                brand: "Marque",
                color: "Couleur",
                condition: "État",
                price: "Prix suggéré",
                title: "Titre",
                description: "Description"
            },
            en: {
                subtitle: "Upload your photos, the bot takes care of the rest!",
                uploadText: "Click or drag your photos here",
                uploadSubtext: "Multiple photos accepted (PNG, JPG, JPEG, WEBP)",
                btnText: "🚀 Analyze and create listing",
                loadingText: "Analyzing...",
                resultTitle: "📋 Analysis Result",
                type: "Type",
                brand: "Brand",
                color: "Color",
                condition: "Condition",
                price: "Suggested Price",
                title: "Title",
                description: "Description"
            },
            es: {
                subtitle: "¡Sube tus fotos, el bot se encarga del resto!",
                uploadText: "Haz clic o arrastra tus fotos aquí",
                uploadSubtext: "Varias fotos aceptadas (PNG, JPG, JPEG, WEBP)",
                btnText: "🚀 Analizar y crear anuncio",
                loadingText: "Analizando...",
                resultTitle: "📋 Resultado del análisis",
                type: "Tipo",
                brand: "Marca",
                color: "Color",
                condition: "Estado",
                price: "Precio sugerido",
                title: "Título",
                description: "Descripción"
            },
            de: {
                subtitle: "Laden Sie Ihre Fotos hoch, der Bot kümmert sich um den Rest!",
                uploadText: "Klicken oder ziehen Sie Ihre Fotos hierher",
                uploadSubtext: "Mehrere Fotos akzeptiert (PNG, JPG, JPEG, WEBP)",
                btnText: "🚀 Analysieren und Anzeige erstellen",
                loadingText: "Analysiere...",
                resultTitle: "📋 Analyseergebnis",
                type: "Typ",
                brand: "Marke",
                color: "Farbe",
                condition: "Zustand",
                price: "Vorgeschlagener Preis",
                title: "Titel",
                description: "Beschreibung"
            }
        };

        function changeLang(lang) {
            currentLang = lang;
            document.querySelectorAll('.lang-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            document.querySelector(`[data-lang="${lang}"]`).classList.add('active');
            
            const t = translations[lang];
            document.getElementById('subtitle').textContent = t.subtitle;
            document.getElementById('uploadText').textContent = t.uploadText;
            document.getElementById('uploadSubtext').textContent = t.uploadSubtext;
            document.getElementById('btnText').textContent = t.btnText;
            document.getElementById('loadingText').textContent = t.loadingText;
            document.getElementById('resultTitle').textContent = t.resultTitle;
        }

        const uploadZone = document.getElementById('uploadZone');

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

        function handleFiles(files) {
            selectedFiles = Array.from(files);
            displayPreviews();
            document.getElementById('analyzeBtn').disabled = selectedFiles.length === 0;
        }

        function displayPreviews() {
            const container = document.getElementById('previewContainer');
            container.innerHTML = '';

            selectedFiles.forEach((file, index) => {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const div = document.createElement('div');
                    div.className = 'preview-item';
                    div.innerHTML = `
                        <img src="${e.target.result}" alt="Preview ${index + 1}">
                        <button class="remove-btn" onclick="removeFile(${index})">×</button>
                    `;
                    container.appendChild(div);
                };
                reader.readAsDataURL(file);
            });
        }

        function removeFile(index) {
            selectedFiles.splice(index, 1);
            displayPreviews();
            document.getElementById('analyzeBtn').disabled = selectedFiles.length === 0;
        }

        async function analyzeImages() {
            if (selectedFiles.length === 0) return;

            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            document.getElementById('error').style.display = 'none';
            document.getElementById('analyzeBtn').disabled = true;

            const formData = new FormData();
            selectedFiles.forEach(file => {
                formData.append('images', file);
            });
            formData.append('language', currentLang);

            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    displayResult(data);
                } else {
                    showError(data.error || 'Erreur inconnue');
                }
            } catch (error) {
                showError('Erreur de connexion: ' + error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('analyzeBtn').disabled = false;
            }
        }

        function displayResult(data) {
            const t = translations[currentLang];
            const content = document.getElementById('resultContent');
            content.innerHTML = `
                <div class="result-item"><strong>${t.type}:</strong> ${data.type}</div>
                <div class="result-item"><strong>${t.brand}:</strong> ${data.marque}</div>
                <div class="result-item"><strong>${t.color}:</strong> ${data.couleur}</div>
                <div class="result-item"><strong>${t.condition}:</strong> ${data.etat}</div>
                <div class="result-item"><strong>${t.price}:</strong> ${data.prix}€</div>
                <div class="result-item"><strong>${t.title}:</strong> ${data.titre}</div>
                <div class="result-item" style="white-space: pre-wrap;"><strong>${t.description}:</strong><br>${data.description}</div>
            `;
            document.getElementById('result').style.display = 'block';
        }

        function showError(message) {
            const errorDiv = document.getElementById('error');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
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
        if 'images' not in request.files:
            return jsonify({'success': False, 'error': 'Aucune image fournie'}), 400

        files = request.files.getlist('images')
        language = request.form.get('language', 'fr')
        
        if not files or files[0].filename == '':
            return jsonify({'success': False, 'error': 'Aucune image sélectionnée'}), 400

        # Sauvegarder et analyser les images
        image_paths = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_paths.append(filepath)

        if not image_paths:
            return jsonify({'success': False, 'error': 'Format d\'image invalide'}), 400

        # Analyse
        analyzer = ImageAnalyzer()
        price_analyzer = PriceAnalyzer()
        desc_generator = DescriptionGenerator()

        result = analyzer.analyze_images(image_paths)
        prix = price_analyzer.calculate_price(result['type'], result['marque'], result['etat'])
        titre, description = desc_generator.generate(
            result['type'], 
            result['marque'], 
            result['couleur'], 
            result['etat'],
            language
        )

        # Nettoyer les fichiers temporaires
        for path in image_paths:
            try:
                os.remove(path)
            except:
                pass

        return jsonify({
            'success': True,
            'type': result['type'],
            'marque': result['marque'],
            'couleur': result['couleur'],
            'etat': result['etat'],
            'prix': prix,
            'titre': titre,
            'description': description
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
