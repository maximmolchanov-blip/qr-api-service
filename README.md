
# 📖 Інструкція з використання Генератора QR-кодів

## 🌐 Вебінтерфейс (через сайт)

### Адреса сервісу

**[https://qr-api-service.onrender.com](https://qr-api-service.onrender.com)**

### Як створити QR-код через сайт:

#### **Крок 1: Оберіть тип QR-коду**

На головній сторінці доступні такі типи:

| Іконка | Тип QR-коду | Призначення                  |
| ------ | ----------- | ---------------------------- |
| 🔗     | URL / Текст | Для посилань і будь-якого тексту |
| ✈️     | Telegram    | Для профілів Telegram        |
| 💬     | WhatsApp    | Для чату WhatsApp            |
| 📷     | Instagram   | Для профілів Instagram       |
| 👥     | Facebook    | Для профілів Facebook        |
| 🎵     | TikTok      | Для профілів TikTok          |
| 🐦     | Twitter (X) | Для профілів Twitter         |
| 💼     | LinkedIn    | Для профілів LinkedIn        |
| 📺     | YouTube     | Для каналів YouTube          |
| 📧     | Email       | Для надсилання email         |
| 📞     | Телефон     | Для дзвінків                 |

#### **Крок 2: Заповніть дані**

Залежно від типу введіть:

* URL: `https://example.com`
* Telegram: `username` (без @)
* WhatsApp: `+380991234567` (з кодом країни)
* Instagram: `username` (без @)
* Email: `example@mail.com`
* Телефон: `+380991234567`
* YouTube: `@channel` або ID каналу
* Інші типи — аналогічно

#### **Крок 3: Налаштуйте зовнішній вигляд**

* **Колір QR** — колір коду (за замовчуванням чорний `#000000`)
* **Колір фону** — колір фону (за замовчуванням білий `#ffffff`)
* **Розмір** — 256×256, 512×512, 1024×1024 пікселів
* **Відступи (quietzone)** — малі, середні, великі

#### **Крок 4: Створіть і завантажте**

* Натисніть **"Створити QR-код"**
* Кнопка **"👁️ Переглянути"** відкриє QR на окремій сторінці
* Кнопка **"⬇️ Завантажити"** збереже зображення на комп'ютер

---

## 🔗 API (через прямі посилання)

### **Метод 1: Отримати зображення напряму**

Ендпоінт `/qr` повертає PNG-зображення QR-коду:

```
https://qr-api-service.onrender.com/qr?data=ВАШІ_ДАНІ
```

Приклади:

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
https://qr-api-service.onrender.com/qr?data=https://wa.me/380991234567
```

* Email:

```
https://qr-api-service.onrender.com/qr?data=mailto:example@mail.com
```

---

### **Метод 2: Налаштований QR-код з параметрами**

Параметри:

| Параметр    | Опис                                              |
| ----------- | ------------------------------------------------- |
| `data`      | Дані для кодування (**обов'язковий**)             |
| `color`     | Колір QR у HEX без # (наприклад `ff0000`)         |
| `bgcolor`   | Колір фону у HEX без #                            |
| `size`      | Розмір зображення у пікселях (256, 512, 1024)     |
| `quietzone` | Відступи (2, 4, 6)                                |

Приклади:

* Червоний QR на білому фоні:

```
https://qr-api-service.onrender.com/qr?data=https://google.com&color=ff0000&bgcolor=ffffff&size=512
```

* Синій QR для Telegram:

```
https://qr-api-service.onrender.com/qr?data=https://t.me/username&color=0088cc&size=512
```

---

### **Метод 3: Перегляд QR на сторінці**

Ендпоінт `/view` відкриває сторінку з QR-кодом:

```
https://qr-api-service.onrender.com/view?data=https://google.com&color=000000&bgcolor=ffffff&size=256
```

---

### **Метод 4: Завантаження QR**

Ендпоінт `/download` завантажує QR-код:

```
https://qr-api-service.onrender.com/download?data=https://google.com
```

Приклади:

* Завантажити QR для Instagram:

```
https://qr-api-service.onrender.com/download?data=https://instagram.com/username
```

* Завантажити великий QR-код:

```
https://qr-api-service.onrender.com/download?data=https://youtube.com/@channelname&size=1024
```

* Завантажити кольоровий QR:

```
https://qr-api-service.onrender.com/download?data=mailto:contact@company.com&color=e74c3c&size=512
```

## 🎨 Популярні кольори для соцмереж

| Сервіс    | HEX колір QR |
| --------- | ------------ |
| Instagram | `e4405f`     |
| WhatsApp  | `25d366`     |
| Telegram  | `0088cc`     |
| Facebook  | `1877f2`     |
| TikTok    | `fe2c55`     |
| YouTube   | `ff0000`     |

---

## ⚠️ Важливі зауваження

1. Спецсимволи в `data` мають бути закодовані (` ` → `%20`, `@` → `%40`)
2. Кольори — HEX без `#`
3. Розмір за замовчуванням — 256×256
```
