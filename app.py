from flask import Flask, request, render_template_string, jsonify
import base64
from io import BytesIO
from PIL import Image
import json
import os

app = Flask(__name__)

# Traductions
TRANSLATIONS = {
    'fr': {
        'title': 'Bot Vinted IA - Automatisation Annonces',
        'subtitle': 'Uploadez vos photos, le bot analyse et crée l\'annonce automatiquement',
        'language': 'Langue',
        'upload_btn': 'Choisir photos (max 5)',
        'analyze_btn': 'Analyser & Créer l\'annonce',
        'results_title': 'Résultats de l\'analyse',
        'product_type': 'Type de produit',
        'brand': 'Marque',
        'color': 'Couleur',
        'condition': 'État',
        'price': 'Prix suggéré',
        'title_label': 'Titre de l\'annonce',
        'description': 'Description',
        'analyzing': 'Analyse en cours...',
        'error': 'Erreur',
        'select_photos': 'Sélectionnez au moins une photo'
    },
    'en': {
        'title': 'Vinted AI Bot - Listing Automation',
        'subtitle': 'Upload your photos, the bot analyzes and creates the listing automatically',
        'language': 'Language',
        'upload_btn': 'Choose photos (max 5)',
        'analyze_btn': 'Analyze & Create listing',
        'results_title': 'Analysis Results',
        'product_type': 'Product type',
        'brand': 'Brand',
        'color': 'Color',
        'condition': 'Condition',
        'price': 'Suggested price',
        'title_label': 'Listing title',
        'description': 'Description',
        'analyzing': 'Analyzing...',
        'error': 'Error',
        'select_photos': 'Select at least one photo'
    },
    'es': {
        'title': 'Bot Vinted IA - Automatización de Anuncios',
        'subtitle': 'Sube tus fotos, el bot analiza y crea el anuncio automáticamente',
        'language': 'Idioma',
        'upload_btn': 'Elegir fotos (máx 5)',
        'analyze_btn': 'Analizar y Crear anuncio',
        'results_title': 'Resultados del análisis',
        'product_type': 'Tipo de producto',
        'brand': 'Marca',
        'color': 'Color',
        'condition': 'Estado',
        'price': 'Precio sugerido',
        'title_label': 'Título del anuncio',
        'description': 'Descripción',
        'analyzing': 'Analizando...',
        'error': 'Error',
        'select_photos': 'Selecciona al menos una foto'
    },
    'de': {
        'title': 'Vinted KI-Bot - Anzeigen-Automatisierung',
        'subtitle': 'Laden Sie Ihre Fotos hoch, der Bot analysiert und erstellt die Anzeige automatisch',
        'language': 'Sprache',
        'upload_btn': 'Fotos auswählen (max 5)',
        'analyze_btn': 'Analysieren & Anzeige erstellen',
        'results_title': 'Analyseergebnisse',
        'product_type': 'Produkttyp',
        'brand': 'Marke',
        'color': 'Farbe',
        'condition': 'Zustand',
        'price': 'Vorgeschlagener Preis',
        'title_label': 'Anzeigentitel',
        'description': 'Beschreibung',
        'analyzing': 'Analysieren...',
        'error': 'Fehler',
        'select_photos': 'Wählen Sie mindestens ein Foto'
    }
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="{{lang}}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{t.title}}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
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
            color: #2d3748;
            font-size: 2em;
            margin-bottom: 10px;
            text-align: center;
        }
        .subtitle {
            color: #718096;
            text-align: center;
            margin-bottom: 30px;
            font-size: 0.95em;
        }
        .language-selector {
            text-align: center;
            margin-bottom: 30px;
        }
        .language-selector select {
            padding: 10px 20px;
            font-size: 1em;
            border: 2px solid #667eea;
            border-radius: 8px;
            background: white;
            cursor: pointer;
            outline: none;
        }
        .upload-zone {
            border: 3px dashed #cbd5e0;
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            background: #f7fafc;
            margin-bottom: 20px;
            transition: all 0.3s;
        }
        .upload-zone:hover {
            border-color: #667eea;
            background: #edf2f7;
        }
        input[type="file"] {
            display: none;
        }
        .upload-label {
            display: inline-block;
            padding: 15px 30px;
            background: #667eea;
            color: white;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
        }
        .upload-label:hover {
            background: #5a67d8;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
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
        .analyze-btn {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.1em;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 20px;
        }
        .analyze-btn:hover:not(:disabled) {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.5);
        }
        .analyze-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .results {
            margin-top: 40px;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 15px;
            display: none;
        }
        .results.show {
            display: block;
            animation: slideIn 0.5s ease;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .result-item {
            margin-bottom: 20px;
        }
        .result-label {
            font-weight: 700;
            color: #4a5568;
            margin-bottom: 8px;
            font-size: 0.9em;
            text-transform: uppercase;
        }
        .result-value {
            padding: 15px;
            background: white;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            font-size: 1.05em;
            color: #2d3748;
        }
        .loading {
            text-align: center;
            padding: 40px;
            display: none;
        }
        .loading.show {
            display: block;
        }
        .spinner {
            border: 4px solid #f3f4f6;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .error {
            background: #fed7d7;
            color: #c53030;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            display: none;
        }
        .error.show {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 {{t.title}}</h1>
        <p class="subtitle">{{t.subtitle}}</p>
        
        <div class="language-selector">
            <label for="language">{{t.language}}: </label>
            <select id="language" onchange="changeLanguage()">
                <option value="fr" {{'selected' if lang == 'fr' else ''}}>🇫🇷 Français</option>
                <option value="en" {{'selected' if lang == 'en' else ''}}>🇬🇧 English</option>
                <option value="es" {{'selected' if lang == 'es' else ''}}>🇪🇸 Español</option>
                <option value="de" {{'selected' if lang == 'de' else ''}}>🇩🇪 Deutsch</option>
            </select>
        </div>

        <div class="upload-zone">
            <label for="photos" class="upload-label">
                📸 {{t.upload_btn}}
            </label>
            <input type="file" id="photos" accept="image/*" multiple onchange="previewImages()">
        </div>

        <div class="preview-container" id="preview"></div>

        <button class="analyze-btn" onclick="analyzePhotos()" id="analyzeBtn" disabled>
            {{t.analyze_btn}}
        </button>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>{{t.analyzing}}</p>
        </div>

        <div class="error" id="error"></div>

        <div class="results" id="results">
            <h2>{{t.results_title}}</h2>
            <div class="result-item">
                <div class="result-label">{{t.product_type}}</div>
                <div class="result-value" id="type"></div>
            </div>
            <div class="result-item">
                <div class="result-label">{{t.brand}}</div>
                <div class="result-value" id="brand"></div>
            </div>
            <div class="result-item">
                <div class="result-label">{{t.color}}</div>
                <div class="result-value" id="color"></div>
            </div>
            <div class="result-item">
                <div class="result-label">{{t.condition}}</div>
                <div class="result-value" id="condition"></div>
            </div>
            <div class="result-item">
                <div class="result-label">{{t.price}}</div>
                <div class="result-value" id="price"></div>
            </div>
            <div class="result-item">
                <div class="result-label">{{t.title_label}}</div>
                <div class="result-value" id="listingTitle"></div>
            </div>
            <div class="result-item">
                <div class="result-label">{{t.description}}</div>
                <div class="result-value" id="description"></div>
            </div>
        </div>
    </div>

    <script>
        let selectedFiles = [];
        const currentLang = '{{lang}}';

        function changeLanguage() {
            const lang = document.getElementById('language').value;
            window.location.href = '/?lang=' + lang;
        }

        function previewImages() {
            const files = document.getElementById('photos').files;
            const preview = document.getElementById('preview');
            const analyzeBtn = document.getElementById('analyzeBtn');
            
            selectedFiles = Array.from(files).slice(0, 5);
            preview.innerHTML = '';
            
            if (selectedFiles.length > 0) {
                analyzeBtn.disabled = false;
                selectedFiles.forEach((file, index) => {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        const div = document.createElement('div');
                        div.className = 'preview-item';
                        div.innerHTML = `<img src="${e.target.result}" alt="Photo ${index + 1}">`;
                        preview.appendChild(div);
                    };
                    reader.readAsDataURL(file);
                });
            } else {
                analyzeBtn.disabled = true;
            }
        }

        async function analyzePhotos() {
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            const error = document.getElementById('error');
            const analyzeBtn = document.getElementById('analyzeBtn');
            
            if (selectedFiles.length === 0) {
                error.textContent = '{{t.select_photos}}';
                error.classList.add('show');
                return;
            }

            loading.classList.add('show');
            results.classList.remove('show');
            error.classList.remove('show');
            analyzeBtn.disabled = true;

            const formData = new FormData();
            selectedFiles.forEach(file => formData.append('photos', file));
            formData.append('language', currentLang);

            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.error) {
                    error.textContent = data.error;
                    error.classList.add('show');
                } else {
                    document.getElementById('type').textContent = data.type;
                    document.getElementById('brand').textContent = data.brand;
                    document.getElementById('color').textContent = data.color;
                    document.getElementById('condition').textContent = data.condition;
                    document.getElementById('price').textContent = data.price;
                    document.getElementById('listingTitle').textContent = data.title;
                    document.getElementById('description').textContent = data.description;
                    results.classList.add('show');
                }
            } catch (err) {
                error.textContent = '{{t.error}}: ' + err.message;
                error.classList.add('show');
            } finally {
                loading.classList.remove('show');
                analyzeBtn.disabled = false;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    lang = request.args.get('lang', 'fr')
    if lang not in TRANSLATIONS:
        lang = 'fr'
    return render_template_string(HTML_TEMPLATE, t=TRANSLATIONS[lang], lang=lang)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        files = request.files.getlist('photos')
        language = request.form.get('language', 'fr')
        
        if not files or len(files) == 0:
            return jsonify({'error': 'Aucune photo fournie'}), 400

        # Convertir images en base64
        images_base64 = []
        for file in files[:5]:
            img = Image.open(file.stream)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            images_base64.append(img_base64)

        # Appel à l'API Claude pour analyse
        result = analyze_with_claude(images_base64, language)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def analyze_with_claude(images_base64, language):
    """Analyse les images avec l'API Claude"""
    import requests
    
    # Prompts selon la langue
    prompts = {
        'fr': """Analyse ces photos de vêtement/accessoire pour Vinted.

Réponds UNIQUEMENT en JSON avec cette structure exacte:
{
    "type": "type exact (t-shirt, pantalon, robe, sac, chaussures, maillot, pull, etc.)",
    "brand": "marque détectée ou 'Non identifié'",
    "color": "couleur principale",
    "condition": "état estimé (Neuf, Très bon état, Bon état, Satisfaisant)",
    "price": "prix suggéré en € (juste le nombre)",
    "title": "titre accrocheur pour l'annonce",
    "description": "description détaillée et attractive"
}

Sois PRÉCIS: détecte le vrai type de produit, la vraie couleur, et les vraies marques visibles.""",
        'en': """Analyze these clothing/accessory photos for Vinted.

Respond ONLY in JSON with this exact structure:
{
    "type": "exact type (t-shirt, pants, dress, bag, shoes, jersey, sweater, etc.)",
    "brand": "detected brand or 'Unidentified'",
    "color": "main color",
    "condition": "estimated condition (New, Very good, Good, Fair)",
    "price": "suggested price in € (just the number)",
    "title": "catchy listing title",
    "description": "detailed and attractive description"
}

Be PRECISE: detect the real product type, real color, and real visible brands.""",
        'es': """Analiza estas fotos de ropa/accesorio para Vinted.

Responde SOLO en JSON con esta estructura exacta:
{
    "type": "tipo exacto (camiseta, pantalón, vestido, bolso, zapatos, camiseta, jersey, etc.)",
    "brand": "marca detectada o 'No identificado'",
    "color": "color principal",
    "condition": "estado estimado (Nuevo, Muy buen estado, Buen estado, Aceptable)",
    "price": "precio sugerido en € (solo el número)",
    "title": "título atractivo para el anuncio",
    "description": "descripción detallada y atractiva"
}

Sé PRECISO: detecta el tipo real de producto, el color real y las marcas reales visibles.""",
        'de': """Analysiere diese Kleidungs-/Accessoire-Fotos für Vinted.

Antworte NUR in JSON mit dieser exakten Struktur:
{
    "type": "genauer Typ (T-Shirt, Hose, Kleid, Tasche, Schuhe, Trikot, Pullover, usw.)",
    "brand": "erkannte Marke oder 'Nicht identifiziert'",
    "color": "Hauptfarbe",
    "condition": "geschätzter Zustand (Neu, Sehr gut, Gut, Akzeptabel)",
    "price": "vorgeschlagener Preis in € (nur die Zahl)",
    "title": "ansprechender Anzeigentitel",
    "description": "detaillierte und attraktive Beschreibung"
}

Sei PRÄZISE: erkenne den echten Produkttyp, die echte Farbe und die echten sichtbaren Marken."""
    }
    
    # Construction du contenu avec les images
    content = [{"type": "text", "text": prompts.get(language, prompts['fr'])}]
    
    for img_base64 in images_base64:
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": img_base64
            }
        })
    
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1024,
                "messages": [{
                    "role": "user",
                    "content": content
                }]
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            text_content = data['content'][0]['text']
            
            # Extraire le JSON de la réponse
            if '```json' in text_content:
                text_content = text_content.split('```json')[1].split('```')[0].strip()
            elif '```' in text_content:
                text_content = text_content.split('```')[1].split('```')[0].strip()
            
            result = json.loads(text_content)
            result['price'] = f"{result['price']}€"
            return result
        else:
            # Fallback en cas d'erreur API
            return get_fallback_analysis(language)
            
    except Exception as e:
        print(f"Erreur API Claude: {e}")
        return get_fallback_analysis(language)

def get_fallback_analysis(language):
    """Analyse de secours si l'API échoue"""
    fallbacks = {
        'fr': {
            'type': 'Vêtement',
            'brand': 'À préciser',
            'color': 'À préciser',
            'condition': 'Bon état',
            'price': '15€',
            'title': 'Article à vendre',
            'description': 'Article en bon état. Plus de détails à venir.'
        },
        'en': {
            'type': 'Clothing',
            'brand': 'To be specified',
            'color': 'To be specified',
            'condition': 'Good condition',
            'price': '15€',
            'title': 'Item for sale',
            'description': 'Item in good condition. More details coming soon.'
        },
        'es': {
            'type': 'Ropa',
            'brand': 'Por especificar',
            'color': 'Por especificar',
            'condition': 'Buen estado',
            'price': '15€',
            'title': 'Artículo en venta',
            'description': 'Artículo en buen estado. Más detalles próximamente.'
        },
        'de': {
            'type': 'Kleidung',
            'brand': 'Anzugeben',
            'color': 'Anzugeben',
            'condition': 'Guter Zustand',
            'price': '15€',
            'title': 'Artikel zu verkaufen',
            'description': 'Artikel in gutem Zustand. Weitere Details folgen.'
        }
    }
    return fallbacks.get(language, fallbacks['fr'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
