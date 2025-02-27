from locust import User, task, between
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import logging
import time

# Настраиваем логирование в консоль
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


class SeleniumUser(User):
    wait_time = between(1, 3)

    def on_start(self):
        """ Инициализация WebDriver перед тестами """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # Без открытия окна браузера
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36')
        chrome_options.add_argument('referer=https://xey.gbo.mybluehost.me/')

        CHROME_DRIVER_PATH = 'D:/xampp/htdocs/auto-test/chromedriver-win64/chromedriver.exe'
        service = Service(CHROME_DRIVER_PATH)

        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def on_stop(self):
        """ Закрытие браузера после тестов """
        self.driver.quit()

    @task
    def full_user_flow(self):
        """ Основной тестовый сценарий """
        logging.info("Загружаем страницу")
        self.driver.get("https://xey.gbo.mybluehost.me/index.html")
        logging.info("Страница загрузилась")

        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        logging.info("Страница загрузила все элементы")

        # Ожидание и клик по первой найденной кнопке
        more_detailed_buttons = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-button")))
        logging.info("Ожидаем, когда можно будет нажать на кнопку More Detailed")

        if more_detailed_buttons:
            more_detailed_buttons[0].click()
            logging.info("Клик по первой кнопке More Detailed")
        else:
            logging.info("Кнопка More Detailed не найдена")

        time.sleep(1)
