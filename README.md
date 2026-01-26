# 📖 Инструкция по использованию QR Code API

## 🌐 Главная страница

**URL сервиса:** `https://your-domain.com`

На главной странице вы найдете:
- 📊 **Статистику сервера** в реальном времени (общее количество запросов, кэш-попадания, заблокированные запросы)
- 🚀 **Быстрый старт** с примерами
- 📖 **Полную документацию** по API
- 💻 **Примеры кода** для разных языков программирования

---

## 🔗 API Эндпоинты

### **1. Генерация QR-кода: `/qr`**

Основной эндпоинт для получения PNG-изображения QR-кода.

#### **Базовый формат:**
```
GET https://your-domain.com/qr?data=ВАШИ_ДАННЫЕ
```

#### **Обязательные параметры:**
- `data` — данные для кодирования (макс 1000 символов)

#### **Опциональные параметры:**
- `color` — цвет QR в HEX без # (по умолчанию: `000000` - черный)
- `bgcolor` — цвет фона в HEX без # (по умолчанию: `ffffff` - белый)
- `size` — размер изображения:
  - Варианты: `Small` (256px), `Medium` (512px), `Large` (1024px)
  - Или число от 64 до 2048 пикселей
  - По умолчанию: `256`
- `quietzone` — отступы вокруг QR (от 0 до 10, по умолчанию: `4`)

---

## 💡 Примеры использования

### **Простые примеры**

**1. Базовый QR-код:**
```
https://your-domain.com/qr?data=https://google.com
```

**2. Telegram профиль:**
```
https://your-domain.com/qr?data=https://t.me/channel
```

**3. WhatsApp чат:**
```
https://your-domain.com/qr?data=https://wa.me/79991234567
```

**4. Email:**
```
https://your-domain.com/qr?data=mailto:example@gmail.com
```

**5. Телефон:**
```
https://your-domain.com/qr?data=tel:+79991234567
```

---

### **Примеры с настройками**

**Зеленый QR-код для Telegram:**
```
https://your-domain.com/qr?data=https://t.me/channel&color=35b635&quietzone=6&size=Small
```

**Красный QR-код среднего размера:**
```
https://your-domain.com/qr?data=https://example.com&color=ff0000&bgcolor=ffffff&size=Medium
```

**Белый QR на черном фоне:**
```
https://your-domain.com/qr?data=Hello%20World&color=ffffff&bgcolor=000000&size=Large
```

**QR точного размера 800px:**
```
https://your-domain.com/qr?data=https://youtube.com/@channel&size=800
```

**Синий QR с минимальными отступами:**
```
https://your-domain.com/qr?data=https://instagram.com/username&color=0088cc&quietzone=0&size=512
```

---

## 💻 Интеграция в код

### **HTML**
```html
<!-- Вставка QR-кода на страницу -->
<img src="https://your-domain.com/qr?data=https://example.com&size=Medium" 
     alt="QR Code">
```

### **Python**
```python
import requests

# Генерация и сохранение QR-кода
url = "https://your-domain.com/qr"
params = {
    "data": "https://t.me/channel",
    "color": "35b635",
    "size": "512",
    "quietzone": "6"
}

response = requests.get(url, params=params)
with open('qrcode.png', 'wb') as f:
    f.write(response.content)

print("QR-код сохранен!")
```

### **JavaScript/Fetch API**
```javascript
// Загрузка и отображение QR-кода
fetch('https://your-domain.com/qr?data=MyData&color=FF5733&size=Medium')
  .then(response => response.blob())
  .then(blob => {
    const img = document.createElement('img');
    img.src = URL.createObjectURL(blob);
    document.body.appendChild(img);
  });
```

### **cURL (командная строка)**
```bash
# Скачивание QR-кода через терминал
curl "https://your-domain.com/qr?data=Test&size=Large&color=0000ff" -o qr.png
```

### **PHP**
```php
<?php
// Получение QR-кода
$url = "https://your-domain.com/qr?data=https://example.com&size=512";
$qrImage = file_get_contents($url);
file_put_contents('qrcode.png', $qrImage);
echo "QR-код создан!";
?>
```

---

## 🎨 Популярные цветовые схемы

**Социальные сети:**
- **Telegram:** `color=0088cc`
- **WhatsApp:** `color=25d366`
- **Instagram:** `color=e4405f`
- **Facebook:** `color=1877f2`
- **TikTok:** `color=fe2c55`
- **YouTube:** `color=ff0000`
- **Twitter/X:** `color=1da1f2`
- **LinkedIn:** `color=0077b5`

**Пример с брендовым цветом:**
```
https://your-domain.com/qr?data=https://t.me/mychannel&color=0088cc&size=Medium&quietzone=6
```

---

## 📊 Дополнительные эндпоинты

### **2. Статистика: `/stats`**
Возвращает JSON со статистикой сервера.

**Запрос:**
```
GET https://your-domain.com/stats
```

**Ответ:**
```json
{
  "total_requests": 1523,
  "cache_hits": 847,
  "rate_limited": 12,
  "errors": 3,
  "active_ips": 45,
  "cache": {
    "size": 312,
    "max_size": 512,
    "hits": 847,
    "misses": 676,
    "hit_rate": 55.62
  }
}
```

### **3. Health Check: `/health`**
Проверка работоспособности сервиса.

**Запрос:**
```
GET https://your-domain.com/health
```

**Ответ:**
```json
{
  "status": "ok",
  "service": "QR Code API",
  "version": "1.0.0"
}
```

---

## 🛡️ Ограничения и лимиты

### **Rate Limiting**
- **Лимит:** 100 запросов в минуту с одного IP
- **При превышении:** HTTP 429 (Too Many Requests)
- **Время ожидания:** 60 секунд

### **Ограничения данных**
- **Максимальная длина данных:** 1000 символов
- **Минимальный размер QR:** 64x64 пикселей
- **Максимальный размер QR:** 2048x2048 пикселей
- **Диапазон quietzone:** 0-10

### **Обработка ошибок**

**Отсутствует параметр `data`:**
```json
{
  "error": "Параметр \"data\" обязателен"
}
```
HTTP 400

**Данные слишком длинные:**
```json
{
  "error": "Данные слишком длинные (макс 1000 символов)"
}
```
HTTP 400

**Превышен лимит запросов:**
```json
{
  "error": "Rate limit exceeded",
  "message": "Максимум 100 запросов в минуту. Попробуйте через 60 секунд."
}
```
HTTP 429

**Неверный формат цвета:**
```json
{
  "error": "Неверный формат цвета. Используйте HEX (например: FF5733)"
}
```
HTTP 400

---

## ⚡ Производительность

### **Кэширование**
- В памяти хранится до **512 популярных QR-кодов**
- Генерация нового QR: **~50ms**
- Из кэша: **~2ms**
- Автоматическая очистка старых записей

### **Оптимизация**
- Используйте одинаковые параметры для часто используемых QR — они будут браться из кэша
- Для статичных QR сохраняйте изображения локально, а не запрашивайте каждый раз

---

## 🔄 Совместимость с tec-it API

Этот API **полностью совместим** с базовыми параметрами tec-it.com QR Code API.

**Миграция:**
```
❌ Старый URL:
https://qrcode.tec-it.com/API/QRCode?data=Test&color=35b635

✅ Новый URL:
https://your-domain.com/qr?data=Test&color=35b635
```

Просто замените домен — все параметры работают одинаково!

---

## 🌟 Практические кейсы

### **1. Визитная карточка (vCard)**
```
https://your-domain.com/qr?data=BEGIN:VCARD%0AVERSION:3.0%0AFN:John%20Doe%0ATEL:+1234567890%0AEMAIL:john@example.com%0AEND:VCARD&size=512
```

### **2. Wi-Fi подключение**
```
https://your-domain.com/qr?data=WIFI:T:WPA;S:MyNetwork;P:password123;;&size=Medium
```

### **3. SMS сообщение**
```
https://your-domain.com/qr?data=sms:+79991234567?body=Hello%20World&size=256
```

### **4. Геолокация**
```
https://your-domain.com/qr?data=geo:48.8584,2.2945?q=Eiffel%20Tower&size=Large
```

### **5. Календарное событие**
```
https://your-domain.com/qr?data=BEGIN:VEVENT%0ASUMMARY:Meeting%0ADTSTART:20260201T100000Z%0ADTEND:20260201T110000Z%0AEND:VEVENT&size=512
```

---

## 📝 Важные замечания

1. **URL-кодирование:** Специальные символы должны быть закодированы:
   - Пробел → `%20`
   - @ → `%40`
   - # → `%23`
   - & → `%26`

2. **Формат цвета:** HEX без символа `#`:
   - ✅ Правильно: `color=ff0000`
   - ❌ Неправильно: `color=#ff0000`

3. **Размер файла:** Small (256px) ≈ 2-5 KB, Medium (512px) ≈ 5-10 KB, Large (1024px) ≈ 10-20 KB

4. **CORS:** API поддерживает запросы с любых доменов

---

## 🚀 Быстрый старт

**Самый простой вариант:**
```
https://your-domain.com/qr?data=YourText
```

**С настройками:**
```
https://your-domain.com/qr?data=https://t.me/channel&color=0088cc&size=Medium&quietzone=6
```

**Вставка в HTML:**
```html
<img src="https://your-domain.com/qr?data=https://example.com" alt="QR">
```

---

## 📞 Поддержка

- Главная страница с документацией: `https://your-domain.com`
- Health check: `https://your-domain.com/health`
- Статистика: `https://your-domain.com/stats`

**Uptime:** 99.9% на платформе Render
