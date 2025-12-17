"""
Bot Vinted Multilingue - Version finale
"""

from flask import Flask, request, jsonify, render_template_string
from werkzeug.utils import secure_filename
import os
from PIL import Image
from collections import Counter
import random

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ===== TRADUCTIONS =====
TRANSLATIONS = {
    'fr': {
        'types': {'T-shirt': 'T-shirt', 'Maillot': 'Maillot', 'Pull': 'Pull', 'Sweat': 'Sweat', 
                  'Pantalon': 'Pantalon', 'Chaussures': 'Chaussures', 'Sac': 'Sac'},
        'colors': {'noir': 'noir', 'blanc': 'blanc', 'gris': 'gris', 'rouge': 'rouge', 'bleu': 'bleu',
                   'vert': 'vert', 'marron': 'marron', 'beige': 'beige', 'or': 'or'},
        'conditions': {'Excellent état': 'Excellent état', 'Très bon état': 'Très bon état', 'Bon état': 'Bon état'},
        'desc': {
            'intro': ["{type} {color} en {condition}.", "Superbe {type} {color}, {condition}."],
            'brand': ["Marque : {brand}.", "{brand} authentique."],
            'details': ["Matière confortable.", "Qualité excellente.", "Peu porté."],
            'closing': ["Contactez-moi ! 📩", "Envoi rapide ! 📦"]
        }
    },
    'en': {
        'types': {'T-shirt': 'T-shirt', 'Maillot': 'Jersey', 'Pull': 'Sweater', 'Sweat': 'Hoodie',
                  'Pantalon': 'Pants', 'Chaussures': 'Shoes', 'Sac': 'Bag'},
        'colors': {'noir': 'black', 'blanc': 'white', 'gris': 'gray', 'rouge': 'red', 'bleu': 'blue',
                   'vert': 'green', 'marron': 'brown', 'beige': 'beige', 'or': 'gold'},
        'conditions': {'Excellent état': 'Excellent condition', 'Très bon état': 'Very good condition', 'Bon état': 'Good condition'},
        'desc': {
            'intro': ["{type} in {color}, {condition}.", "Beautiful {color} {type}."],
            'brand': ["Brand: {brand}.", "Authentic {brand}."],
            'details': ["Comfortable material.", "Excellent quality.", "Barely worn."],
            'closing': ["Contact me! 📩", "Fast shipping! 📦"]
        }
    },
    'es': {
        'types': {'T-shirt': 'Camiseta', 'Maillot': 'Camiseta de fútbol', 'Pull': 'Jersey', 'Sweat': 'Sudadera',
                  'Pantalon': 'Pantalón', 'Chaussures': 'Zapatos', 'Sac': 'Bolso'},
        'colors': {'noir': 'negro', 'blanc': 'blanco', 'gris': 'gris', 'rouge': 'rojo', 'bleu': 'azul',
                   'vert': 'verde', 'marron': 'marrón', 'beige': 'beige', 'or': 'dorado'},
        'conditions': {'Excellent état': 'Estado excelente', 'Très bon état': 'Muy buen estado', 'Bon état': 'Buen estado'},
        'desc': {
            'intro': ["{type} {color} en {condition}.", "Hermosa {type} {color}."],
            'brand': ["Marca: {brand}.", "{brand} auténtico."],
            'details': ["Material cómodo.", "Excelente calidad.", "Poco usado."],
            'closing': ["¡Contáctame! 📩", "¡Envío rápido! 📦"]
        }
    },
    'de': {
        'types': {'T-shirt': 'T-Shirt', 'Maillot': 'Trikot', 'Pull': 'Pullover', 'Sweat': 'Kapuzenpullover',
                  'Pantalon': 'Hose', 'Chaussures': 'Schuhe', 'Sac': 'Tasche'},
        'colors': {'noir': 'schwarz', 'blanc': 'weiß', 'gris': 'grau', 'rouge': 'rot', 'bleu': 'blau',
                   'vert': 'grün', 'marron': 'braun', 'beige': 'beige', 'or': 'gold'},
        'conditions': {'Excellent état': 'Ausgezeichneter Zustand', 'Très bon état': 'Sehr guter Zustand', 'Bon état': 'Guter Zustand'},
        'desc': {
            'intro': ["{type} in {color}, {condition}.", "Schönes {color} {type}."],
            'brand': ["Marke: {brand}.", "Authentisch {brand}."],
            'details': ["Bequemes Material.", "Ausgezeichnete Qualität.", "Kaum getragen."],
            'closing': ["Kontaktieren Sie mich! 📩", "Schneller Versand! 📦"]
        }
    }
}


# ===== ANALYSE D'IMAGES =====
def classify_color(r, g, b):
    if r < 50 and g < 50 and b < 50: return 'noir'
    if r > 220 and g > 220 and b > 220: return 'blanc'
    if abs(r - g) < 30 and abs(g - b) < 30 and 50 <= r <= 220: return 'gris'
    if r > g > b and r < 180 and g < 140: return 'marron'
    if r > 180 and g > 160 and b > 130 and r - b < 80: return 'beige'
    if r > 200 and g > 180 and b < 120: return 'or'
    if r > g + 50 and r > b + 50 and r > 100: return 'rouge'
    if b > r + 50 and b > g + 30 and b > 100: return 'bleu'
    if g > r + 40 and g > b + 40: return 'vert'
    return None

def extract_colors(img):
    img_small = img.resize((100, 100))
    pixels = list(img_small.getdata())
    colors = []
    for r, g, b in pixels[:1000]:
        color = classify_color(r, g, b)
        if color: colors.append(color)
    return colors

def detect_brand(colors, ratio):
    if 'blanc' in colors and 'or' in colors and colors.count('blanc') > 2 and 1.0 <= ratio <= 1.5:
        return 'Real Madrid'
    if 'bleu' in colors and 'rouge' in colors:
        if colors.count('bleu') + colors.count('rouge') >= 4 and 1.0 <= ratio <= 1.5:
            return 'Barcelona'
    return 'À préciser'

def detect_type(ratio, colors, marque):
    if ratio < 0.7: return 'Chaussures'
    if marque in ['Real Madrid', 'Barcelona', 'Psg']: return 'Maillot'
    
    cuir_colors = ['noir', 'marron', 'beige']
    sport_colors = ['rouge', 'bleu', 'vert', 'or']
    cuir_count = sum(colors.count(c) for c in cuir_colors if c in colors)
    sport_count = sum(colors.count(c) for c in sport_colors if c in colors)
    
    if cuir_count > sport_count * 2 and 0.9 <= ratio <= 1.3:
        if len([c for c in colors if c in sport_colors]) <= 1:
            return 'Sac'
    
    if 0.7 <= ratio < 0.95: return 'Pantalon'
    if ratio > 1.35: return 'Sweat'
    return 'T-shirt'

def analyze_images(image_paths):
    all_colors = []
    all_ratios = []
    
    for path in image_paths:
        try:
            img = Image.open(path)
            colors = extract_colors(img)
            all_colors.extend(colors)
            width, height = img.size
            ratio = height / width if width > 0 else 1.0
            all_ratios.append(ratio)
        except Exception as e:
            continue
    
    color_counts = Counter(all_colors)
    dominant_colors = [c for c, count in color_counts.most_common(3)]
    avg_ratio = sum(all_ratios) / len(all_ratios) if all_ratios else 1.0
    
    marque = detect_brand(dominant_colors, avg_ratio)
    type_produit = detect_type(avg_ratio, dominant_colors, marque)
    couleur = dominant_colors[0] if dominant_colors else 'noir'
    
    total = sum(color_counts.values())
    if total > 0 and color_counts.get('blanc', 0) / total > 0.3:
        etat = 'Excellent état'
    elif total > 0 and color_counts.get('noir', 0) / total > 0.4:
        etat = 'Très bon état'
    else:
        etat = 'Très bon état'
    
    return {'type': type_produit, 'marque': marque, 'couleur': couleur, 'etat': etat}


# ===== PRIX =====
def calculate_price(product_type, brand, condition):
    base = {'T-shirt': 8, 'Maillot': 25, 'Pull': 15, 'Sweat': 18, 'Pantalon': 15, 
            'Chaussures': 30, 'Sac': 20}.get(product_type, 15)
    brand_mult = {'Nike': 1.5, 'Adidas': 1.5, 'Real Madrid': 2.0, 'Barcelona': 2.0}.get(brand, 1.0)
    cond_mult = {'Excellent état': 1.1, 'Très bon état': 1.0, 'Bon état': 0.8}.get(condition, 1.0)
    price = base * brand_mult * cond_mult
    return max(5, int(round(price / 5) * 5))


# ===== DESCRIPTION =====
def generate_description(product_type, brand, color, condition, language):
    trans = TRANSLATIONS.get(language, TRANSLATIONS['fr'])
    type_trans = trans['types'].get(product_type, product_type)
    color_trans = trans['colors'].get(color, color)
    cond_trans = trans['conditions'].get(condition, condition)
    
    if brand and brand != 'À préciser':
        title = f"{type_trans} {brand} - {color_trans} - {cond_trans}"
    else:
        title = f"{type_trans} {color_trans} - {cond_trans}"
    
    desc_t = trans['desc']
    intro = random.choice(desc_t['intro']).format(type=type_trans.lower(), color=color_trans, condition=cond_trans.lower())
    brand_text = ""
    if brand and brand != 'À préciser':
        brand_text = " " + random.choice(desc_t['brand']).format(brand=brand)
    detail = random.choice(desc_t['details'])
    closing = random.choice(desc_t['closing'])
    
    description = f"{intro}{brand_text} {detail} {closing}"
    return title, description


# ===== HTML TEMPLATE =====
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vinted Bot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
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
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Vinted Bot</h1>
        <p class="subtitle" id="subtitle">Téléchargez vos photos !</p>
        
        <div class="lang-selector">
            <button class="lang-btn active" onclick="changeLang('fr')">🇫🇷</button>
            <button class="lang-btn" onclick="changeLang('en')">🇬🇧</button>
            <button class="lang-btn" onclick="changeLang('es')">🇪🇸</button>
            <button class="lang-btn" onclick="changeLang('de')">🇩🇪</button>
        </div>

        <div class="upload-zone" onclick="document.getElementById('fileInput').click()">
            <p style="font-size: 48px;">📸</p>
            <p id="uploadText">Cliquez ou glissez vos photos ici</p>
        </div>

        <input type="file" id="fileInput" multiple accept="image/*" onchange="handleFiles(this.files)">
        <div class="preview-container" id="previewContainer"></div>
        <button id="analyzeBtn" onclick="analyzeImages()" disabled>🚀 Analyser</button>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="color: #667eea;">Analyse en cours...</p>
        </div>

        <div class="result" id="result" style="display: none;">
            <h3>📋 Résultat</h3>
            <div id="resultContent"></div>
        </div>
    </div>

    <script>
        let selectedFiles = [];
        let currentLang = 'fr';

        function changeLang(lang) {
            currentLang = lang;
            document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
        }

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
                    div.innerHTML = `<img src="${e.target.result}"><button class="remove-btn" onclick="removeFile(${index})">×</button>`;
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
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            document.getElementById('analyzeBtn').disabled = true;

            const formData = new FormData();
            selectedFiles.forEach(file => formData.append('images', file));
            formData.append('language', currentLang);

            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                if (data.success) {
                    document.getElementById('resultContent').innerHTML = `
                        <div class="result-item"><strong>Type:</strong> ${data.type}</div>
                        <div class="result-item"><strong>Marque:</strong> ${data.marque}</div>
                        <div class="result-item"><strong>Couleur:</strong> ${data.couleur}</div>
                        <div class="result-item"><strong>État:</strong> ${data.etat}</div>
                        <div class="result-item"><strong>Prix:</strong> ${data.prix}€</div>
                        <div class="result-item"><strong>Titre:</strong> ${data.titre}</div>
                        <div class="result-item"><strong>Description:</strong><br>${data.description}</div>
                    `;
                    document.getElementById('result').style.display = 'block';
                }
            } catch (error) {
                alert('Erreur: ' + error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('analyzeBtn').disabled = false;
            }
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
            return jsonify({'success': False, 'error': 'Aucune image'}), 400

        files = request.files.getlist('images')
        language = request.form.get('language', 'fr')
        
        if not files or files[0].filename == '':
            return jsonify({'success': False, 'error': 'Aucune image sélectionnée'}), 400

        image_paths = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_paths.append(filepath)

        if not image_paths:
            return jsonify({'success': False, 'error': 'Format invalide'}), 400

        result = analyze_images(image_paths)
        prix = calculate_price(result['type'], result['marque'], result['etat'])
        titre, description = generate_description(
            result['type'], 
            result['marque'], 
            result['couleur'], 
            result['etat'],
            language
        )

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
