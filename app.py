from flask import Flask, request, send_file, render_template_string
import qrcode
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# HTML страница для генератора
HTML_TEMPLATE = '''
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
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 800px;
            width: 100%;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            text-align: center;
        }
        .subtitle {
            color: #666;
            text-align: center;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .section {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 25px;
        }
        .section h2 {
            color: #667eea;
            font-size: 18px;
            margin-bottom: 15px;
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
        input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        .color-group {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
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
        .btn:active {
            transform: translateY(0);
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
        }
        .preview img {
            max-width: 100%;
            height: auto;
        }
        .api-url {
            background: #333;
            color: #0f0;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            word-break: break-all;
            margin-top: 15px;
        }
        .code-block {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            overflow-x: auto;
            margin-top: 10px;
        }
        .param {
            color: #f92672;
        }
        .string {
            color: #a6e22e;
        }
        small {
            color: #666;
            font-size: 12px;
            display: block;
            margin-top: 5px;
        }
        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }
            .color-group {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔲 QR Code API Service</h1>
        <p class="subtitle">Бесплатный генератор QR-кодов с API</p>

        <!-- Generator Section -->
        <div class="section">
            <h2>Генератор QR-кодов</h2>
            <div class="form-group">
                <label>Данные для QR-кода</label>
                <input type="text" id="qrData" placeholder="https://t.me/your_bot" value="https://t.me/bot">
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
                    <label>Размер (px)</label>
                    <select id="qrSize">
                        <option value="128">128x128</option>
                        <option value="256" selected>256x256</option>
                        <option value="512">512x512</option>
                        <option value="1024">1024x1024</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Отступы</label>
                    <select id="quietZone">
                        <option value="2">Маленькие (2)</option>
                        <option value="4" selected>Средние (4)</option>
                        <option value="6">Большие (6)</option>
                    </select>
                </div>
            </div>

            <button class="btn" onclick="generateQR()">Создать QR-код</button>

            <div class="preview" id="preview">
                <p style="color: #999;">QR-код появится здесь</p>
            </div>

            <div id="apiUrlBlock" style="display: none;">
                <small>Прямая ссылка на QR-код:</small>
                <div class="api-url" id="apiUrl"></div>
            </div>
        </div>

        <!-- API Documentation -->
        <div class="section">
            <h2>📖 API Документация</h2>
            <p style="margin-bottom: 15px; color: #555;">
                Используйте GET-запрос для генерации QR-кодов:
            </p>
            
            <div class="code-block">
GET /qr?<span class="param">data</span>=<span class="string">https://example.com</span>&<span class="param">color</span>=<span class="string">000000</span>&<span class="param">bgcolor</span>=<span class="string">ffffff</span>&<span class="param">size</span>=<span class="string">256</span>&<span class="param">quietzone</span>=<span class="string">4</span>
            </div>

            <div style="margin-top: 20px;">
                <strong>Параметры:</strong>
                <ul style="margin-left: 20px; margin-top: 10px; color: #555; line-height: 1.8;">
                    <li><code>data</code> - данные для кодирования (обязательный)</li>
                    <li><code>color</code> - цвет QR в HEX без # (по умолчанию: 000000)</li>
                    <li><code>bgcolor</code> - цвет фона в HEX без # (по умолчанию: ffffff)</li>
                    <li><code>size</code> - размер в пикселях (по умолчанию: 256)</li>
                    <li><code>quietzone</code> - отступы вокруг QR (по умолчанию: 4)</li>
                </ul>
            </div>

            <div style="margin-top: 20px;">
                <strong>Пример использования:</strong>
                <div class="code-block">
&lt;img src="https://ваш-домен.com/qr?data=https://t.me/bot&color=35b635&size=256"&gt;
                </div>
            </div>
        </div>
    </div>

    <script>
        function generateQR() {
            const data = document.getElementById('qrData').value;
            const color = document.getElementById('qrColor').value.replace('#', '');
            const bgcolor = document.getElementById('bgColor').value.replace('#', '');
            const size = document.getElementById('qrSize').value;
            const quietzone = document.getElementById('quietZone').value;

            if (!data) {
                alert('Введите данные для QR-кода');
                return;
            }

            const url = `/qr?data=${encodeURIComponent(data)}&color=${color}&bgcolor=${bgcolor}&size=${size}&quietzone=${quietzone}`;
            
            document.getElementById('preview').innerHTML = `<img src="${url}" alt="QR Code">`;
            document.getElementById('apiUrlBlock').style.display = 'block';
            document.getElementById('apiUrl').textContent = window.location.origin + url;
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/qr')
def generate_qr():
    # Получаем параметры из запроса
    data = request.args.get('data', '')
    if not data:
        return 'Error: parameter "data" is required', 400
    
    # Параметры QR-кода
    color = request.args.get('color', '000000')
    bgcolor = request.args.get('bgcolor', 'ffffff')
    size = int(request.args.get('size', 256))
    quietzone = int(request.args.get('quietzone', 4))
    
    # Преобразуем HEX в RGB
    try:
        fill_color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        back_color = tuple(int(bgcolor[i:i+2], 16) for i in (0, 2, 4))
    except:
        return 'Error: invalid color format. Use HEX without #', 400
    
    # Создаем QR-код
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=quietzone,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Генерируем изображение
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    # Изменяем размер
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    
    # Сохраняем в буфер
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)