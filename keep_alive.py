import threading
import time
import requests
import logging

logger = logging.getLogger(__name__)

class KeepAlive:
    """
    Класс для поддержания активности сервиса на Render.com
    Отправляет HTTP-запросы к собственному health endpoint каждые 14 минут
    """
    
    def __init__(self, app_url=None, interval=840):
        """
        Args:
            app_url: URL приложения (например, 'https://your-app.onrender.com')
            interval: Интервал в секундах (по умолчанию 840 сек = 14 мин)
        """
        self.app_url = app_url
        self.interval = interval
        self.running = False
        self.thread = None
        
    def _ping(self):
        """Отправляет ping-запрос к health endpoint"""
        if not self.app_url:
            logger.warning("KeepAlive: app_url не задан, пропускаю ping")
            return
            
        try:
            # Добавляем таймаут, чтобы не зависнуть
            response = requests.get(
                f"{self.app_url}/health",
                timeout=10,
                headers={'User-Agent': 'KeepAlive/1.0'}
            )
            
            if response.status_code == 200:
                logger.info(f"KeepAlive: успешный ping - {self.app_url}")
            else:
                logger.warning(f"KeepAlive: ping вернул статус {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"KeepAlive: ошибка ping - {e}")
    
    def _run(self):
        """Основной цикл для периодических ping-запросов"""
        logger.info(f"KeepAlive: запущен (интервал {self.interval} сек)")
        
        while self.running:
            time.sleep(self.interval)
            if self.running:  # Проверяем снова после sleep
                self._ping()
    
    def start(self):
        """Запускает фоновый поток для keep-alive"""
        if self.running:
            logger.warning("KeepAlive: уже запущен")
            return
        
        if not self.app_url:
            logger.info("KeepAlive: app_url не задан, keep-alive отключен")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        logger.info("KeepAlive: поток запущен")
    
    def stop(self):
        """Останавливает keep-alive"""
        if not self.running:
            return
        
        logger.info("KeepAlive: остановка...")
        self.running = False
        
        if self.thread:
            self.thread.join(timeout=5)
        
        logger.info("KeepAlive: остановлен")
