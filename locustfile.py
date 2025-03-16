from locust import User, task, between
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import logging
import time
import sys

start_time = time.time()

# Создаем обработчик для записи логов в файл
file_handler = logging.FileHandler("test.log", encoding="utf-8")

# Создаем обработчик для вывода логов в Run/консоль
console_handler = logging.StreamHandler(sys.__stdout__)  # <--- Используем sys.__stdout__

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[file_handler, console_handler]  # Добавляем два обработчика
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
        logging.info(" Загружаем страницу index.html \U000023F3")
        self.driver.get("https://xey.gbo.mybluehost.me/index.html")
        logging.info(" Страница index.html загрузилась \u2705")

        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        logging.info("Страница загрузила все элементы \u2705")

        # Ожидание и клик по первой найденной кнопке
        more_detailed_buttons = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-button")))
        logging.info("Ожидаем, когда можно будет нажать на кнопку More Detailed \U000023F3 ")
        logging.info("Ожидаем, что на кнопку More Detailed можно нажать \U000023F3 ")

        if more_detailed_buttons:
            first_buttom = more_detailed_buttons[0]
            self.wait.until(EC.element_to_be_clickable(first_buttom))
            first_buttom.click()
            logging.info("Клик по первой кнопке More Detailed \u2735")
        else:
            logging.info("Кнопка More Detailed не найдена \u2705")

        try:
            logging.info("Ожидаем страницу с расписанием Sveti Stefan \U000023F3")
            self.driver.get("https://xey.gbo.mybluehost.me/budva-sveti-stefan-budva.html")
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            load_time = time.time() - start_time
            logging.info(f"⏳ Время загрузки страницы: {load_time:.2f} секунд")

            if "404" in self.driver.page_source:
                raise Exception("Страница не найдена \u274c")
            logging.info("Страница Sveti Stefan загрузилась \u2705")
        except Exception as e:
            logging.info(f"Страница не открыта: {e} \u274c")

        try:
            logging.info("Waiting the button Schedule_button")
            schedule_buttons = self.wait.until(EC.presence_of_all_elements_located((By.ID, "detailedScheduleButton")))
            logging.info("Button found \u2705")
        except Exception as e:
            logging.info(f"The button was not found: {e} \u274c")

        if schedule_buttons:
            sch_but_01 = schedule_buttons
            logging.info("Ждем загрузки кнопки Detailed Schedule \U000023F3")
            try:
                self.wait.until(EC.element_to_be_clickable((By.ID, "detailedScheduleButton")))
                logging.info("Кнопка Detailed Schedule загрузилась \u2705")
            except Exception as e:
                logging.info(f"The button was not loud: {e} \u274c")
                sch_but_01.click()
                logging.info("Кнопка нажата ")

        else:
            logging.info("Клик не сработал \u274c")

        try:
            logging.info("Загружаем попап с расписанием Budva-Sveti Stefan \U000023F3")
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "popup-content")))
            logging.info("Popup загрузился")

        except Exception as e:
            logging.info(f"Popup не найден {e} \u274c")


time.sleep(5)
