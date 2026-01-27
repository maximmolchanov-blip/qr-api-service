

# 📖 Инструкция по использованию QR Code Generator

## 🌐 Веб-интерфейс (через сайт)

### Адрес сервиса

**[https://qr-api-service.onrender.com](https://qr-api-service.onrender.com)**

### Как создать QR-код через сайт:

#### **Шаг 1: Выберите тип QR-кода**

На главной странице доступны следующие типы:

| Иконка | Тип QR-кода | Назначение                 |
| ------ | ----------- | -------------------------- |
| 🔗     | URL / Текст | Для ссылок и любого текста |
| ✈️     | Telegram    | Для профилей Telegram      |
| 💬     | WhatsApp    | Для WhatsApp чата          |
| 📷     | Instagram   | Для профилей Instagram     |
| 👥     | Facebook    | Для профилей Facebook      |
| 🎵     | TikTok      | Для профилей TikTok        |
| 🐦     | Twitter (X) | Для профилей Twitter       |
| 💼     | LinkedIn    | Для профилей LinkedIn      |
| 📺     | YouTube     | Для каналов YouTube        |
| 📧     | Email       | Для отправки email         |
| 📞     | Телефон     | Для звонков                |

#### **Шаг 2: Заполните данные**

В зависимости от типа введите:

* URL: `https://example.com`
* Telegram: `username` (без @)
* WhatsApp: `+79991234567` (с кодом страны)
* Instagram: `username` (без @)
* Email: `example@mail.com`
* Телефон: `+79991234567`
* YouTube: `@channel` или ID канала
* Остальные типы аналогично

#### **Шаг 3: Настройте внешний вид**

* **Цвет QR** — цвет кода (по умолчанию черный `#000000`)
* **Цвет фона** — цвет фона (по умолчанию белый `#ffffff`)
* **Размер** — 256x256, 512x512, 1024x1024 пикселей
* **Отступы (quietzone)** — маленькие, средние, большие

#### **Шаг 4: Создайте и скачайте**

* Нажмите **"Создать QR-код"**
* Кнопка **"👁️ Посмотреть"** откроет QR на отдельной странице
* Кнопка **"⬇️ Скачать"** сохранит изображение на компьютер

---

## 🔗 API (через прямые ссылки)

### **Метод 1: Получить изображение напрямую**

Эндпоинт `/qr` возвращает PNG-изображение QR-кода:

```
https://qr-api-service.onrender.com/qr?data=ВАШИ_ДАННЫЕ
```

Примеры:

* Текст/URL:

```
https://qr-api-service.onrender.com/qr?data=https://google.com
```

* Telegram:

```
https://qr-api-service.onrender.com/qr?data=https://t.me/username
```

* WhatsApp:

```
https://qr-api-service.onrender.com/qr?data=https://wa.me/79991234567
```

* Email:

```
https://qr-api-service.onrender.com/qr?data=mailto:example@mail.com
```

---

### **Метод 2: Настроенный QR-код с параметрами**

Параметры:

| Параметр    | Описание                                       |
| ----------- | ---------------------------------------------- |
| `data`      | Данные для кодирования (**обязательный**)      |
| `color`     | Цвет QR в HEX без # (например `ff0000`)        |
| `bgcolor`   | Цвет фона в HEX без #                          |
| `size`      | Размер изображения в пикселях (256, 512, 1024) |
| `quietzone` | Отступы (2, 4, 6)                              |

Примеры:

* Красный QR на белом фоне:

```
https://qr-api-service.onrender.com/qr?data=https://google.com&color=ff0000&bgcolor=ffffff&size=512
```

* Синий QR для Telegram:

```
https://qr-api-service.onrender.com/qr?data=https://t.me/username&color=0088cc&size=512
```

---

### **Метод 3: Просмотр QR на странице**

Эндпоинт `/view` открывает страницу с QR-кодом:

```
https://qr-api-service.onrender.com/view?data=https://google.com&color=000000&bgcolor=ffffff&size=256
```

---

### **Метод 4: Скачивание QR**

Эндпоинт `/download` скачивает QR-код:

```
https://qr-api-service.onrender.com/download?data=https://google.com
```

Примеры:

* Скачать QR для Instagram:

```
https://qr-api-service.onrender.com/download?data=https://instagram.com/username
```

* Скачать большой QR-код:

```
https://qr-api-service.onrender.com/download?data=https://youtube.com/@channelname&size=1024
```

* Скачать цветной QR:

```
https://qr-api-service.onrender.com/download?data=mailto:contact@company.com&color=e74c3c&size=512
```

## 🎨 Популярные цвета для соцсетей

| Сервис    | HEX цвет QR |
| --------- | ----------- |
| Instagram | `e4405f`    |
| WhatsApp  | `25d366`    |
| Telegram  | `0088cc`    |
| Facebook  | `1877f2`    |
| TikTok    | `fe2c55`    |
| YouTube   | `ff0000`    |

---

## ⚠️ Важные замечания

1. Спецсимволы в `data` должны быть закодированы (` ` → `%20`, `@` → `%40`)
2. Цвета — HEX без `#`
3. Размер по умолчанию — 256x256
4. Rate limit: **максимум 10 запросов в секунду с одного IP**
5. Максимальная длина данных — 1000 символов


