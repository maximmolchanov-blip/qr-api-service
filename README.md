# qr-api-service
# 📖 Инструкция по использованию QR Code Generator

## 🌐 Веб-интерфейс (через сайт)

### Адрес сервиса
**https://qr-api-service.onrender.com**

### Как создать QR-код через сайт:

#### **Шаг 1: Выберите тип QR-кода**
На главной странице доступны следующие типы:
- 🔗 **URL / Текст** — для ссылок и любого текста
- ✈️ **Telegram** — для профилей Telegram
- 💬 **WhatsApp** — для WhatsApp чата
- 📷 **Instagram** — для профилей Instagram
- 👥 **Facebook** — для профилей Facebook
- 🎵 **TikTok** — для профилей TikTok
- 🐦 **Twitter (X)** — для профилей Twitter
- 💼 **LinkedIn** — для профилей LinkedIn
- 📺 **YouTube** — для каналов YouTube
- 📧 **Email** — для отправки email
- 📞 **Телефон** — для звонков

#### **Шаг 2: Заполните данные**
В зависимости от типа введите:
- Для URL: `https://example.com`
- Для Telegram: `username` (без @)
- Для WhatsApp: `+79991234567` (с кодом страны)
- Для Instagram: `username` (без @)
- Для Email: `example@mail.com`
- И так далее...

#### **Шаг 3: Настройте внешний вид**
- **Цвет QR** — выберите цвет самого кода (по умолчанию черный)
- **Цвет фона** — выберите цвет фона (по умолчанию белый)
- **Размер** — выберите размер: 256x256, 512x512 или 1024x1024 пикселей
- **Отступы** — маленькие, средние или большие

#### **Шаг 4: Создайте и скачайте**
- Нажмите **"Создать QR-код"**
- Используйте кнопку **"👁️ Посмотреть"** для просмотра на отдельной странице
- Используйте кнопку **"⬇️ Скачать"** для сохранения на компьютер

---

## 🔗 API (через прямые ссылки)

### **Метод 1: Получить изображение напрямую**

Используйте эндпоинт `/qr` для получения PNG-изображения:

```
https://qr-api-service.onrender.com/qr?data=ВАШИ_ДАННЫЕ
```

#### Примеры для разных типов:

**1. Простой текст или URL:**
```
https://qr-api-service.onrender.com/qr?data=https://google.com
```

**2. Telegram профиль:**
```
https://qr-api-service.onrender.com/qr?data=https://t.me/durov
```

**3. WhatsApp (звонок/чат):**
```
https://qr-api-service.onrender.com/qr?data=https://wa.me/79991234567
```

**4. Instagram профиль:**
```
https://qr-api-service.onrender.com/qr?data=https://instagram.com/instagram
```

**5. Email:**
```
https://qr-api-service.onrender.com/qr?data=mailto:example@gmail.com
```

**6. Телефон:**
```
https://qr-api-service.onrender.com/qr?data=tel:+79991234567
```

**7. YouTube канал:**
```
https://qr-api-service.onrender.com/qr?data=https://youtube.com/@channelname
```

**8. TikTok профиль:**
```
https://qr-api-service.onrender.com/qr?data=https://tiktok.com/@username
```

**9. Twitter/X профиль:**
```
https://qr-api-service.onrender.com/qr?data=https://twitter.com/elonmusk
```

**10. LinkedIn профиль:**
```
https://qr-api-service.onrender.com/qr?data=https://linkedin.com/in/username
```

**11. Facebook профиль:**
```
https://qr-api-service.onrender.com/qr?data=https://facebook.com/zuck
```

---

### **Метод 2: Настроенный QR-код с параметрами**

Добавьте параметры для кастомизации:

#### Все доступные параметры:
- `data` — данные для кодирования (**обязательный**)
- `color` — цвет QR в HEX без # (например: `ff0000` для красного)
- `bgcolor` — цвет фона в HEX без # (например: `000000` для черного)
- `size` — размер в пикселях (256, 512, 1024)
- `quietzone` — отступы вокруг кода (2, 4, 6)

#### Примеры с параметрами:

**Красный QR-код на белом фоне:**
```
https://qr-api-service.onrender.com/qr?data=https://google.com&color=ff0000&bgcolor=ffffff&size=512
```

**Белый QR-код на черном фоне:**
```
https://qr-api-service.onrender.com/qr?data=Hello%20World&color=ffffff&bgcolor=000000&size=1024
```

**Синий QR-код размером 512px с большими отступами:**
```
https://qr-api-service.onrender.com/qr?data=https://t.me/durov&color=0000ff&bgcolor=ffffff&size=512&quietzone=6
```

**Зеленый QR для WhatsApp:**
```
https://qr-api-service.onrender.com/qr?data=https://wa.me/79991234567&color=25d366&bgcolor=ffffff&size=256
```

---

### **Метод 3: Просмотр на странице**

Эндпоинт `/view` открывает QR-код на отдельной странице с информацией:

```
https://qr-api-service.onrender.com/view?data=https://google.com&color=000000&bgcolor=ffffff&size=256
```

**Пример:**
```
https://qr-api-service.onrender.com/view?data=https://t.me/durov&color=0088cc&size=512
```

---

### **Метод 4: Прямое скачивание**

Эндпоинт `/download` автоматически скачивает файл `qrcode.png`:

```
https://qr-api-service.onrender.com/download?data=https://google.com
```

**Примеры для скачивания:**

**Скачать QR для Instagram:**
```
https://qr-api-service.onrender.com/download?data=https://instagram.com/cristiano
```

**Скачать большой QR-код:**
```
https://qr-api-service.onrender.com/download?data=https://youtube.com/@MrBeast&size=1024
```

**Скачать цветной QR:**
```
https://qr-api-service.onrender.com/download?data=mailto:contact@company.com&color=e74c3c&size=512
```

---

## 💡 Практические примеры использования

### **Визитная карточка (vCard):**
```
https://qr-api-service.onrender.com/qr?data=BEGIN:VCARD%0AVERSION:3.0%0AFN:John%20Doe%0ATEL:+1234567890%0AEMAIL:john@example.com%0AEND:VCARD
```

### **Wi-Fi подключение:**
```
https://qr-api-service.onrender.com/qr?data=WIFI:T:WPA;S:NetworkName;P:password123;;
```

### **SMS сообщение:**
```
https://qr-api-service.onrender.com/qr?data=sms:+79991234567?body=Hello
```

### **Геолокация (Google Maps):**
```
https://qr-api-service.onrender.com/qr?data=https://maps.google.com/?q=48.8584,2.2945
```

---

## 🎨 Популярные цветовые комбинации

**Instagram (градиент розовый-фиолетовый):**
```
color=e4405f
```

**WhatsApp (зеленый):**
```
color=25d366
```

**Telegram (синий):**
```
color=0088cc
```

**Facebook (синий):**
```
color=1877f2
```

**TikTok (черно-розовый):**
```
color=000000 или color=fe2c55
```

**YouTube (красный):**
```
color=ff0000
```

---

## ⚠️ Важные замечания

1. **Специальные символы** в параметре `data` должны быть закодированы (например, пробел = `%20`, @ = `%40`)
2. **Цвета** указываются в HEX формате **без символа #** (правильно: `ff0000`, неправильно: `#ff0000`)
3. **Размер по умолчанию** — 256x256 пикселей
4. **Максимальный размер** — 1024x1024 пикселей
5. Для **коротких ссылок** используйте сервисы сокращения URL перед генерацией QR

---

## 🚀 Быстрый старт

**Самый простой способ:**
1. Откройте https://qr-api-service.onrender.com
2. Выберите нужный тип
3. Введите данные
4. Скачайте готовый QR-код

**Для разработчиков:**
Вставьте в HTML для отображения QR прямо на странице:
```html
<img src="https://qr-api-service.onrender.com/qr?data=https://yoursite.com" alt="QR Code">
```
