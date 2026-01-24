from flask import Flask, request, send_file, render_template_string, redirect, url_for
import qrcode
from io import BytesIO
from PIL import Image

app = Flask(__name__)

HTML_MAIN = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Code API Service</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 900px;
            width: 100%;
            margin: 0 auto;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            text-align: center;
            font-size: 28px;
        }
        .subtitle {
            color: #666;
            text-align: center;
            margin-bottom: 40px;
            font-size: 14px;
        }
        .type-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .type-card {
            background: #f8f9fa;
            border: 3px solid #e0e0e0;
            border-radius: 15px;
            padding: 25px 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            color: #333;
        }
        .type-card:hover {
            border-color: #667eea;
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
            background: white;
        }
        .type-icon {
            font-size: 50px;
            margin-bottom: 12px;
        }
        .type-name {
            font-size: 15px;
            font-weight: 600;
            color: #333;
        }
        .api-section {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            margin-top: 30px;
        }
        .api-section h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 22px;
        }
        .code-block {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            overflow-x: auto;
            margin: 15px 0;
        }
        .param { color: #f92672; }
        .string { color: #a6e22e; }
        @media (max-width: 768px) {
            .container { padding: 20px; }
            h1 { font-size: 24px; }
            .type-grid { grid-template-columns: repeat(2, 1fr); gap: 15px; }
            .type-icon { font-size: 40px; }
            .type-name { font-size: 13px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔲 QR Code Generator</h1>
        <p class="subtitle">Выберите тип QR-кода</p>
        
        <div class="type-grid">
            <a href="/generate?type=url" class="type-card">
                <div class="type-icon">🔗</div>
                <div class="type-name">URL / Текст</div>
            </a>
            <a href="/generate?type=telegram" class="type-card">
                <div class="type-icon">✈️</div>
                <div class="type-name">Telegram</div>
            </a>
            <a href="/generate?type=whatsapp" class="type-card">
                <div class="type-icon">💬</div>
                <div class="type-name">WhatsApp</div>
            </a>
            <a href="/generate?type=instagram" class="type-card">
                <div class="type-icon">📷</div>
                <div class="type-name">Instagram</div>
            </a>
            <a href="/generate?type=facebook" class="type-card">
                <div class="type-icon">👥</div>
                <div class="type-name">Facebook</div>
            </a>
            <a href="/generate?type=tiktok" class="type-card">
                <div class="type-icon">🎵</div>
                <div class="type-name">TikTok</div>
            </a>
            <a href="/generate?type=twitter" class="type-card">
                <div class="type-icon">🐦</div>
                <div class="type-name">Twitter (X)</div>
            </a>
            <a href="/generate?type=linkedin" class="type-card">
                <div class="type-icon">💼</div>
                <div class="type-name">LinkedIn</div>
            </a>
            <a href="/generate?type=youtube" class="type-card">
                <div class="type-icon">📺</div>
                <div class="type-name">YouTube</div>
            </a>
            <a href="/generate?type=email" class="type-card">
                <div class="type-icon">📧</div>
                <div class="type-name">Email</div>
            </a>
            <a href="/generate?type=phone" class="type-card">
                <div class="type-icon">📞</div>
                <div class="type-name">Телефон</div>
            </a>
        </div>

        <div class="api-section">
            <h2>📖 API Документация</h2>
            <p style="color: #555; margin-bottom: 15px;">
                Используйте GET-запрос для генерации QR-кодов:
            </p>
            <div class="code-block">
GET /qr?<span class="param">data</span>=<span class="string">https://example.com</span>&<span class="param">color</span>=<span class="string">000000</span>&<span class="param">bgcolor</span>=<span class="string">ffffff</span>&<span class="param">size</span>=<span class="string">256</span>
            </div>
            <p style="color: #555; margin-top: 20px;"><strong>Параметры:</strong></p>
            <ul style="margin-left: 20px; margin-top: 10px; color: #555; line-height: 1.8;">
                <li><code>data</code> - данные для кодирования (обязательный)</li>
                <li><code>color</code> - цвет QR в HEX без # (по умолчанию: 000000)</li>
                <li><code>bgcolor</code> - цвет фона в HEX без # (по умолчанию: ffffff)</li>
                <li><code>size</code> - размер в пикселях (по умолчанию: 256)</li>
                <li><code>quietzone</code> - отступы вокруг QR (по умолчанию: 4)</li>
            </ul>
            <p style="color: #555; margin-top: 20px;"><strong>Эндпоинты:</strong></p>
            <ul style="margin-left: 20px; margin-top: 10px; color: #555; line-height: 1.8;">
                <li><code>/qr</code> - получить PNG изображение</li>
                <li><code>/view</code> - посмотреть QR на странице</li>
                <li><code>/download</code> - скачать QR-код</li>
            </ul>
        </div>
    </div>
</body>
</html>
'''

HTML_GENERATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Создать QR - {{ type_name }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 700px;
            width: 100%;
            margin: 0 auto;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            text-align: center;
            font-size: 26px;
        }
        .subtitle {
            color: #666;
            text-align: center;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .form-section {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            color: #333;
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 14px;
        }
        input, textarea, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
            font-family: inherit;
        }
        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        textarea {
            resize: vertical;
            min-height: 100px;
        }
        small {
            color: #666;
            font-size: 12px;
            display: block;
            margin-top: 5px;
        }
        .color-group {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        input[type="color"] {
            height: 50px;
            cursor: pointer;
        }
        .btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        .btn-secondary {
            background: #6c757d;
            margin-top: 10px;
        }
        .preview {
            background: white;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            min-height: 200px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px dashed #e0e0e0;
            margin-top: 20px;
        }
        .preview img {
            max-width: 100%;
            height: auto;
        }
        .btn-group {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 15px;
        }
        .btn-action {
            padding: 12px;
            background: #28a745;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            text-align: center;
            transition: all 0.2s;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ type_icon }} {{ type_name }}</h1>
        <p class="subtitle">Заполните данные для QR-кода</p>
        <div class="form-section">
            <div class="form-group">
                <label>{{ input_label }}</label>
                {% if type == 'url' %}
                <textarea id="dataInput" placeholder="{{ placeholder }}"></textarea>
                {% else %}
                <input type="text" id="dataInput" placeholder="{{ placeholder }}">
                {% endif %}
                <small>{{ helper_text }}</small>
            </div>
            <div class="color-group">
                <div class="form-group">
                    <label>Цвет QR</label>
                    <input type="color" id="qrColor" value="#000000">
                </div>
                <div class="form-group">
                    <label>Цвет фона</label>
                    <input type="color" id="bgColor" value="#ffffff">
                </div>
            </div>
            <div class="color-group">
                <div class="form-group">
                    <label>Размер</label>
                    <select id="qrSize">
                        <option value="256" selected>256x256</option>
                        <option value="512">512x512</option>
                        <option value="1024">1024x1024</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Отступы</label>
                    <select id="quietZone">
                        <option value="4" selected>Средние</option>
                        <option value="2">Маленькие</option>
                        <option value="6">Большие</option>
                    </select>
                </div>
            </div>
            <button class="btn" onclick="generateQR()">Создать QR-код</button>
            <a href="/" class="btn btn-secondary" style="display: block; text-align: center; text-decoration: none;">← Назад</a>
            <div class="preview" id="preview">
                <p style="color: #999;">QR-код появится здесь</p>
            </div>
            <div id="buttonGroup" style="display: none;" class="btn-group">
                <a class="btn-action" id="viewBtn" href="#" target="_blank">👁️ Посмотреть</a>
                <a class="btn-action" id="downloadBtn" href="#" download="qrcode.png">⬇️ Скачать</a>
            </div>
        </div>
    </div>
    <script>
        const qrType = "{{ type }}";
        function buildData() {
            const input = document.getElementById('dataInput').value.trim();
            if (!input) return null;
            switch(qrType) {
                case 'url': return input;
                case 'telegram': return "https://t.me/" + input.replace('@', '');
                case 'whatsapp': return "https://wa.me/" + input.replace(/[^0-9+]/g, '');
                case 'instagram': return "https://instagram.com/" + input.replace('@', '');
                case 'facebook': return "https://facebook.com/" + input;
                case 'tiktok': return "https://tiktok.com/@" + input.replace('@', '');
                case 'twitter': return "https://twitter.com/" + input.replace('@', '');
                case 'linkedin': return "https://linkedin.com/in/" + input;
                case 'youtube': return input.startsWith('@') ? "https://youtube.com/" + input : "https://youtube.com/channel/" + input;
                case 'email': return "mailto:" + input;
                case 'phone': return "tel:" + input;
                default: return input;
            }
        }
        function generateQR() {
            const data = buildData();
            if (!data) { alert('Пожалуйста, заполните поле'); return; }
            const color = document.getElementById('qrColor').value.replace('#', '');
            const bgcolor = document.getElementById('bgColor').value.replace('#', '');
            const size = document.getElementById('qrSize').value;
            const quietzone = document.getElementById('quietZone').value;
            const params = "data=" + encodeURIComponent(data) + "&color=" + color + "&bgcolor=" + bgcolor + "&size=" + size + "&quietzone=" + quietzone;
            const qrUrl = "/qr?" + params;
            const viewUrl = "/view?" + params;
            const downloadUrl = "/download?" + params;
            document.getElementById('preview').innerHTML = '<img src="' + qrUrl + '" alt="QR Code">';
            document.getElementById('buttonGroup').style.display = 'grid';
            document.getElementById('viewBtn').href = viewUrl;
            document.getElementById('downloadBtn').href = downloadUrl;
        }
        document.getElementById('dataInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && qrType !== 'url') { e.preventDefault(); generateQR(); }
        });
    </script>
</body>
</html>
'''

VIEW_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Просмотр QR-кода</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 600px;
            width: 100%;
            text-align: center;
        }
        h1 { color: #333; margin-bottom: 30px; }
        .qr-display {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .qr-display img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
        }
        .info {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: left;
        }
        .info p { color: #555; margin: 8px 0; word-break: break-all; }
        .info strong { color: #333; }
        .btn {
            display: inline-block;
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            margin: 5px;
            transition: transform 0.2s;
        }
        .btn-secondary { background: #28a745; }
        .btn-back { background: #6c757d; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔲 Ваш QR-код</h1>
        <div class="qr-display">
            <img src="{{ qr_url }}" alt="QR Code">
        </div>
        <div class="info">
            <p><strong>Данные:</strong> {{ data }}</p>
            <p><strong>Размер:</strong> {{ size }}x{{ size }} пикселей</p>
            <p><strong>Цвет:</strong> #{{ color }}</p>
            <p><strong>Фон:</strong> #{{ bgcolor }}</p>
        </div>
        <a href="{{ download_url }}" class="btn btn-secondary" download="qrcode.png">⬇️ Скачать QR-код</a>
        <a href="/" class="btn btn-back">← Создать новый</a>
    </div>
</body>
</html>
'''

QR_TYPES = {
    'url': {'name': 'URL / Текст', 'icon': '🔗', 'label': 'URL или текст', 'placeholder': 'https://example.com', 'helper': 'Введите любой URL или текст'},
    'telegram': {'name': 'Telegram', 'icon': '✈️', 'label': 'Username', 'placeholder': 'username', 'helper': 'Введите username без @'},
    'whatsapp': {'name': 'WhatsApp', 'icon': '💬', 'label': 'Номер телефона', 'placeholder': '+79991234567', 'helper': 'С кодом страны'},
    'instagram': {'name': 'Instagram', 'icon': '📷', 'label': 'Username', 'placeholder': 'username', 'helper': 'Введите username без @'},
    'facebook': {'name': 'Facebook', 'icon': '👥', 'label': 'Username или ID', 'placeholder': 'username', 'helper': 'Введите username или ID'},
    'tiktok': {'name': 'TikTok', 'icon': '🎵', 'label': 'Username', 'placeholder': 'username', 'helper': 'Введите username без @'},
    'twitter': {'name': 'Twitter (X)', 'icon': '🐦', 'label': 'Username', 'placeholder': 'username', 'helper': 'Введите username без @'},
    'linkedin': {'name': 'LinkedIn', 'icon': '💼', 'label': 'Username', 'placeholder': 'username', 'helper': 'LinkedIn username'},
    'youtube': {'name': 'YouTube', 'icon': '📺', 'label': 'Канал', 'placeholder': '@channel или ID', 'helper': '@channel или ID'},
    'email': {'name': 'Email', 'icon': '📧', 'label': 'Email адрес', 'placeholder': 'example@mail.com', 'helper': 'Email адрес'},
    'phone': {'name': 'Телефон', 'icon': '📞', 'label': 'Номер телефона', 'placeholder': '+79991234567', 'helper': 'С кодом страны'}
}

@app.route('/')
def index():
    return render_template_string(HTML_MAIN)

@app.route('/generate')
def generate_page():
    qr_type = request.args.get('type', 'url')
    if qr_type not in QR_TYPES:
        return redirect('/')
    config = QR_TYPES[qr_type]
    return render_template_string(HTML_GENERATE, type=qr_type, type_name=config['name'], 
                                 type_icon=config['icon'], input_label=config['label'],
                                 placeholder=config['placeholder'], helper_text=config['helper'])

@app.route('/qr')
def generate_qr():
    data = request.args.get('data', '')
    if not data:
        return 'Error: parameter "data" is required', 400
    color = request.args.get('color', '000000')
    bgcolor = request.args.get('bgcolor', 'ffffff')
    size = int(request.args.get('size', 256))
    quietzone = int(request.args.get('quietzone', 4))
    try:
        fill_color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        back_color = tuple(int(bgcolor[i:i+2], 16) for i in (0, 2, 4))
    except:
        return 'Error: invalid color format. Use HEX without #', 400
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=quietzone)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/view')
def view_qr():
    data = request.args.get('data', '')
    if not data:
        return redirect('/')
    color = request.args.get('color', '000000')
    bgcolor = request.args.get('bgcolor', 'ffffff')
    size = request.args.get('size', '256')
    quietzone = request.args.get('quietzone', '4')
    qr_url = url_for('generate_qr', data=data, color=color, bgcolor=bgcolor, size=size, quietzone=quietzone)
    download_url = url_for('download_qr', data=data, color=color, bgcolor=bgcolor, size=size, quietzone=quietzone)
    return render_template_string(VIEW_TEMPLATE, qr_url=qr_url, download_url=download_url, 
                                 data=data, color=color, bgcolor=bgcolor, size=size)

@app.route('/download')
def download_qr():
    data = request.args.get('data', '')
    if not data:
        return 'Error: parameter "data" is required', 400
    color = request.args.get('color', '000000')
    bgcolor = request.args.get('bgcolor', 'ffffff')
    size = int(request.args.get('size', 256))
    quietzone = int(request.args.get('quietzone', 4))
    try:
        fill_color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        back_color = tuple(int(bgcolor[i:i+2], 16) for i in (0, 2, 4))
    except:
        return 'Error: invalid color format. Use HEX without #', 400
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=quietzone)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='qrcode.png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
