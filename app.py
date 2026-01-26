from flask import Flask, request, send_file, render_template_string, redirect, url_for, jsonify
import qrcode
from io import BytesIO
from PIL import Image
from functools import lru_cache, wraps
from collections import defaultdict
import time
from threading import Lock
import logging

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Статистика
stats = {
    'total_requests': 0,
    'cache_hits': 0,
    'rate_limited': 0,
    'errors': 0,
    'web_generations': 0
}

# Rate Limiting
rate_limit_storage = defaultdict(list)
rate_limit_lock = Lock()

def get_client_ip():
    """Получает реальный IP клиента"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    return request.remote_addr

def rate_limit(max_requests=100, window=60):
    """Декоратор для rate limiting"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            ip = get_client_ip()
            current_time = time.time()
            
            with rate_limit_lock:
                rate_limit_storage[ip] = [
                    req_time for req_time in rate_limit_storage[ip]
                    if current_time - req_time < window
                ]
                
                if len(rate_limit_storage[ip]) >= max_requests:
                    stats['rate_limited'] += 1
                    logger.warning(f"Rate limit exceeded for IP: {ip}")
                    return jsonify({
                        'error': 'Rate limit exceeded',
                        'message': f'Максимум {max_requests} запросов в {window} сек.'
                    }), 429
                
                rate_limit_storage[ip].append(current_time)
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

@lru_cache(maxsize=512)
def create_qr_image(data, fill_color, back_color, size, quietzone):
    """Генерирует QR-код с кэшированием"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=quietzone
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf.read()

def parse_color(color_str):
    """Парсит цвет из HEX"""
    color_str = color_str.lstrip('#')
    if len(color_str) == 6:
        return tuple(int(color_str[i:i+2], 16) for i in (0, 2, 4))
    return (0, 0, 0)

def parse_size(size_param):
    """Парсит размер"""
    size_map = {'small': 256, 'medium': 512, 'large': 1024}
    
    if isinstance(size_param, str):
        size_lower = size_param.lower()
        if size_lower in size_map:
            return size_map[size_lower]
        try:
            size = int(size_param)
            return min(max(size, 64), 2048)
        except:
            return 256
    
    return min(max(int(size_param), 64), 2048)

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

HTML_MAIN = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Code Generator - Создание QR-кодов</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            text-align: center;
            font-size: 32px;
        }
        .subtitle {
            color: #666;
            text-align: center;
            margin-bottom: 40px;
            font-size: 16px;
        }
        .badge {
            display: inline-block;
            padding: 4px 12px;
            background: #28a745;
            color: white;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            margin-left: 10px;
        }
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            border-bottom: 2px solid #e0e0e0;
        }
        .tab {
            padding: 15px 25px;
            background: none;
            border: none;
            color: #666;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.3s;
        }
        .tab.active {
            color: #667eea;
            border-bottom-color: #667eea;
        }
        .tab:hover { color: #667eea; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .type-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
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
        .type-icon { font-size: 50px; margin-bottom: 12px; }
        .type-name { font-size: 15px; font-weight: 600; }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-box {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }
        .stat-value {
            font-size: 32px;
            font-weight: 700;
            color: #667eea;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
            font-size: 14px;
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
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #667eea;
            color: white;
            font-weight: 600;
        }
        .warning {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
            color: #856404;
        }
        @media (max-width: 768px) {
            .container { padding: 20px; }
            h1 { font-size: 24px; }
            .type-grid { grid-template-columns: repeat(2, 1fr); }
            .tabs { flex-wrap: wrap; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔲 QR Code Generator <span class="badge">PRO</span></h1>
        <p class="subtitle">Создавайте QR-коды онлайн или через API</p>
        
        <div class="tabs">
            <button class="tab active" onclick="switchTab('generator')">🎨 Генератор</button>
            <button class="tab" onclick="switchTab('api')">📖 API</button>
            <button class="tab" onclick="switchTab('stats')">📊 Статистика</button>
        </div>

        <div id="generator" class="tab-content active">
            <h2 style="color: #667eea; margin-bottom: 20px; font-size: 20px;">Выберите тип QR-кода</h2>
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
        </div>

        <div id="api" class="tab-content">
            <div class="api-section">
                <h2>🚀 Быстрый старт</h2>
                <p style="margin-bottom: 15px;">Просто используйте URL для получения QR-кода:</p>
                <div class="code-block">
<span class="param">GET</span> {request.host_url}qr?<span class="param">data</span>=<span class="string">YourData</span>
                </div>
            </div>

            <div class="api-section">
                <h2>📖 Параметры API</h2>
                <table>
                    <tr>
                        <th>Параметр</th>
                        <th>Описание</th>
                        <th>По умолчанию</th>
                    </tr>
                    <tr>
                        <td><code>data</code></td>
                        <td>Данные для QR-кода (обязательно, макс 1000 символов)</td>
                        <td>—</td>
                    </tr>
                    <tr>
                        <td><code>color</code></td>
                        <td>Цвет QR в HEX (с # или без)</td>
                        <td>000000</td>
                    </tr>
                    <tr>
                        <td><code>bgcolor</code></td>
                        <td>Цвет фона в HEX</td>
                        <td>ffffff</td>
                    </tr>
                    <tr>
                        <td><code>size</code></td>
                        <td>Small/Medium/Large или число (64-2048px)</td>
                        <td>256</td>
                    </tr>
                    <tr>
                        <td><code>quietzone</code></td>
                        <td>Отступы вокруг QR (0-10)</td>
                        <td>4</td>
                    </tr>
                </table>
            </div>

            <div class="api-section">
                <h2>💻 Примеры использования</h2>
                <h3 style="margin: 20px 0 10px 0;">HTML</h3>
                <div class="code-block">
&lt;img src="{request.host_url}qr?data=https://example.com&size=Medium"&gt;
                </div>

                <h3 style="margin: 20px 0 10px 0;">Python</h3>
                <div class="code-block">
import requests

url = "{request.host_url}qr"
params = {{"data": "https://t.me/channel", "color": "35b635", "size": "512"}}

response = requests.get(url, params=params)
with open('qrcode.png', 'wb') as f:
    f.write(response.content)
                </div>

                <h3 style="margin: 20px 0 10px 0;">JavaScript</h3>
                <div class="code-block">
fetch('{request.host_url}qr?data=MyData&color=FF5733')
  .then(r => r.blob())
  .then(blob => {{
    const img = document.createElement('img');
    img.src = URL.createObjectURL(blob);
    document.body.appendChild(img);
  }});
                </div>
            </div>

            <div class="warning">
                <strong>Rate Limit:</strong> 100 запросов в минуту с одного IP<br>
                <strong>Макс. длина данных:</strong> 1000 символов<br>
                <strong>Макс. размер:</strong> 2048x2048 пикселей
            </div>
        </div>

        <div id="stats" class="tab-content">
            <div class="api-section">
                <h2>📊 Статистика сервера</h2>
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-value">{stats['total_requests']}</div>
                        <div class="stat-label">Всего запросов</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{stats['web_generations']}</div>
                        <div class="stat-label">Веб-генераций</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{stats['cache_hits']}</div>
                        <div class="stat-label">Кэш-попадания</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{stats['rate_limited']}</div>
                        <div class="stat-label">Заблокировано</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{len(rate_limit_storage)}</div>
                        <div class="stat-label">Активных IP</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{stats['errors']}</div>
                        <div class="stat-label">Ошибок</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function switchTab(tabName) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(tabName).classList.add('active');
        }
    </script>
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
        .form-group { margin-bottom: 20px; }
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
        textarea { resize: vertical; min-height: 100px; }
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
            transition: transform 0.2s;
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
        .preview img { max-width: 100%; }
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
        }
        .error-message {
            background: #f8d7da;
            color: #721c24;
            padding: 12px;
            border-radius: 8px;
            margin-top: 15px;
            display: none;
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
            <div class="error-message" id="errorMessage"></div>
            <div class="preview" id="preview">
                <p style="color: #999;">QR-код появится здесь</p>
            </div>
            <div id="buttonGroup" style="display: none;" class="btn-group">
                <a class="btn-action" id="downloadBtn" href="#" download="qrcode.png">⬇️ Скачать</a>
                <a class="btn-action" id="viewBtn" href="#" target="_blank">👁️ Посмотреть</a>
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
        function showError(message) {
            const errorDiv = document.getElementById('errorMessage');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
            setTimeout(() => { errorDiv.style.display = 'none'; }, 5000);
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
            const downloadUrl = "/download?" + params;
            
            fetch(qrUrl)
                .then(response => {
                    if (response.status === 429) {
                        return response.json().then(data => {
                            throw new Error(data.message);
                        });
                    }
                    if (!response.ok) throw new Error('Ошибка генерации QR-кода');
                    return response.blob();
                })
                .then(blob => {
                    const imgUrl = URL.createObjectURL(blob);
                    document.getElementById('preview').innerHTML = '<img src="' + imgUrl + '" alt="QR Code">';
                    document.getElementById('buttonGroup').style.display = 'grid';
                    document.getElementById('downloadBtn').href = downloadUrl;
                    document.getElementById('viewBtn').href = qrUrl;
                })
                .catch(error => {
                    showError(error.message);
                });
        }
        document.getElementById('dataInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && qrType !== 'url') { e.preventDefault(); generateQR(); }
        });
    </script>
</body>
</html>
'''

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
@rate_limit(max_requests=100, window=60)
def generate_qr():
    stats['total_requests'] += 1
    
    data = request.args.get('data', '')
    if not data:
        stats['errors'] += 1
        return jsonify({'error': 'Параметр "data" обязателен'}), 400
    
    if len(data) > 1000:
        stats['errors'] += 1
        return jsonify({'error': 'Данные слишком длинные (макс 1000 символов)'}), 400
    
    color = request.args.get('color', '000000')
    bgcolor = request.args.get('bgcolor', 'ffffff')
    size = parse_size(request.args.get('size', '256'))
    quietzone = int(request.args.get('quietzone', 4))
    quietzone = min(max(quietzone, 0), 10)
    
    try:
        fill_color = parse_color(color)
        back_color = parse_color(bgcolor)
    except Exception as e:
        stats['errors'] += 1
        return jsonify({'error': 'Неверный формат цвета'}), 400
    
    try:
        cache_info = create_qr_image.cache_info()
        initial_hits = cache_info.hits
        
        img_bytes = create_qr_image(data, fill_color, back_color, size, quietzone)
        
        cache_info = create_qr_image.cache_info()
        if cache_info.hits > initial_hits:
            stats['cache_hits'] += 1
        
        stats['web_generations'] += 1
        ip = get_client_ip()
        logger.info(f"QR generated - IP: {ip}, Size: {size}")
        
        return send_file(
            BytesIO(img_bytes),
            mimetype='image/png',
            as_attachment=False,
            download_name='qrcode.png'
        )
    except Exception as e:
        stats['errors'] += 1
        logger.error(f"QR generation error: {e}")
        return jsonify({'error': 'Ошибка генерации QR-кода'}), 500

@app.route('/download')
@rate_limit(max_requests=100, window=60)
def download_qr():
    stats['total_requests'] += 1
    
    data = request.args.get('data', '')
    if not data:
        return jsonify({'error': 'Параметр "data" обязателен'}), 400
    
    if len(data) > 1000:
        return jsonify({'error': 'Данные слишком длинные'}), 400
    
    color = request.args.get('color', '000000')
    bgcolor = request.args.get('bgcolor', 'ffffff')
    size = parse_size(request.args.get('size', '256'))
    quietzone = int(request.args.get('quietzone', 4))
    quietzone = min(max(quietzone, 0), 10)
    
    try:
        fill_color = parse_color(color)
        back_color = parse_color(bgcolor)
        img_bytes = create_qr_image(data, fill_color, back_color, size, quietzone)
        
        return send_file(
            BytesIO(img_bytes),
            mimetype='image/png',
            as_attachment=True,
            download_name='qrcode.png'
        )
    except Exception as e:
        logger.error(f"Download error: {e}")
        return jsonify({'error': 'Ошибка скачивания'}), 500

@app.route('/stats')
def show_stats():
    cache_info = create_qr_image.cache_info()
    
    return jsonify({
        'total_requests': stats['total_requests'],
        'web_generations': stats['web_generations'],
        'cache_hits': stats['cache_hits'],
        'rate_limited': stats['rate_limited'],
        'errors': stats['errors'],
        'active_ips': len(rate_limit_storage),
        'cache': {
            'size': cache_info.currsize,
            'max_size': cache_info.maxsize,
            'hits': cache_info.hits,
            'misses': cache_info.misses,
            'hit_rate': round(cache_info.hits / (cache_info.hits + cache_info.misses) * 100, 2) if (cache_info.hits + cache_info.misses) > 0 else 0
        }
    })

@app.route('/health')
def health_check():
    return jsonify({'status': 'ok', 'service': 'QR Code API', 'version': '2.0.0'}), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': ['/qr', '/download', '/stats', '/health']
    }), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal error: {e}")
    return jsonify({'error': 'Внутренняя ошибка сервера'}), 500
