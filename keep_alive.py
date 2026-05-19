import threading
import time
import requests
import logging

logger = logging.getLogger(__name__)


class KeepAlive:
    """
    Клас для підтримки активності сервісу на Render.com
    Надсилає HTTP-запити до власного health-ендпоінту кожні 14 хвилин
    """

    def __init__(self, app_url=None, interval=840):
        """
        Args:
            app_url: URL застосунку (наприклад, 'https://your-app.onrender.com')
            interval: Інтервал у секундах (за замовчуванням 840 сек = 14 хв)
        """
        self.app_url = app_url
        self.interval = interval
        self.running = False
        self.thread = None

    def _ping(self):
        """Надсилає ping-запит до health-ендпоінту"""
        if not self.app_url:
            logger.warning("KeepAlive: app_url не задано, пропускаю ping")
            return

        try:
            # Додаємо таймаут, щоб не зависнути
            response = requests.get(
                f"{self.app_url}/health",
                timeout=10,
                headers={'User-Agent': 'KeepAlive/1.0'}
            )

            if response.status_code == 200:
                logger.info(f"KeepAlive: успішний ping — {self.app_url}")
            else:
                logger.warning(f"KeepAlive: ping повернув статус {response.status_code}")

        except requests.exceptions.RequestException as e:
            logger.error(f"KeepAlive: помилка ping — {e}")

    def _run(self):
        """Основний цикл для періодичних ping-запитів"""
        logger.info(f"KeepAlive: запущено (інтервал {self.interval} сек)")

        while self.running:
            time.sleep(self.interval)
            if self.running:  # Перевіряємо знову після sleep
                self._ping()

    def start(self):
        """Запускає фоновий потік для keep-alive"""
        if self.running:
            logger.warning("KeepAlive: вже запущено")
            return

        if not self.app_url:
            logger.info("KeepAlive: app_url не задано, keep-alive вимкнено")
            return

        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        logger.info("KeepAlive: потік запущено")

    def stop(self):
        """Зупиняє keep-alive"""
        if not self.running:
            return

        logger.info("KeepAlive: зупинка...")
        self.running = False

        if self.thread:
            self.thread.join(timeout=5)

        logger.info("KeepAlive: зупинено")
